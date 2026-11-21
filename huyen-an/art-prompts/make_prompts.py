# Sinh bộ câu lệnh tạo tranh (prompt) cho từng lá bài, đối thủ và chủ tiệm.
# Chạy: python3 make_prompts.py  ->  prompts.json + PROMPTS.md
import json, pathlib

STYLE = ("dark fantasy trading card illustration, painterly digital painting, dramatic rim lighting, "
         "rich detail, single creature centered, three-quarter view, dark atmospheric background lit by {glow}, "
         "high contrast, vertical composition, no text, no border, no frame, no watermark")
NEGATIVE = ("text, letters, logo, watermark, signature, frame, border, card template, user interface, "
            "multiple creatures, blurry, low detail, cartoon, chibi, cute, anime, deformed anatomy, extra limbs")
GLOW = {'hoa': 'ember orange and red firelight', 'thuy': 'deep blue and teal moonlight',
        'moc': 'moss green and amber forest light', 'none': 'cold grey torchlight'}
TIER = ['', 'detailed, ', 'highly detailed, epic, ', 'masterpiece, legendary, epic scale, ', 'masterpiece, mythic, awe-inspiring, epic scale, ']

# id, tên trong game, hệ, bậc (0-4), mô tả tiếng Anh
CARDS = [
 ('boar','Lợn Lòi Than','hoa',0,'a hulking wild boar with coal-black hide, glowing ember cracks across its body, tusks of charred bone'),
 ('rat','Chuột Cống Lửa','hoa',0,'a giant sewer rat wreathed in small flames, burning red eyes, scorched bristling fur'),
 ('ant','Kiến Lửa','hoa',0,'a giant fire ant with a molten orange carapace, mandibles dripping lava'),
 ('cbat','Dơi Hang','hoa',0,'a cave bat with leathery wings glowing ember-red at the edges, fangs bared'),
 ('ogre','Chằn Tinh','hoa',0,'a brutish fire ogre with scarred red skin and a spiked iron club, sparks drifting around it'),
 ('scarab','Bọ Hung Lam','thuy',0,'a large beetle with an iridescent deep-blue shell, glowing cyan markings, water droplets'),
 ('croc','Ngạc Ngư','thuy',0,'an armored swamp crocodile emerging from black water, algae hanging from its scales'),
 ('seahorse','Hải Mã','thuy',0,'a giant warrior seahorse with blade-like fins and bioluminescent blue spots, underwater'),
 ('mud','Bùn Quái','thuy',0,'a shambling swamp mud golem dripping black mud, eyes glowing teal'),
 ('cuttle','Mực Vực Sâu','thuy',0,'an abyssal cuttlefish with glowing tentacles in the deep sea darkness'),
 ('bear','Gấu Rừng Già','moc',0,'an ancient forest bear with moss and lichen growing on its fur, claws like gnarled bark'),
 ('stoat','Chồn Tuyết','moc',0,'a white snow stoat with frost-tipped fur, poised among pine roots'),
 ('falcon','Ưng Xám','moc',0,'a grey hunting falcon with slate feathers diving with talons extended'),
 ('horse','Ngựa Hoang','moc',0,'a wild black stallion with a mane of leaves and vines, glowing green eyes'),
 ('skel','Bộ Xương','moc',0,'an animated skeleton warrior overgrown with roots and moss, holding a rusted sword'),
 ('yeti','Tuyết Nhân','moc',0,'a towering yeti with matted white fur and icy breath among frosted rocks'),
 ('wolf','Sói Non','moc',1,'a young direwolf with silver-grey fur and fierce eyes under moonlight'),
 ('wolf2','Lang Vương (Sói Non tiến hóa)','moc',2,'a massive adult moon wolf king with a silver mane and glowing pale runes on its fur, howling'),
 ('turtle','Giáp Thú','thuy',1,'a giant armored turtle beast with a shell of blue crystal plates'),
 ('fox','Long Tử Phun Lửa','hoa',1,'a young fire drake breathing a jet of flame, small wings spread'),
 ('snake','Thủy Xà','thuy',1,'a water serpent with luminous blue scales coiling through dark water'),
 ('scorp','Bọ Cạp Lửa','hoa',1,'a scorpion with an obsidian carapace and a glowing molten stinger raised high'),
 ('rscorp','Bọ Cạp Đá','moc',1,'a scorpion made of mossy stone plates and rock, cracks glowing green'),
 ('spider','Nhện Giăng Tơ','moc',1,'a giant spider weaving glowing silk webs, a cluster of green eyes'),
 ('troll','Quỷ Đập Đá','moc',1,'a hulking rock troll smashing a boulder apart with a stone club'),
 ('naga','Xà Nữ','thuy',1,'a naga warrior with a serpent lower body and sea-green scales, wielding a trident'),
 ('ghoul','Thực Thi Quỷ','moc',1,'a rotting ghoul exhaling poisonous green fumes, long hooked claws'),
 ('shadow','Bóng Ma','thuy',1,'a hooded shadow wraith made of black mist with piercing blue eyes'),
 ('rider','Lang Kỵ','hoa',1,'a goblin raider riding a flaming wolf, spear raised for a charge'),
 ('gale','Phong Linh','thuy',1,'a storm spirit of swirling wind and rain with lightning crackling in its core'),
 ('fguard','Hỏa Vệ Binh','hoa',1,'a fire guardian knight with a flaming halberd, armor glowing like a forge'),
 ('bat','Dạ Bức Vương','thuy',2,'a colossal vampire bat lord with tattered wings and a bone crown before a blood moon'),
 ('phoenix','Hỏa Hồn','hoa',2,'a fire spirit bird rising from ashes, wings made of roaring flame'),
 ('lion','Sư Thứu','moc',2,'a griffin with a lion body and eagle wings, golden-green plumage, wings spread'),
 ('serpent','Hải Xà Vương','thuy',2,'a gigantic sea serpent king rising from a stormy sea, crown of coral and pearls'),
 ('draug','Tử Kỵ Sĩ','hoa',2,'a death knight in blackened armor with burning eyes, ember-wreathed greatsword and tower shield'),
 ('tentacle','Xúc Tu Vực Thẳm','thuy',2,'enormous abyssal tentacles rising from a dark rift, glowing runes along them'),
 ('wose','Mộc Tinh Cổ Thụ','moc',2,'an ancient walking tree spirit with a face in its bark and glowing amber eyes'),
 ('dragon','Cổ Long Tro Tàn','hoa',3,'an ancient ash dragon with scales of cooled magma, embers swirling, glowing throat'),
 ('deer','Cổ Thụ Thần','moc',3,'a divine great stag made of ancient forest, antlers like a tree canopy with glowing leaves'),
 ('reaper','Tử Thần','thuy',4,'the grim reaper in tattered robes holding a huge scythe, cold blue soulfire'),
 ('lich','Hư Vô Chi Vương','thuy',4,'the void lich king on a bone throne, crowned skull, purple void energy swirling'),
 ('soul','Tàn Hồn','none',0,'a faint wandering ghost wisp, pale and translucent'),
]
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
for cid, name, el, r, subj in CARDS:
    out.append({'file': cid + '.png', 'name': name, 'size': '1024x1536',
                'prompt': TIER[r] + subj + ', ' + STYLE.format(glow=GLOW[el]), 'negative': NEGATIVE})
for cid, name, subj in PEOPLE:
    out.append({'file': cid + '.png', 'name': name, 'size': '1024x1536', 'prompt': subj + ', ' + PSTYLE, 'negative': NEGATIVE})

here = pathlib.Path(__file__).parent
(here / 'prompts.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
md = ['# Câu lệnh tạo tranh cho Huyền Ấn', '',
      'Mỗi mục: tên file cần lưu, câu lệnh chính (prompt), câu lệnh loại trừ (negative prompt).',
      'Khổ tranh 2:3 dọc (1024×1536). Lưu đúng tên file rồi gửi lại để gắn vào game.', '',
      'Mẹo giữ phong cách đồng bộ: dùng cùng một công cụ, cùng một model, và nếu công cụ có "seed" hoặc "style reference" thì giữ cố định cho cả bộ.', '']
for o in out:
    md += [f"## {o['file']} · {o['name']}", '', '```', o['prompt'], '```', '', 'Loại trừ: `' + o['negative'] + '`', '']
(here / 'PROMPTS.md').write_text('\n'.join(md), encoding='utf8')
print(len(out), 'prompts')
