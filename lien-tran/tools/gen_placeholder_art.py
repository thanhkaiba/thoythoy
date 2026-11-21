# Vẽ hình tạm bằng code (không dùng AI): sprite pixel cho ảnh binh, Ảnh Tướng, lính phe ta,
# chân dung phe địch và tranh minh họa 9 thẻ chiến thuật.
# Dùng: python3 gen_placeholder_art.py <thư mục web/art>/   (cần Pillow)
# Muốn thay bằng tranh thật: ghi đè file cùng tên, giữ nguyên kích thước khung (288×240, 4 khung ngang).
import math, sys
from PIL import Image, ImageDraw, ImageFilter

OUT = sys.argv[1]
W, H, S = 72, 60, 4          # khung độ phân giải thấp, phóng to ×4 kiểu pixel art
FX, GY = 36, 56              # tâm bàn chân, mặt đất


def P(x, y):
    return (int(round(x)), int(round(y)))


def vec(deg, l):
    r = math.radians(deg)
    return (math.cos(r) * l, math.sin(r) * l)


SHADOW = dict(cloak=(66, 46, 108), cloak2=(44, 30, 74), trim=(132, 100, 196), void=(16, 9, 28), eye=(255, 214, 92),
              hand=(34, 22, 54), steel=(214, 200, 255), wood=(92, 70, 136), leg=(30, 20, 50), boot=(22, 14, 38),
              outline=(14, 8, 24), fx=(226, 208, 255), crest=(196, 52, 60), gold=(214, 170, 74))
BOSS = dict(SHADOW, cloak=(58, 34, 78), cloak2=(38, 22, 54), trim=(214, 170, 74), eye=(255, 84, 84), cape=(128, 34, 44),
            cape2=(92, 22, 34), steel=(240, 226, 255), fx=(255, 170, 190))


def human(tunic, tunic2):
    return dict(tunic=tunic, tunic2=tunic2, hat=(222, 188, 112), hat2=(176, 140, 72), skin=(244, 204, 164), hair=(52, 38, 30),
                steel=(228, 234, 242), wood=(126, 88, 52), leg=(70, 60, 62), boot=(48, 38, 34), outline=(40, 27, 20),
                fx=(255, 255, 255), hand=(244, 204, 164), eye=(40, 27, 20))


SQUADS = {'kiem': human((150, 44, 44), (104, 28, 32)), 'thuong': human((110, 78, 170), (74, 50, 122)),
          'cung': human((78, 140, 196), (48, 98, 150)), 'truong': human((214, 112, 150), (164, 72, 110))}

# tư thế: nghiêng người, góc tay, góc vũ khí (0 = sang phải, -90 = lên trên)
POSES = {
    'kiem': [dict(lean=0, arm=35, w=-55), dict(lean=-2, arm=-125, w=-115, stride=2), dict(lean=3, arm=5, w=38, stride=3, fx=1), dict(lean=1, arm=40, w=12, stride=2)],
    'thuong': [dict(lean=0, arm=45, w=-22), dict(lean=-2, arm=150, w=-6, stride=2), dict(lean=4, arm=0, w=0, stride=3, fx=1), dict(lean=1, arm=25, w=-10, stride=2)],
    'cung': [dict(lean=0, arm=25, w=0), dict(lean=-1, arm=0, w=0, draw=1, stride=2), dict(lean=0, arm=0, w=0, stride=2, fx=1), dict(lean=0, arm=35, w=25)],
    'truong': [dict(lean=0, arm=30, w=-82), dict(lean=-1, arm=-60, w=-98, glow=1), dict(lean=2, arm=-10, w=-48, stride=2, fx=1), dict(lean=0, arm=22, w=-72)],
}


