# Bộ mô tả v3: thế giới cyberpunk, mọi linh thú là máy móc, mỗi con một tính cách và nét "dị" riêng.
MOOD = {
    'cute': 'endearing and charming, big expressive camera eyes, small and lovable, still rendered in the same gritty painterly style',
    'weird': 'strange uncanny surreal machine design, memorable silhouette',
    'grotesque': 'grotesque and horrifying, unsettling mechanical details',
    'eerie': 'eerie and haunting, quiet dread',
    'majestic': 'majestic and awe-inspiring, heroic pose',
    'menacing': 'menacing and intimidating, aggressive pose',
    'whimsical': 'whimsical yet eerie, playful and odd',
}
STYLE = ("cyberpunk trading card illustration, gritty neon-lit dystopian megacity, painterly digital painting, "
         "chrome plating and exposed wiring, holographic glow, light rain, dramatic rim lighting, rich detail, "
         "single machine creature centered, three-quarter view, dark background lit by {glow}, high contrast, "
         "vertical composition, no text, no letters, no logos, no border, no frame, no watermark")
GLOW = {'hoa': 'hot orange and magenta neon', 'thuy': 'icy cyan and blue neon',
        'moc': 'toxic acid-green neon', 'none': 'dim violet neon'}
PSTYLE = ("cyberpunk character portrait, gritty neon-lit dystopian megacity, painterly digital painting, waist-up, "
          "cybernetic implants, dramatic rim lighting, rich detail, dark background, high contrast, vertical composition, "
          "no text, no letters, no logos, no border, no frame, no watermark")
NEGATIVE = ("text, letters, logo, brand name, watermark, signature, frame, border, card template, user interface, "
            "multiple creatures, blurry, low detail, cartoon, chibi, anime, flat colors, deformed anatomy, extra limbs")

