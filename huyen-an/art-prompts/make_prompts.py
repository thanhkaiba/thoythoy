# Sinh bộ câu lệnh tạo tranh (prompt) cho từng lá bài, đối thủ và chủ tiệm.
# Chạy: python3 make_prompts.py  ->  prompts.json + PROMPTS.md
import json, pathlib
from cards_v3 import CARDS, PEOPLE, MOOD, STYLE, GLOW, PSTYLE, NEGATIVE

TIER = ['', 'detailed, ', 'highly detailed, epic, ', 'masterpiece, legendary, epic scale, ', 'masterpiece, mythic, awe-inspiring, epic scale, ']

out = []
for cid, name, el, r, mood, subj in CARDS:
    out.append({'file': cid + '.png', 'name': name, 'mood': mood, 'size': '1024x1536',
                'prompt': TIER[r] + subj + ', ' + MOOD[mood] + ', ' + STYLE.format(glow=GLOW[el]), 'negative': NEGATIVE})
for cid, name, subj in PEOPLE:
    out.append({'file': cid + '.png', 'name': name, 'size': '1024x1536', 'prompt': subj + ', ' + PSTYLE, 'negative': NEGATIVE})

here = pathlib.Path(__file__).parent
(here / 'prompts.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
md = ['# Câu lệnh tạo tranh cho Huyền Ấn (bản cyberpunk)', '',
      'Mỗi mục: tên file cần lưu, câu lệnh chính (prompt), câu lệnh loại trừ (negative prompt).',
      'Khổ tranh 2:3 dọc. Lưu đúng tên file rồi gửi lại để gắn vào game.', '']
for o in out:
    md += [f"## {o['file']} · {o['name']}" + (f" · {o['mood']}" if o.get('mood') else ''), '', '```', o['prompt'], '```', '',
           'Loại trừ: `' + o['negative'] + '`', '']
(here / 'PROMPTS.md').write_text('\n'.join(md), encoding='utf8')
print(len(out), 'prompts')