def outline(im, col):
    px = im.load()
    edge = []
    for y in range(H):
        for x in range(W):
            if px[x, y][3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < W and 0 <= yy < H and px[xx, yy][3]:
                    edge.append((x, y))
                    break
    for x, y in edge:
        px[x, y] = col + (255,)


def weapon(d, kind, pal, hand, ang, pose, big):
    hx, hy = hand
    if kind == 'kiem':
        L = 17 if not big else 20
        bx, by = vec(ang, L)
        d.line([P(hx, hy), P(hx + bx, hy + by)], fill=pal['steel'], width=2)
        gx, gy = vec(ang + 90, 3)
        d.line([P(hx - gx, hy - gy), P(hx + gx, hy + gy)], fill=pal['gold'] if 'gold' in pal else pal['wood'], width=1)
        kx, ky = vec(ang + 180, 3)
        d.line([P(hx, hy), P(hx + kx, hy + ky)], fill=pal['wood'], width=1)
    elif kind == 'thuong':
        back, fwd = (10, 24) if not big else (12, 27)
        ax, ay = vec(ang + 180, back)
        bx, by = vec(ang, fwd)
        d.line([P(hx + ax, hy + ay), P(hx + bx, hy + by)], fill=pal['wood'], width=1)
        tx, ty = hx + bx, hy + by
        ex, ey = vec(ang, 6 if not big else 9)
        sx, sy = vec(ang + 90, 2 if not big else 4)
        if big:   # đại đao lưỡi cong
            d.polygon([P(tx, ty), P(tx + ex, ty + ey - 1), P(tx + ex * .6 + sx, ty + ey * .6 + sy + 2), P(tx - ex * .2 + sx, ty + sy)], fill=pal['steel'])
        else:
            d.polygon([P(tx - sx, ty - sy), P(tx + ex, ty + ey), P(tx + sx, ty + sy)], fill=pal['steel'])
    elif kind == 'cung':
        r = 9
        pts = [P(hx + vec(ang + a, r)[0] - vec(ang, r - 2)[0], hy + vec(ang + a, r)[1] - vec(ang, r - 2)[1]) for a in range(-75, 76, 15)]
        d.line(pts, fill=pal['wood'], width=1)
        top, bot = pts[0], pts[-1]
        if pose.get('draw'):
            nock = P(hx - 7, hy)
            d.line([top, nock, bot], fill=(pal['hat2'] if 'hat2' in pal else pal['trim']), width=1)
            d.line([nock, P(hx + 9, hy)], fill=pal['fx'], width=1)
        else:
            d.line([top, bot], fill=(pal['hat2'] if 'hat2' in pal else pal['trim']), width=1)
    else:  # trượng
        ax, ay = vec(ang + 180, 9)
        bx, by = vec(ang, 13)
        d.line([P(hx + ax, hy + ay), P(hx + bx, hy + by)], fill=pal['wood'], width=1)
        ox, oy = hx + bx, hy + by
        d.ellipse([ox - 2, oy - 2, ox + 2, oy + 2], fill=pal['fx'] if pose.get('glow') or pose.get('fx') else pal['steel'])


def effects(d, kind, pal, hand, sh, pose):
    if not pose.get('fx'):
        return
    hx, hy = hand
    fx = pal['fx']
    if kind == 'kiem':
        for i, r in enumerate((17, 18, 19)):
            d.arc([sh[0] - r, sh[1] - r, sh[0] + r + 6, sh[1] + r], start=-78 + i * 4, end=52 - i * 6, fill=fx, width=1)
    elif kind == 'thuong':
        for i, (dy, l) in enumerate(((-3, 9), (0, 12), (3, 8))):
            d.line([P(hx + 22 - l * .2, hy + dy), P(hx + 22 + l, hy + dy)], fill=fx, width=1)
    elif kind == 'cung':
        d.line([P(hx + 12, hy), P(hx + 24, hy)], fill=fx, width=1)
        d.polygon([P(hx + 24, hy - 2), P(hx + 28, hy), P(hx + 24, hy + 2)], fill=fx)
        d.line([P(hx + 4, hy - 2), P(hx + 9, hy - 2)], fill=fx, width=1)
        d.line([P(hx + 3, hy + 2), P(hx + 8, hy + 2)], fill=fx, width=1)
    else:
        ox, oy = hx + vec(pose['w'], 13)[0], hy + vec(pose['w'], 13)[1]
        d.ellipse([ox + 6, oy - 1, ox + 12, oy + 5], fill=fx)
        d.arc([ox - 5, oy - 5, ox + 5, oy + 5], 0, 360, fill=fx, width=1)
        for a in (-60, -20, 20):
            vx, vy = vec(a, 8)
            d.point(P(ox + vx, oy + vy), fill=fx)


def frame(kind, weap, pose, pal):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lean, stride = pose.get('lean', 0), pose.get('stride', 1)
    big = kind == 'boss'
    hooded = kind in ('shadow', 'captain', 'boss')
    tx = FX + lean * .5
    hr = 10 if big else 9
    hx, hy = FX + lean, GY - 29 - (2 if big else 0)
    sh = (tx + 2, GY - 19 - (1 if big else 0))
    hand = (sh[0] + vec(pose['arm'], 7)[0], sh[1] + vec(pose['arm'], 7)[1])
    # áo choàng sau lưng (tướng)
    if big:
        d.polygon([P(tx - 3, GY - 25), P(tx - 16 - lean, GY - 3), P(tx - 9, GY - 6), P(tx - 5, GY - 2), P(tx + 2, GY - 8), P(tx + 3, GY - 22)], fill=pal['cape'])
        d.polygon([P(tx - 10, GY - 12), P(tx - 16 - lean, GY - 3), P(tx - 9, GY - 6)], fill=pal['cape2'])
    # chân
    for lx in (FX - 4 - stride, FX + 1 + stride):
        d.rectangle([lx, GY - 10, lx + 2, GY - 2], fill=pal['leg'])
        d.rectangle([lx, GY - 2, lx + 4, GY - 1], fill=pal['boot'])
    # thân
    if hooded:
        w = 6 if big else 5
        d.polygon([P(tx - w, GY - 22), P(tx + w, GY - 22), P(tx + w + 3, GY - 6), P(tx + 5, GY - 9), P(tx + 2, GY - 5), P(tx - 1, GY - 9),
                   P(tx - 4, GY - 5), P(tx - w - 3, GY - 7)], fill=pal['cloak'])
        d.polygon([P(tx - w, GY - 22), P(tx - w + 3, GY - 22), P(tx - w, GY - 9), P(tx - w - 3, GY - 7)], fill=pal['cloak2'])
        d.line([P(tx - 2, GY - 21), P(tx + 4, GY - 12)], fill=pal['trim'], width=1)
        if big:
            d.rectangle([tx - 7, GY - 23, tx - 3, GY - 20], fill=pal['trim'])
            d.rectangle([tx + 3, GY - 23, tx + 7, GY - 20], fill=pal['trim'])
            d.line([P(tx - 5, GY - 13), P(tx + 6, GY - 13)], fill=pal['trim'], width=1)
    else:
        d.rectangle([tx - 5, GY - 22, tx + 5, GY - 10], fill=pal['tunic'])
        d.rectangle([tx - 5, GY - 22, tx - 3, GY - 10], fill=pal['tunic2'])
        d.polygon([P(tx - 6, GY - 11), P(tx + 6, GY - 11), P(tx + 7, GY - 7), P(tx - 7, GY - 7)], fill=pal['tunic'])
        d.line([P(tx - 5, GY - 13), P(tx + 5, GY - 13)], fill=pal['hat2'], width=1)
    # đầu
    if hooded:
        d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=pal['cloak'])
        d.pieslice([hx - hr, hy - hr, hx + hr, hy + hr], 100, 250, fill=pal['cloak2'])
        d.polygon([P(hx - hr + 2, hy - 4), P(hx - hr - 4, hy - hr + 1), P(hx - 3, hy - hr + 1)], fill=pal['cloak2'])   # chóp mũ trùm
        d.ellipse([hx - 3, hy - 4, hx + hr - 1, hy + 5], fill=pal['void'])
        for ex in (hx, hx + 4):
            d.rectangle([ex, hy - 1, ex + 1, hy + (1 if big else 0)], fill=pal['eye'])
        if kind == 'captain':
            d.arc([hx - hr - 3, hy - hr - 4, hx + 5, hy + 2], 190, 330, fill=pal['crest'], width=2)
            d.rectangle([tx - 7, GY - 23, tx - 4, GY - 21], fill=pal['gold'])
        if big:   # sừng mũ trụ
            d.line([P(hx - 6, hy - 7), P(hx - 10, hy - 12), P(hx - 9, hy - 17)], fill=pal['trim'], width=2)
            d.line([P(hx + 5, hy - 8), P(hx + 9, hy - 12), P(hx + 9, hy - 17)], fill=pal['trim'], width=2)
            d.rectangle([hx - 1, hy - hr - 1, hx + 1, hy - hr + 2], fill=pal['crest'])
    else:
        d.ellipse([hx - 8, hy - 7, hx + 8, hy + 9], fill=pal['skin'])
        d.pieslice([hx - 8, hy - 7, hx + 8, hy + 9], 95, 230, fill=pal['hair'])
        d.rectangle([hx + 3, hy + 1, hx + 3, hy + 2], fill=pal['eye'])
        d.rectangle([hx + 6, hy + 1, hx + 6, hy + 2], fill=pal['eye'])
        d.polygon([P(hx - 12, hy - 3), P(hx + 12, hy - 3), P(hx + 1, hy - 13), P(hx - 1, hy - 13)], fill=pal['hat'])   # nón lính
        d.polygon([P(hx - 12, hy - 3), P(hx - 1, hy - 13), P(hx - 3, hy - 3)], fill=pal['hat2'])
    weapon(d, weap, pal, hand, pose['w'], pose, big)
    # tay
    d.line([P(*sh), P(*hand)], fill=pal['cloak2'] if hooded else pal['tunic2'], width=3)
    d.rectangle([hand[0] - 1, hand[1] - 1, hand[0] + 1, hand[1] + 1], fill=pal['hand'])
    outline(im, pal['outline'])
    effects(ImageDraw.Draw(im), weap, pal, hand, sh, pose)
    return im


