// Ghép các khung hình đã tách nền của từng nhân vật thành sprite webp dạng lưới, cùng khung cắt chung cho mọi đoạn của nhân vật đó.
// Dùng: node vid_pack.js <thư mục khung (mỗi đoạn một thư mục con <id>_<đoạn>)> <thư mục ra> <chiều cao dáng đứng> <id ...>
// Khung bị giới hạn tối đa MW x MH (biến môi trường, mặc định 460x300) để ảnh giải nén không quá nặng.
// In ra JSON mô tả: kích thước khung, số cột, số khung, điểm chạm đất (gx, gy) và chiều cao dáng đứng (rh) trong khung.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const [src, dst, RH, ...ids] = process.argv.slice(2), MW = +(process.env.MW || 460), MH = +(process.env.MH || 300);
(async () => { const b = await chromium.launch(); const p = await b.newPage(); fs.mkdirSync(dst, { recursive: true }); const meta = {};
  for (const id of ids) {
    const clips = fs.readdirSync(src).filter(d => d.startsWith(id + '_')).map(d => d.slice(id.length + 1));
    const frames = {}; for (const c of clips) frames[c] = fs.readdirSync(path.join(src, id + '_' + c)).filter(f => f.endsWith('.png')).sort().map(f => 'data:image/png;base64,' + fs.readFileSync(path.join(src, id + '_' + c, f)).toString('base64'));
    const res = await p.evaluate(async ([frames, RH, MW, MH]) => {
      const load = async d => { const im = new Image(); im.src = d; await im.decode(); return im };
      const all = {}; for (const c in frames) all[c] = await Promise.all(frames[c].map(load));
      const W = 832, H = 480, cv = document.createElement('canvas'); cv.width = W; cv.height = H; const x = cv.getContext('2d', { willReadFrequently: true });
      const bbox = im => { x.clearRect(0, 0, W, H); x.drawImage(im, 0, 0); const a = x.getImageData(0, 0, W, H).data; let x0 = W, x1 = 0, y0 = H, y1 = 0;
        for (let y = 0; y < H; y += 2) for (let i = 0; i < W; i += 2) if (a[(y * W + i) * 4 + 3] > 40) { if (i < x0) x0 = i; if (i > x1) x1 = i; if (y < y0) y0 = y; if (y > y1) y1 = y } return [x0, y0, x1, y1] };
      let U = [W, H, 0, 0]; for (const c in all) for (const im of all[c]) { const q = bbox(im); U = [Math.min(U[0], q[0]), Math.min(U[1], q[1]), Math.max(U[2], q[2]), Math.max(U[3], q[3])] }
      U = [Math.max(0, U[0] - 6), Math.max(0, U[1] - 6), Math.min(W, U[2] + 6), Math.min(H, U[3] + 6)];
      const rest = bbox(all[Object.keys(all)[0]][0]), s = Math.min(RH / (rest[3] - rest[1]), MW / (U[2] - U[0]), MH / (U[3] - U[1])), fw = Math.round((U[2] - U[0]) * s), fh = Math.round((U[3] - U[1]) * s);
      const out = {}; for (const c in all) { const n = all[c].length, cols = Math.ceil(Math.sqrt(n * fh / fw)), rows = Math.ceil(n / cols), o = document.createElement('canvas');
        o.width = cols * fw; o.height = rows * fh; const ox = o.getContext('2d'); ox.imageSmoothingQuality = 'high';
        all[c].forEach((im, k) => ox.drawImage(im, U[0], U[1], U[2] - U[0], U[3] - U[1], (k % cols) * fw, Math.floor(k / cols) * fh, fw, fh));
        out[c] = { data: o.toDataURL('image/webp', .76), n, cols } }
      return { out, fw, fh, gx: Math.round((W * .4 - U[0]) * s), gy: Math.round((440 - U[1]) * s), rh: Math.round((rest[3] - rest[1]) * s) } }, [frames, +RH, MW, MH]);
    meta[id] = { fw: res.fw, fh: res.fh, gx: res.gx, gy: res.gy, rh: res.rh };
    for (const c in res.out) { const buf = Buffer.from(res.out[c].data.split(',')[1], 'base64'); fs.writeFileSync(path.join(dst, `${id}_${c}.webp`), buf); meta[id][c] = { n: res.out[c].n, cols: res.out[c].cols }; console.error(id, c, Math.round(buf.length / 1024) + 'KB') } }
  console.log(JSON.stringify(meta)); await b.close() })();