# id, tên trong game, hệ, bậc, tính cách, mô tả
CARDS = [
 ('boar','Lợn Lò Hơi','hoa',0,'weird','a robotic wild boar built from a scrapyard boiler, three smoking exhaust chimneys on its back, glowing orange heat vents along its plating, three hydraulic steel tusks, red optic eyes'),
 ('rat','Chuột Cầu Chì','hoa',0,'whimsical','a scrappy robot rat wearing a cracked bronze headlamp as a helmet, its long tail is a sparking power cable fuse, mischievous LED grin'),
 ('ant','Kiến Plasma','hoa',0,'weird','a mechanical ant whose abdomen is a glass fuel cell of swirling orange plasma, needle-thin iron legs, welding sparks at its jaws'),
 ('cbat','Dơi Ăng-ten','hoa',0,'cute','a round little bat drone wrapped in soft orange insulation foam, oversized satellite-dish ears glowing at the tips, big round camera eyes, hanging upside down from a cable'),
 ('ogre','Cự Hán Lò Đúc','hoa',0,'grotesque','a hulking cyborg brute with an open furnace reactor in its belly glowing behind iron grates, chains and pistons on its arms, a bell-shaped hydraulic hammer'),
 ('scarab','Bọ Kính Lam','thuy',0,'cute','a small robot beetle with a polished sapphire glass dome on its back holding a tiny holographic pond with floating lily pads'),
 ('croc','Cá Sấu Tàu Ngầm','thuy',0,'weird','a cyborg crocodile whose back is a wrecked mini submarine covered in barnacles and flickering neon signs, rising from black canal water'),
 ('seahorse','Hiệp Sĩ Hải Mã','thuy',0,'cute','a tiny brave robot seahorse knight with a scrap-metal helmet and a needle antenna lance, bubbles, cyan LED freckles'),
 ('mud','Quái Dầu Thải','thuy',0,'weird','a sludge blob of black machine oil and e-waste with many mismatched camera lenses floating inside it, antennas and a rusty blade sticking out'),
 ('cuttle','Mực Mặt Nạ','thuy',0,'eerie','a robotic cuttlefish with a cracked porcelain android mask for a face, fiber-optic tentacles trailing glowing code'),
 ('bear','Gấu Bảo Trì','moc',0,'weird','an old sleepy maintenance robot bear with a small rusted shrine and paper lanterns on its back, moss and glowing mushrooms along its spine, gentle optic eyes'),
 ('stoat','Chồn Bông','moc',0,'cute','a fluffy white robot stoat with soft synthetic fur and a tiny red scarf, holding a glowing green battery like an acorn, perched on thick cables'),
 ('falcon','Ưng Ba Mắt','moc',0,'weird','a robotic falcon with three glowing optic eyes and feathers made of sharp carbon-fiber blades, diving'),
 ('horse','Ngựa Cáp Quang','moc',0,'eerie','a wild robotic stallion made of bundled fiber-optic cables and vines, a hollow ribcage full of floating green LEDs, glowing eyes'),
 ('skel','Khung Xương Máy','moc',0,'whimsical','a small cheerful salvaged android skeleton with a flowering vine growing through its chassis and a bird nest on its head, holding a rusty pipe sword'),
 ('yeti','Tuyết Nhân Làm Lạnh','moc',0,'weird','a giant cryo yeti mech with a frozen coolant waterfall pouring from its shoulder tanks, icicle beard, a tiny red robot bird on its head'),
 ('wolf','Sói Con Máy','moc',1,'cute','a fluffy robot wolf pup with oversized paws and a glowing crescent-moon LED on its forehead, trying to howl'),
 ('wolf2','Lang Vương Plasma (Sói Con Máy nâng cấp)','moc',2,'majestic','a massive cyber wolf king with a mane of silver plasma and a holographic crescent moon behind its head, glowing circuit patterns on its plating'),
 ('turtle','Rùa Máy Chủ','thuy',1,'weird','a giant tank-like robot turtle whose shell is a cluster of blue crystal server towers like a tiny frozen city with lit windows'),
 ('fox','Long Tử Plasma','hoa',1,'cute','a small young mech drake with stubby wings and a big round head, proudly puffing a little jet of plasma from a nozzle'),
 ('snake','Xà Chất Lỏng','thuy',1,'eerie','a serpent made of flowing translucent liquid coolant with a glowing data pearl visible in its throat'),
 ('scorp','Bọ Cạp Lò Rèn','hoa',1,'menacing','a mechanical scorpion with obsidian armor plates and a stinger that is a glowing molten forge hammer, sparks flying'),
 ('rscorp','Bọ Cạp Bê Tông','moc',1,'weird','a mechanical scorpion assembled from concrete rubble and broken statues, a carved stone face on its back, green circuit cracks'),
 ('spider','Nhện Búp Bê','moc',1,'eerie','a spider drone whose body is a cracked porcelain doll head, weaving glowing fiber-optic webs'),
 ('troll','Robot Phá Dỡ','moc',1,'whimsical','a hulking demolition robot with a bird nest on its head and a grinning grille mouth, smashing a concrete block with a wrecking hammer'),
 ('naga','Xà Nữ Chrome','thuy',1,'eerie','a cyborg naga priestess with a serpentine robotic lower body, sea-green chrome scales, a jellyfish-like holographic crown, holding a trident of coral wires'),
 ('ghoul','Kẻ Nhặt Rác','moc',1,'grotesque','an emaciated scavenger cyborg with a mouth-shaped exhaust on its stomach venting toxic green gas, long hooked metal claws'),
 ('shadow','Bóng Ma Tĩnh Điện','thuy',1,'eerie','a tall hooded ghost android with no face, only a single blue flame flickering inside an empty helmet, body of black smoke and static'),
 ('rider','Kỵ Sĩ Đường Phố','hoa',1,'menacing','a scrawny street punk wearing a cooking pot as a helmet, riding a robot wolf wreathed in plasma flames, spear raised for a charge'),
 ('gale','Diều Bão','thuy',1,'whimsical','a storm drone shaped like a giant floating paper kite with lightning tassels and a rain-cloud exhaust trail, one big camera eye'),
 ('fguard','Vệ Binh Lò Lửa','hoa',1,'menacing','a security mech whose helmet is an open furnace door with flames inside, molten seams in the armor, a plasma halberd'),
 ('bat','Dạ Bức Neon','thuy',2,'grotesque','a colossal vampire bat war-drone with wings made of torn neon billboards and a crown of antennas, before a blood-red moon over the megacity'),
 ('phoenix','Phượng Mạch Điện','hoa',2,'majestic','a phoenix made of burning circuit boards and ember sparks rising from a pile of e-waste ash, long ribbon-cable tail'),
 ('lion','Sư Thứu Đồng','moc',2,'majestic','a mechanical griffin with a lion chassis and eagle wings of brass blades, a mane of autumn-colored cables, wings spread'),
 ('serpent','Hải Xà Máy Chủ','thuy',2,'majestic','a gigantic sea serpent mech wearing a sunken data center as a crown, rising from a stormy toxic sea'),
 ('draug','Tử Kỵ Sĩ Thép','hoa',2,'menacing','a death-knight cyborg whose blackened armor is fused with the bones of a skeletal robot warhorse, burning red visor, glowing greatsword and tower shield'),
 ('tentacle','Xúc Tu Cổng Lỗi','thuy',2,'grotesque','enormous cable tentacles emerging from a glitching eye-shaped portal in the sky above the megacity, glowing code along them, a small hover car caught in their grip'),
 ('wose','Cây Máy Chủ Cổ','moc',2,'eerie','an ancient walking server-tree mech with a giant carved face in its rusted bark plating, an owl drone living in one eye socket, glowing amber coolant sap'),
 ('dragon','Long Cơ Giới','hoa',3,'majestic','an ancient war dragon mech with scales of cooled slag metal and a ruined skyscraper embedded in its back, sparks swirling, glowing reactor throat'),
 ('deer','Thần Lộc Ăng-ten','moc',3,'majestic','a divine great stag machine overgrown with moss, antlers like a canopy of antennas hung with tiny glowing lanterns, a cloak of moss and cables'),
 ('reaper','Tử Thần Lượng Tử','thuy',4,'eerie','a towering grim reaper android in tattered black robes with an hourglass core inside its ribcage, a huge scythe of cold blue energy'),
 ('lich','Trí Tuệ Hư Vô','thuy',4,'majestic','a rogue AI king with a chrome skull face and cables, on a throne of melted crowns and servers, purple void energy and shattered floating holograms'),
 ('soul','Tàn Ảnh','none',0,'cute','a small round ghost hologram with big sad eyes holding a tiny glowing candle'),
]
PEOPLE = [
 ('o1','Kẻ Lang Thang (Mái Neon)','a hooded nameless street drifter in rain-soaked rags holding a glowing lantern, on a neon rooftop'),
 ('o2','Tín Đồ Máy (Chợ Đêm)','a machine cultist in tattered blue robes with cybernetic implants and a necklace of old chips, holding a ritual data blade, in a neon night market'),
 ('o3','Thợ Săn Tiền Thưởng (Hẻm Dây Cáp)','a grim bounty hunter with a long rail rifle and a bone-white mask with red optics, in a cable-choked alley'),
 ('o4','Lính Đánh Thuê Thép (Xưởng Đúc)','a heavy mercenary in charred powered armor holding a great hydraulic axe, in a glowing foundry'),
 ('o5','Kẻ Nuôi Drone (Lưới Ngầm)','a drone-keeper hacker draped in cables with small spider drones crawling on her arms, in an underground server tunnel'),
 ('o6','Phù Thủy Mạng (Cống Độc)','a netrunner witch with a crooked antenna staff and floating holographic wisps, in a toxic sewer'),
 ('o7','Kỵ Sĩ Mech (Lò Phản Ứng)','a mech dragon rider pilot in red armor holding a dragon-headed lance, in a glowing reactor chamber'),
 ('merchant','Lão Hắc Thị (chủ tiệm)','a sly hooded black-market fixer leaning on a shock baton, credit chips and stimulant vials on a neon-lit table'),
]