def atlas(name, kind, weap, pal):
    sheet = Image.new('RGBA', (W * 4, H), (0, 0, 0, 0))
    for i, pose in enumerate(POSES[weap]):
        sheet.paste(frame(kind, weap, pose, pal), (i * W, 0))
    sheet = sheet.resize((W * 4 * S, H * S), Image.NEAREST)
    sheet.save(OUT + name + '.webp', lossless=True, method=6)
    return sheet


def portrait(name, kind, weap, pal, bg):
    f = frame(kind, weap, POSES[weap][0], pal)
    cx, cy = FX, GY - 30
    head = f.crop((cx - 9, cy - 12, cx + 15, cy + 12)).resize((192, 192), Image.NEAREST)
    im = Image.new('RGB', (192, 192), bg)
    g = ImageDraw.Draw(im)
    for i in range(192):
        k = i / 191
        g.line([(0, i), (192, i)], fill=tuple(int(bg[j] * (1 - .35 * k)) for j in range(3)))
    im.paste(head, (0, 0), head)
    im.save(OUT + name + '.jpg', quality=90)


# ---------- tranh thẻ: vẽ ở 4× rồi thu nhỏ cho mịn ----------
CW, CH, Q = 240, 180, 4
INK = (43, 29, 20)


def card(name, bg0, bg1, paint):
    im = Image.new('RGB', (CW * Q, CH * Q))
    d = ImageDraw.Draw(im)
    for y in range(CH * Q):
        k = y / (CH * Q - 1)
        d.line([(0, y), (CW * Q, y)], fill=tuple(int(bg0[i] + (bg1[i] - bg0[i]) * k) for i in range(3)))
    paint(d, lambda *v: [x * Q for x in v], Q)
    im = im.resize((CW, CH), Image.LANCZOS)
    im.save(OUT + 'card_' + name + '.webp', quality=88, method=6)


