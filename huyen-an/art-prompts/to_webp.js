// Chuyển tranh đã tạo (png/jpg) sang webp 480x720 cho game.
// Dùng: node to_webp.js <thư mục tranh gốc> <thư mục web/art>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [src, dst] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  let n = 0, kb = 0;
  for (const f of fs.readdirSync(src).filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f))) {
    const id = f.replace(/\.\w+$/, ''), mime = /png$/i.test(f) ? 'png' : 'jpeg';
    const data = 'data:image/' + mime + ';base64,' + fs.readFileSync(path.join(src, f)).toString('base64');
    const out = await p.evaluate(async d => {
      const im = new Image(); im.src = d; await im.decode();
      const W = 480, H = 720, c = document.createElement('canvas'); c.width = W; c.height = H;
      const x = c.getContext('2d'); x.imageSmoothingQuality = 'high';
      const s = Math.max(W / im.width, H / im.height), w = im.width * s, h = im.height * s;
      x.drawImage(im, (W - w) / 2, (H - h) / 2, w, h);
      return c.toDataURL('image/webp', .82);
    }, data);
    const buf = Buffer.from(out.split(',')[1], 'base64');
    fs.writeFileSync(path.join(dst, id + '.webp'), buf); n++; kb += buf.length / 1024;
  }
  console.log(n, 'files,', Math.round(kb), 'KB');
  await b.close();
})();
