"""Tạo đoạn video hoạt ảnh cho nhân vật qua Replicate (wan-video/wan-2.2-i2v-fast).

Dùng:  python3 vid_gen.py <thư mục ảnh vào> <thư mục ra> <tệp jobs.json> [tên job ...]
jobs.json: [{"name": "boar_atk", "id": "boar", "prompt": "..."}]. Khung đầu và khung cuối đều là ảnh vào, để đoạn video quay về tư thế ban đầu.
Token do proxy của môi trường gắn vào, script không đọc khóa nào. Chạy tuần tự để khỏi bị giới hạn tốc độ.
"""
import base64, json, pathlib, subprocess, sys, time

API = 'https://api.replicate.com/v1'
MODEL = 'wan-video/wan-2.2-i2v-fast'


def curl(args, data=None):
    return subprocess.run(['curl', '-s', '-m', '300'] + args, input=data, capture_output=True, text=True).stdout


def run(job, src, out):
    dst = out / (job['name'] + '.mp4')
    if dst.exists():
        return 'có sẵn'
    uri = 'data:image/png;base64,' + base64.b64encode((src / (job['id'] + '.png')).read_bytes()).decode()
    body = json.dumps({'input': {'image': uri, 'last_image': uri, 'prompt': job['prompt'], 'num_frames': job.get('frames', 81),
                                 'resolution': '480p', 'frames_per_second': 16, 'seed': job.get('seed', 7)}})
    for _ in range(8):
        pred = json.loads(curl(['-X', 'POST', '-H', 'Content-Type: application/json', '-H', 'Prefer: wait=60', '--data-binary', '@-', f'{API}/models/{MODEL}/predictions'], body))
        if pred.get('status') == 429:
            time.sleep(int(pred.get('retry_after', 10)) + 1); continue
        break
    t0 = time.time()
    while 'id' in pred and pred.get('status') not in ('succeeded', 'failed', 'canceled') and time.time() - t0 < 600:
        time.sleep(4); pred = json.loads(curl([f"{API}/predictions/{pred['id']}"]))
    if pred.get('status') != 'succeeded':
        return 'lỗi: ' + str(pred.get('error') or pred.get('detail') or pred.get('status'))[:300]
    o = pred['output']; url = o[0] if isinstance(o, list) else o
    subprocess.run(['curl', '-s', '-m', '300', '-o', str(dst), url])
    return 'xong %.1fs' % (pred.get('metrics') or {}).get('predict_time', 0)


if __name__ == '__main__':
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    jobs = json.loads(pathlib.Path(sys.argv[3]).read_text(encoding='utf8'))
    want = sys.argv[4:]
    for j in jobs:
        if want and j['name'] not in want:
            continue
        print(j['name'], run(j, src, out), flush=True)