def hills(d, q, y, col, seed):
    pts = [(0, CH * Q)]
    x = 0
    i = 0
    while x <= CW * Q:
        pts.append((x, (y + ((i * 37 + seed * 11) % 17) - (26 if i % 2 else 0)) * Q))
        x += 30 * Q
        i += 1
    pts.append((CW * Q, CH * Q))
    d.polygon(pts, fill=col)


def c_tram(d, s, q):
    d.ellipse(s(118, 24, 214, 120), fill=(246, 238, 208))
    d.ellipse(s(140, 14, 226, 100), fill=(34, 40, 78))
    hills(d, q, 150, (22, 24, 48), 1)
    d.line(s(26, 150, 210, 34), fill=(255, 255, 255), width=5 * q)
    d.line(s(40, 152, 196, 54), fill=(190, 210, 255), width=2 * q)
    for x, y in ((40, 40), (70, 70), (95, 28), (30, 96)):
        d.ellipse(s(x, y, x + 3, y + 3), fill=(246, 238, 208))


def c_loi(d, s, q):
    for x, y, w in ((20, 16, 90), (90, 6, 110), (150, 26, 80)):
        d.ellipse(s(x, y, x + w, y + 46), fill=(70, 56, 104))
    d.polygon(s(128, 30, 96, 96, 122, 96, 92, 164, 160, 80, 130, 80, 156, 30), fill=(255, 226, 96))
    d.polygon(s(128, 30, 108, 80, 124, 80, 118, 96, 122, 96, 132, 70, 118, 70, 138, 30), fill=(255, 250, 200))
    hills(d, q, 168, (30, 22, 52), 3)


