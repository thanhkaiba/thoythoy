# Sinh bộ câu lệnh tạo tranh (prompt) cho từng lá bài và boss.
# Chạy: python3 make_prompts.py  ->  prompts.json + PROMPTS.md
import json, pathlib
from cards_v4 import CARDS, PEOPLE, MOOD, ACCENT, STYLE, BSTYLE, NEGATIVE

TIER = ['', 'detailed, ', 'highly detailed, epic, ', 'masterpiece, legendary, epic scale, ', 'masterpiece, mythic, awe-inspiring, epic scale, ']

out = []
for cid, name, el, r, mood, subj, loc, angle, pal in CARDS:
    out.append({'file': cid + '.png', 'name': name, 'mood': mood, 'size': '1024x1536',
                'prompt': TIER[r] + subj + ', ' + MOOD[mood] + ', ' + STYLE.format(angle=angle, loc=loc, pal=pal, acc=ACCENT[el]),
                'negative': NEGATIVE})
for cid, name, subj, loc, angle, pal in PEOPLE:
    out.append({'file': cid + '.png', 'name': name, 'size': '1024x1536',
                'prompt': subj + ', ' + BSTYLE.format(angle=angle, loc=loc, pal=pal), 'negative': NEGATIVE})

here = pathlib.Path(__file__).parent
(here / 'prompts.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
md = ['# Câu lệnh tạo tranh cho Huyền Ấn (bản cyberpunk v4)', '',
      'Mỗi mục: tên file, câu lệnh chính, câu lệnh loại trừ. Khổ 2:3 dọc.', '']
for o in out:
    md += [f"## {o['file']} · {o['name']}" + (f" · {o['mood']}" if o.get('mood') else ''), '', '```', o['prompt'], '```', '',
           'Loại trừ: `' + o['negative'] + '`', '']
(here / 'PROMPTS.md').write_text('\n'.join(md), encoding='utf8')
print(len(out), 'prompts')
