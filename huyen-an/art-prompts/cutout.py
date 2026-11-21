"""Tách nền tranh lá bài qua Replicate (851-labs/background-remover) để có hình nhân vật trong suốt.

Dùng:  python3 cutout.py <thư mục ảnh nguồn> <thư mục ra> [id ...]
Token do proxy của môi trường gắn vào, script không đọc khóa nào. Chạy tuần tự, nghỉ giữa các lần để khỏi bị giới hạn tốc độ.
"""
import base64, json, pathlib, subprocess, sys, time

API = 'https://api.replicate.com/v1'
VER = 'a029dff38972b5fda4ec5d75d7d1cd25aeff621d2cf4946a41055d7db66b80bc'


def curl(args, data=None):
    return subprocess.run(['curl', '-s', '-m', '180'] + args, input=data, capture_output=True, text=True).stdout


def one(src, dst):
    uri = 'data:image/%s;base64,' % src.suffix[1:] + base64.b64encode(src.read_bytes()).decode()
    body = json.dumps({'version': VER, 'input': {'image': uri, 'format': 'png', 'background_type': 'rgba'}})
    for _ in range(8):
        pred = json.loads(curl(['-X', 'POST', '-H', 'Content-Type: application/json', '-H', 'Prefer: wait=60', '--data-binary', '@-', f'{API}/predictions'], body))
        if pred.get('status') == 429:
            time.sleep(int(pred.get('retry_after', 10)) + 1); continue
        break
    for _ in range(60):
        if pred.get('status') in ('succeeded', 'failed', 'canceled') or 'id' not in pred:
            break
        time.sleep(2); pred = json.loads(curl([f"{API}/predictions/{pred['id']}"]))
    if pred.get('status') != 'succeeded':
        return 'lỗi: ' + str(pred.get('error') or pred.get('detail') or pred)[:200]
    out = pred['output']; url = out[0] if isinstance(out, list) else out
    subprocess.run(['curl', '-s', '-m', '120', '-o', str(dst), url])
    return 'xong %.4fs' % (pred.get('metrics') or {}).get('predict_time', 0)


if __name__ == '__main__':
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    ids = sys.argv[3:] or sorted(p.stem for p in src.glob('*.webp'))
    for i in ids:
        dst = out / (i + '.png')
        if dst.exists():
            print(i, 'có sẵn'); continue
        print(i, one(next(src.glob(i + '.*')), dst), flush=True)
        time.sleep(11)
