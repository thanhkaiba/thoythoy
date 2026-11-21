# Sinh bộ câu lệnh tạo tranh (prompt) cho từng lá bài, đối thủ và chủ tiệm.
# Chạy: python3 make_prompts.py  ->  prompts.json + PROMPTS.md
import json, pathlib

STYLE = ("dark fantasy trading card illustration, painterly digital painting, dramatic rim lighting, "
         "rich detail, single creature centered, three-quarter view, dark atmospheric background lit by {glow}, "
         "high contrast, vertical composition, no text, no border, no frame, no watermark")
NEGATIVE = ("text, letters, logo, watermark, signature, frame, border, card template, user interface, "
            "multiple creatures, blurry, low detail, cartoon, chibi, anime, flat colors, deformed anatomy, extra limbs")
GLOW = {'hoa': 'ember orange and red firelight', 'thuy': 'deep blue and teal moonlight',
        'moc': 'moss green and amber forest light', 'none': 'cold grey torchlight'}
TIER = ['', 'detailed, ', 'highly detailed, epic, ', 'masterpiece, legendary, epic scale, ', 'masterpiece, mythic, awe-inspiring, epic scale, ']

# id, tên trong game, hệ, bậc (0-4), mô tả tiếng Anh
from cards_v2 import CARDS, MOOD
PEOPLE = [
 ('o1','Lữ Khách Vô Danh (Cổng Tro)','a hooded nameless wanderer in grey rags holding a lantern, at a gate of ash'),
 ('o2','Tín Đồ Lạc Lối (Rừng Chết)','a lost cultist in tattered blue robes with a bone necklace and a ritual dagger, dead forest'),
 ('o3','Thợ Săn Rừng Sâu (Hẻm Xương)','a grim deep-forest hunter with a longbow and a bone mask, canyon of bones'),
 ('o4','Kỵ Sĩ Tro Tàn (Lò Thiêu)','an ash knight in charred armor holding a great axe, furnace glow'),
 ('o5','Kẻ Nuôi Nhện (Hang Nhện)','a spider-keeper sorcerer draped in webs with small spiders on his arms, cave'),
 ('o6','Phù Thủy Đầm Lầy (Đầm Oán Hồn)','a swamp witch with a crooked staff and will-o-wisps, haunted marsh'),
 ('o7','Long Kỵ Sĩ (Sào Huyệt Rồng)','a dragon knight in red armor holding a dragon-head lance, dragon lair'),
 ('merchant','Lão Hắc Thị (chủ tiệm)','a sly hooded black-market merchant leaning on a mace, coins and potions on a table'),
]
PSTYLE = ("dark fantasy character portrait, painterly digital painting, waist-up, dramatic rim lighting, rich detail, "
          "dark atmospheric background, high contrast, vertical composition, no text, no border, no frame, no watermark")

out = []
for cid, name, el, r, mood, subj in CARDS:
    out.append({'file': cid + '.png', 'name': name, 'mood': mood, 'size': '1024x1536',
                'prompt': TIER[r] + subj + ', ' + MOOD[mood] + ', ' + STYLE.format(glow=GLOW[el]), 'negative': NEGATIVE})
for cid, name, subj in PEOPLE:
    out.append({'file': cid + '.png', 'name': name, 'size': '1024x1536', 'prompt': subj + ', ' + PSTYLE, 'negative': NEGATIVE})

here = pathlib.Path(__file__).parent
(here / 'prompts.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
md = ['# Câu lệnh tạo tranh cho Huyền Ấn', '',
      'Mỗi mục: tên file cần lưu, câu lệnh chính (prompt), câu lệnh loại trừ (negative prompt).',
      'Khổ tranh 2:3 dọc (1024×1536). Lưu đúng tên file rồi gửi lại để gắn vào game.', '',
      'Mẹo giữ phong cách đồng bộ: dùng cùng một công cụ, cùng một model, và nếu công cụ có "seed" hoặc "style reference" thì giữ cố định cho cả bộ.', '']
for o in out:
    md += [f"## {o['file']} · {o['name']}" + (f" · {o['mood']}" if o.get('mood') else ''), '', '```', o['prompt'], '```', '', 'Loại trừ: `' + o['negative'] + '`', '']
(here / 'PROMPTS.md').write_text('\n'.join(md), encoding='utf8')
print(len(out), 'prompts')
