// Tách tranh ba vật cản (đã tách nền) thành ba hình riêng theo khoảng trống giữa chúng, cắt sát, vẽ sẵn lớp tối chân theo loại, lưu webp.
// Dùng: node split_props.js <thư mục png đã tách nền (props<i>.png)> <thư mục ra>   → prop<i>_tree|fire|rock.webp (trái: lạnh, giữa: nóng, phải: phế liệu)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const [src, dst] = process.argv.slice(2);
const LOOK = { tree: [['up', '#1f5f8480', 0, '#0000', .3], ['down', '#ffffff22', 0, '#0000', .35]],
  fire: [['up', '#0009', 0, '#0000', .22], ['up', '#ff6a1f28', 0, '#0000', .5]],
  rock: [['up', '#000b', 0, '#0000', .28], ['down', '#29e6ff18', 0, '#0000', .25]] };
(async () => { const b = await chromium.launch(); const p = await b.newPage(); fs.mkdirSync(dst, { recursive: true });
  for (const f of fs.readdirSync(src).filter(f => /^props\d+\.png$/.test(f)).sort()) { const i = f.match(/\d+/)[0];
    const d = 'data:image/png;base64,' + fs.readFileSync(path.join(src, f)).toString('base64');
    const out = await p.evaluate(async ([d, LOOK]) => { const im = new Image(); im.src = d; await im.decode(); const W = im.width, H = im.height;
      const c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d'); x.drawImage(im, 0, 0); const a = x.getImageData(0, 0, W, H).data;
      const col = new Array(W).fill(0); for (let y = 0; y < H; y++) for (let i = 0; i < W; i++) if (a[(y * W + i) * 4 + 3] > 60) col[i]++;
      // cắt tại cột thưa nhất quanh mốc 1/3 và 2/3, rồi trong mỗi phần lấy dải cột liền nhau rộng nhất (bỏ mảnh vụn lẻ)
      const cut = (lo, hi) => { let bi = lo | 0, bv = 1e9; for (let i = lo | 0; i < hi; i++) { let v = 0; for (let j = -3; j <= 3; j++) v += col[i + j] || 0; if (v < bv) { bv = v; bi = i } } return bi };
      const c1 = cut(W * .22, W * .45), c2 = cut(W * .55, W * .78);
      const top = [[0, c1], [c1, c2], [c2, W - 1]].map(([lo, hi]) => { const runs = []; let s = -1;
        for (let i = lo; i <= hi + 1; i++) { const on = i <= hi && col[i] > 3; if (on && s < 0) s = i; if (!on && s >= 0) { if (runs.length && s - runs[runs.length - 1][1] < 14) runs[runs.length - 1][1] = i - 1; else runs.push([s, i - 1]); s = -1 } }
        return runs.sort((p, q) => (q[1] - q[0]) - (p[1] - p[0]))[0] || [lo, hi] });
      return top.map(([x0, x1], k) => { let y0 = H, y1 = 0; for (let y = 0; y < H; y++) for (let i = x0; i <= x1; i++) if (a[(y * W + i) * 4 + 3] > 24) { if (y < y0) y0 = y; if (y > y1) y1 = y }
        const w = x1 - x0 + 1, h = y1 - y0 + 1, sc = Math.min(1, 420 / w, 420 / h), o = document.createElement('canvas'); o.width = Math.round(w * sc); o.height = Math.round(h * sc);
        const ox = o.getContext('2d'); ox.imageSmoothingQuality = 'high'; ox.drawImage(c, x0, y0, w, h, 0, 0, o.width, o.height); ox.globalCompositeOperation = 'source-atop';
        for (const [dir, c0, s0, c1, s1] of LOOK[['tree', 'fire', 'rock'][k]]) { const g = dir === 'up' ? ox.createLinearGradient(0, o.height, 0, 0) : ox.createLinearGradient(0, 0, 0, o.height); g.addColorStop(s0, c0); g.addColorStop(s1, c1); ox.fillStyle = g; ox.fillRect(0, 0, o.width, o.height) }
        return [o.toDataURL('image/webp', .84), o.width + 'x' + o.height] }) }, [d, LOOK]);
    out.forEach(([data, sz], k) => { const t = ['tree', 'fire', 'rock'][k], buf = Buffer.from(data.split(',')[1], 'base64'); fs.writeFileSync(path.join(dst, `prop${i}_${t}.webp`), buf); console.log(`prop${i}_${t}`, sz, Math.round(buf.length / 1024) + 'KB') }) }
  await b.close() })();