def c_bang(d, s, q):
    hills(d, q, 150, (176, 208, 226), 2)
    d.line(s(36, 142, 186, 46), fill=(60, 110, 160), width=5 * q)
    d.polygon(s(186, 46, 204, 24, 214, 62), fill=(236, 250, 255))
    d.polygon(s(36, 142, 20, 138, 30, 158), fill=(60, 110, 160))
    for x, y, r in ((70, 60, 12), (150, 120, 10), (198, 100, 7), (104, 148, 6)):
        d.polygon(s(x, y - r, x + r * .5, y, x, y + r, x - r * .5, y), fill=(255, 255, 255))
        d.polygon(s(x - r, y, x, y - r * .5, x + r, y, x, y + r * .5), fill=(214, 240, 255))


def c_hoa(d, s, q):
    hills(d, q, 152, (60, 30, 50), 4)
    for x, y, r, col, c2 in ((70, 104, 30, (255, 122, 150), (255, 220, 200)), (128, 78, 38, (255, 150, 80), (255, 236, 170)), (182, 110, 26, (236, 110, 200), (255, 214, 240))):
        d.ellipse(s(x - r, y - r * .6, x + r, y + r), fill=col)
        d.polygon(s(x - r * .85, y - r * .1, x + r * .15, y - r * 1.9, x + r * .8, y - r * .2), fill=col)
        d.ellipse(s(x - r * .45, y - r * .1, x + r * .45, y + r * .75), fill=c2)


def c_khien(d, s, q):
    hills(d, q, 150, (150, 140, 120), 5)
    for i, x in enumerate((44, 100, 156)):
        d.polygon(s(x, 44, x + 44, 44, x + 44, 110, x + 22, 146, x, 110), fill=(120, 132, 150), outline=INK)
        d.polygon(s(x + 6, 50, x + 38, 50, x + 38, 108, x + 22, 136, x + 6, 108), fill=(176, 188, 204))
        d.line(s(x + 22, 50, x + 22, 136), fill=(120, 132, 150), width=3 * q)
        d.line(s(x + 6, 80, x + 38, 80), fill=(120, 132, 150), width=3 * q)
        d.ellipse(s(x + 17, 75, x + 27, 85), fill=(214, 170, 74))


def c_hanh(d, s, q):
    d.ellipse(s(160, 20, 210, 70), fill=(168, 50, 42))
    hills(d, q, 96, (150, 164, 128), 6)
    hills(d, q, 128, (122, 146, 98), 8)
    d.polygon(s(96, 180, 150, 180, 128, 120, 120, 120), fill=(226, 208, 162))
    d.polygon(s(120, 120, 128, 120, 150, 96, 146, 96), fill=(226, 208, 162))
    d.line(s(60, 150, 60, 62), fill=INK, width=3 * q)
    d.polygon(s(60, 64, 104, 76, 60, 92), fill=(46, 95, 143))
    for x, y in ((112, 168), (126, 154), (120, 140), (130, 128)):
        d.ellipse(s(x, y, x + 7, y + 5), fill=(122, 96, 60))


