// Chuyển ảnh sang webp với kích thước cho trước (cắt phủ kín).
// Dùng: node conv_any.js <thư mục nguồn> <thư mục đích> <W> <H> [id ...]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [src, dst, W, H, ...ids] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const f of fs.readdirSync(src).filter(f => /\.(png|jpg)$/i.test(f))) {
    const id = f.replace(/\.\w+$/, '');
    if (ids.length && !ids.includes(id)) continue;
    const data = 'data:image/png;base64,' + fs.readFileSync(path.join(src, f)).toString('base64');
    const out = await p.evaluate(async ([d, W, H]) => {
      const im = new Image(); im.src = d; await im.decode();
      const c = document.createElement('canvas'); c.width = W; c.height = H;
      const x = c.getContext('2d'); x.imageSmoothingQuality = 'high';
      const s = Math.max(W / im.width, H / im.height), w = im.width * s, h = im.height * s;
      x.drawImage(im, (W - w) / 2, (H - h) / 2, w, h);
      return c.toDataURL('image/webp', .8);
    }, [data, +W, +H]);
    const buf = Buffer.from(out.split(',')[1], 'base64');
    fs.writeFileSync(path.join(dst, id + '.webp'), buf);
    console.log(id, Math.round(buf.length / 1024) + 'KB');
  }
  await b.close();
})();
