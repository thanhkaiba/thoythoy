// Cắt sát phần trong suốt quanh hình đã tách nền rồi lưu webp, để đáy hình trùng với chân nhân vật hoặc đáy vật cản.
// Dùng: node crop_webp.js <thư mục png> <thư mục ra> <rộng tối đa> <cao tối đa> [id ...]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [src, dst, MW, MH, ...ids] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); fs.mkdirSync(dst, { recursive: true });
  for (const f of fs.readdirSync(src).filter(f => f.endsWith('.png'))) {
    const id = f.slice(0, -4); if (ids.length && !ids.includes(id)) continue;
    const data = 'data:image/png;base64,' + fs.readFileSync(path.join(src, f)).toString('base64');
    const [out, info] = await p.evaluate(async ([d, MW, MH]) => {
      const im = new Image(); im.src = d; await im.decode();
      const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const x = c.getContext('2d'); x.drawImage(im, 0, 0);
      const a = x.getImageData(0, 0, c.width, c.height).data; let x0 = c.width, x1 = 0, y0 = c.height, y1 = 0;
      for (let y = 0; y < c.height; y++) for (let i = 0; i < c.width; i++) if (a[(y * c.width + i) * 4 + 3] > 24) { if (i < x0) x0 = i; if (i > x1) x1 = i; if (y < y0) y0 = y; if (y > y1) y1 = y }
      x0 = Math.max(0, x0 - 2); y0 = Math.max(0, y0 - 2); x1 = Math.min(c.width - 1, x1 + 2); y1 = Math.min(c.height - 1, y1 + 1);
      const w = x1 - x0 + 1, h = y1 - y0 + 1, s = Math.min(1, MW / w, MH / h), o = document.createElement('canvas');
      o.width = Math.round(w * s); o.height = Math.round(h * s); const ox = o.getContext('2d'); ox.imageSmoothingQuality = 'high'; ox.drawImage(c, x0, y0, w, h, 0, 0, o.width, o.height);
      return [o.toDataURL('image/webp', .82), o.width + 'x' + o.height];
    }, [data, +MW, +MH]);
    const buf = Buffer.from(out.split(',')[1], 'base64'); fs.writeFileSync(path.join(dst, id + '.webp'), buf);
    console.log(id, info, Math.round(buf.length / 1024) + 'KB');
  }
  await b.close();
})();
