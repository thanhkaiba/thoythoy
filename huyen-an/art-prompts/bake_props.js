// Vẽ sẵn lớp tối ở chân và ánh viền lên ảnh vật cản (thay cho mask CSS, vì mask không tải được khi chạy từ file://).
// Dùng: node bake_props.js <thư mục webp nguồn> <thư mục ra>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const [src, dst] = process.argv.slice(2);
const LOOK = { tree: [['to top', '#2a6a8aa0', 0, '#0000', .35], ['to bottom', '#ffffff30', 0, '#0000', .4]],
  fire: [['to top', '#000a', 0, '#0000', .25], ['to top', '#ff6a1f40', 0, '#0000', .6]],
  rock: [['to top', '#000c', 0, '#0000', .32], ['to bottom', '#29e6ff26', 0, '#0000', .28]] };
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  for (const t of Object.keys(LOOK)) {
    const d = 'data:image/webp;base64,' + fs.readFileSync(path.join(src, `prop_${t}.webp`)).toString('base64');
    const out = await p.evaluate(async ([d, L]) => { const im = new Image(); im.src = d; await im.decode();
      const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const x = c.getContext('2d'); x.drawImage(im, 0, 0); x.globalCompositeOperation = 'source-atop';
      for (const [dir, c0, s0, c1, s1] of L) { const g = dir === 'to top' ? x.createLinearGradient(0, c.height, 0, 0) : x.createLinearGradient(0, 0, 0, c.height); g.addColorStop(s0, c0); g.addColorStop(s1, c1); x.fillStyle = g; x.fillRect(0, 0, c.width, c.height) }
      return c.toDataURL('image/webp', .85) }, [d, LOOK[t]]);
    const buf = Buffer.from(out.split(',')[1], 'base64'); fs.writeFileSync(path.join(dst, `prop_${t}.webp`), buf); console.log(t, Math.round(buf.length / 1024) + 'KB') }
  await b.close() })();
