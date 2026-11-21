// Đặt hình nhân vật đã tách nền lên nền xanh phẳng 832x480, quay mặt sang phải, chân chạm vạch đất, làm khung đầu và khung cuối cho video.
// Dùng: node vid_compose.js <thư mục png tách nền> <thư mục ra> <id:hướng> ...   (hướng 1 = đang nhìn phải, -1 = nhìn trái, 0 = nhìn thẳng)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const [src, dst, ...items] = process.argv.slice(2);
(async () => { const b = await chromium.launch(); const p = await b.newPage(); fs.mkdirSync(dst, { recursive: true });
  for (const it of items) { const [id, face] = it.split(':');
    const d = 'data:image/png;base64,' + fs.readFileSync(path.join(src, id + '.png')).toString('base64');
    const out = await p.evaluate(async ([d, flip]) => { const im = new Image(); im.src = d; await im.decode();
      const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const x = c.getContext('2d'); x.drawImage(im, 0, 0);
      const a = x.getImageData(0, 0, c.width, c.height).data; let x0 = c.width, x1 = 0, y0 = c.height, y1 = 0;
      for (let y = 0; y < c.height; y++) for (let i = 0; i < c.width; i++) if (a[(y * c.width + i) * 4 + 3] > 24) { if (i < x0) x0 = i; if (i > x1) x1 = i; if (y < y0) y0 = y; if (y > y1) y1 = y }
      const w = x1 - x0 + 1, h = y1 - y0 + 1, s = Math.min(330 / h, 360 / w), o = document.createElement('canvas'); o.width = 832; o.height = 480; const ox = o.getContext('2d');
      ox.fillStyle = '#00b140'; ox.fillRect(0, 0, 832, 480); const dw = w * s, dh = h * s, cx = 832 * .4, gy = 440;
      ox.save(); if (flip) { ox.translate(cx * 2, 0); ox.scale(-1, 1) } ox.drawImage(c, x0, y0, w, h, cx - dw / 2, gy - dh, dw, dh); ox.restore();
      return o.toDataURL('image/png') }, [d, face === '-1']);
    fs.writeFileSync(path.join(dst, id + '.png'), Buffer.from(out.split(',')[1], 'base64')); console.log(id) }
  await b.close() })();
