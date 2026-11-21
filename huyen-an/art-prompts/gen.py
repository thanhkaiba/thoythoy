"""Tạo tranh qua Replicate từ prompts.json.

Dùng:  python3 gen.py <model> <thư mục ra> [id ...]
  model: flux2 | imagen4 | seedream4 | ideogram3
Token Replicate do proxy của môi trường tự gắn vào yêu cầu, script không đọc khóa nào.
"""
import json, subprocess, sys, time, pathlib, zlib, concurrent.futures as cf

HERE = pathlib.Path(__file__).parent
MODELS = {
    'flux2': ('black-forest-labs/flux-2-pro', lambda p, sd=7: {'prompt': p, 'aspect_ratio': '2:3', 'resolution': '1 MP', 'output_format': 'png', 'seed': sd, 'safety_tolerance': 5}),
    'imagen4': ('google/imagen-4', lambda p: {'prompt': p, 'aspect_ratio': '3:4', 'image_size': '1K', 'output_format': 'png', 'safety_filter_level': 'block_only_high'}),
    'seedream4': ('bytedance/seedream-4', lambda p: {'prompt': p, 'aspect_ratio': '2:3', 'size': '2K', 'enhance_prompt': False}),
    'ideogram3': ('ideogram-ai/ideogram-v3-quality', lambda p: {'prompt': p, 'aspect_ratio': '2:3', 'magic_prompt_option': 'Off', 'seed': 7}),
}
API = 'https://api.replicate.com/v1'


def curl(args):
    r = subprocess.run(['curl', '-s', '-m', '180'] + args, capture_output=True, text=True)
    return r.stdout


def run(model_key, item, out_dir):
    name, make = MODELS[model_key]
    dest = out_dir / item['file'].replace('.png', '')
    if any(out_dir.glob(dest.name + '.*')):
        return item['file'], 'có sẵn'
    body = json.dumps({'input': make(item['prompt'], zlib.crc32(item['file'].encode()) % 100000) if model_key == 'flux2' else make(item['prompt'])})
    for attempt in range(8):
        raw = curl(['-X', 'POST', '-H', 'Content-Type: application/json', '-H', 'Prefer: wait=60', '-d', body, f'{API}/models/{name}/predictions'])
        try:
            pred = json.loads(raw)
        except ValueError:
            return item['file'], 'lỗi: ' + raw[:200]
        if pred.get('status') == 429:
            time.sleep(int(pred.get('retry_after', 10)) + 1)
            continue
        break
    if 'id' not in pred:
        return item['file'], 'lỗi: ' + raw[:300]
    for _ in range(90):
        if pred.get('status') in ('succeeded', 'failed', 'canceled'):
            break
        time.sleep(3)
        pred = json.loads(curl([f"{API}/predictions/{pred['id']}"]))
    if pred.get('status') != 'succeeded':
        return item['file'], 'lỗi: ' + str(pred.get('error') or pred.get('detail') or pred.get('status'))[:200]
    out = pred['output']
    url = out[0] if isinstance(out, list) else out
    ext = url.split('?')[0].rsplit('.', 1)[-1]
    subprocess.run(['curl', '-s', '-m', '180', '-o', f'{dest}.{ext}', url])
    return item['file'], 'xong'


if __name__ == '__main__':
    model_key, out = sys.argv[1], pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    items = json.loads((HERE / 'prompts.json').read_text(encoding='utf8'))
    want = sys.argv[3:]
    if want:
        items = [i for i in items if i['file'].replace('.png', '') in want]
    with cf.ThreadPoolExecutor(4) as ex:
        for f, st in ex.map(lambda it: run(model_key, it, out), items):
            print(model_key, f, st, flush=True)