def c_quyet(d, s, q):
    d.ellipse(s(70, 30, 170, 130), fill=(255, 196, 96))
    d.ellipse(s(90, 50, 150, 110), fill=(255, 240, 190))
    for a, b in (((52, 150), (176, 30)), ((188, 150), (64, 30))):
        d.line([a[0] * q, a[1] * q, b[0] * q, b[1] * q], fill=(236, 240, 246), width=7 * q)
        d.line([a[0] * q, a[1] * q, (a[0] + (b[0] - a[0]) * .16) * q, (a[1] + (b[1] - a[1]) * .16) * q], fill=INK, width=9 * q)
    d.line(s(58, 118, 86, 140), fill=(214, 170, 74), width=5 * q)
    d.line(s(182, 118, 154, 140), fill=(214, 170, 74), width=5 * q)
    hills(d, q, 172, (70, 14, 14), 7)


def c_vien(d, s, q):
    hills(d, q, 120, (142, 170, 120), 9)
    hills(d, q, 146, (104, 140, 92), 2)
    for x, h, col in ((62, 86, (79, 125, 67)), (118, 104, (46, 95, 143)), (176, 80, (168, 50, 42))):
        d.line(s(x, 156, x, 156 - h), fill=INK, width=3 * q)
        d.polygon(s(x, 156 - h, x + 40, 156 - h + 6, x + 34, 156 - h + 18, x + 40, 156 - h + 32, x, 156 - h + 36), fill=col)
        d.ellipse(s(x - 5, 150, x + 5, 160), fill=INK)


def c_pha(d, s, q):
    hills(d, q, 150, (140, 128, 120), 4)
    d.rectangle(s(30, 70, 210, 160), fill=(150, 144, 136), outline=INK, width=2 * q)
    for i in range(7):
        d.rectangle(s(30 + i * 27, 54, 48 + i * 27, 72), fill=(150, 144, 136), outline=INK, width=2 * q)
    d.polygon(s(120, 70, 108, 96, 126, 110, 112, 132, 124, 160, 136, 160, 128, 132, 144, 108, 126, 94, 134, 70), fill=(40, 27, 20))
    for a in range(0, 360, 30):
        vx, vy = vec(a, 34)
        wx, wy = vec(a, 58)
        d.line(s(120 + vx, 112 + vy, 120 + wx, 112 + wy), fill=(255, 214, 92), width=3 * q)
    d.ellipse(s(102, 94, 138, 130), fill=(255, 240, 190))


sheets = []
for wp in POSES:
    sheets.append(atlas('sol_' + wp, 'soldier', wp, SQUADS[wp]))     # lính phe ta, màu áo theo từng tướng
    sheets.append(atlas('sh_' + wp, 'shadow', wp, SHADOW))           # lính ảnh binh
    sheets.append(atlas('cap_' + wp, 'captain', wp, SHADOW))         # đội trưởng ảnh binh (có ngù đỏ)
sheets.append(atlas('boss', 'boss', 'thuong', BOSS))
portrait('p_shadow', 'captain', 'kiem', SHADOW, (96, 78, 140))
portrait('p_boss', 'boss', 'thuong', BOSS, (120, 52, 60))
card('tram', (24, 28, 62), (58, 62, 112), c_tram)
card('loi', (44, 34, 78), (110, 92, 150), c_loi)
card('bang', (214, 236, 246), (150, 196, 222), c_bang)
card('hoa', (58, 30, 72), (176, 84, 96), c_hoa)
card('khien', (232, 222, 196), (196, 184, 156), c_khien)
card('hanh', (244, 234, 208), (214, 222, 190), c_hanh)
card('quyet', (150, 30, 30), (92, 16, 20), c_quyet)
card('vien', (236, 240, 214), (190, 214, 176), c_vien)
card('pha', (240, 226, 200), (206, 180, 150), c_pha)
if len(sys.argv) > 2:   # tờ xem nhanh
    sh = Image.new('RGB', (W * 4 * S, H * S * len(sheets)), (214, 196, 160))
    for i, s_ in enumerate(sheets):
        sh.paste(s_, (0, i * H * S), s_)
    sh.save(sys.argv[2])
print('ok', len(sheets), 'atlas')
