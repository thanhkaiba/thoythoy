"""Sinh danh sách job video (ra đòn có đạn theo vũ khí, và trúng đòn) cho mọi lá, xếp lá hiếm trước.

Dùng:  python3 vid_jobs.py <cardlist.json> > vid_jobs.json
cardlist.json lấy từ game: [{"id","r","w"}...]. Mô tả nhân vật lấy từ cards_v4.py.
"""
import json, sys
from cards_v4 import CARDS as V4

DESC = {c[0]: c[5].split(',')[0] for c in V4}
SHOT = {
 'laser': 'charges a blinding glow and fires a rapid barrage of bright laser bolts to the right with muzzle flashes and recoil, the glowing bolts streak out of the frame to the right',
 'electric': 'crackles with electricity, gathers a ball of lightning and hurls it to the right together with forked arcs of chain lightning that shoot out of the frame to the right',
 'plasma': 'charges its core and fires glowing plasma orbs to the right with a bright recoil flash, the orbs fly out of the frame to the right',
 'flame': 'rears back and unleashes a roaring stream of fire and blazing fireballs to the right, the fireballs fly out of the frame to the right',
 'missile': 'opens hidden hatches and launches a salvo of small missiles with smoke trails that fly out of the frame to the right',
 'sonic': 'rears back and blasts powerful glowing sonic shockwave rings to the right, the rings expand and fly out of the frame to the right',
 'cryo': 'fires a freezing frost blast and sharp ice shards to the right, the shards fly out of the frame to the right',
 'toxic': 'spits several glowing globs of toxic acid sludge to the right, the globs arc out of the frame to the right',
 'claw': 'lunges and slashes the air with its claws, releasing three glowing claw-shaped energy slashes that fly out of the frame to the right',
 'bite': 'lunges and snaps its jaws, launching a glowing crescent energy shockwave that flies out of the frame to the right',
 'blade': 'swings its blade in a powerful arc, releasing a glowing crescent energy slash that flies out of the frame to the right',
 'hammer': 'charges forward and slams with full force, sending a glowing energy shockwave and flying debris blasting out of the frame to the right',
}
TAIL = (' Then it returns to its exact original pose. Dynamic, powerful, dramatic action with bright glowing effects. Static locked-off camera, '
        'the solid flat green background stays completely unchanged, no ground, no shadows, no other creatures, the whole character stays inside the frame.')

if __name__ == '__main__':
    cards = sorted(json.load(open(sys.argv[1])), key=lambda c: (-c['r'], c['id']))
    jobs = []
    for c in cards:
        s = DESC.get(c['id'], 'the mechanical creature').strip()
        S = 'The ' + (s[2:] if s.startswith('a ') else s[3:] if s.startswith('an ') else s)
        jobs.append({'name': c['id'] + '_atk', 'id': c['id'], 'seed': 11, 'prompt': f"{S} {SHOT.get(c['w'], SHOT['plasma'])}.{TAIL}"})
        jobs.append({'name': c['id'] + '_hit', 'id': c['id'], 'prompt': f"{S} is struck hard from the right by an energy blast, recoils backward and staggers, sparks and debris fly from its armour, then it regains its balance.{TAIL}"})
    print(json.dumps(jobs, ensure_ascii=False, indent=1))
