"""The 18 premium cursor sets."""
from toolkit import hexc
from roles import Style, ROLES


def pal(pt, pb, ol, acc, acc2, glow, bad, plate, halo='ffffff'):
    return dict(pt=hexc(pt), pb=hexc(pb), ol=hexc(ol), acc=hexc(acc), acc2=hexc(acc2), glow=hexc(glow),
                bad=hexc(bad), plate=hexc(plate), halo=hexc(halo, 235))


def cycle(names):
    return {r: names[i % len(names)] for i, (r, _, _) in enumerate(ROLES)}


ENSEMBLE = {
    'Arrow': 'charr_tybalt', 'Help': 'asura_taimi', 'AppStarting': 'golem_blish', 'Wait': 'lich_joko',
    'Crosshair': 'sylvari_canach', 'IBeam': 'golem_blish', 'NWPen': 'asura_taimi', 'No': 'lich_joko',
    'SizeNS': 'charr_tybalt', 'SizeWE': 'sylvari_canach', 'SizeNWSE': 'golem_blish', 'SizeNESW': 'asura_taimi',
    'SizeAll': 'lich_joko', 'UpArrow': 'sylvari_canach', 'Hand': 'charr_tybalt', 'Pin': 'sylvari_canach',
    'Person': 'asura_taimi',
}

SETS = [
    # ---------------------------------------------------------------- FFXIV
    dict(franchise='FFXIV', slug='Crystal-Dawn', name='FFXIV - Crystal Dawn',
         blurb='Aether-lit crystal shards, dawn-gold trim and Eorzean sky blues.',
         style=Style(pal('f4fdff', '5aa8f0', '0a2a63', 'ffd86a', '8fe8ff', '8fe8ff', 'ff5a6a', '15306e'), 'shard', 'crystal')),
    dict(franchise='FFXIV', slug='Chocobo-Caravan', name='FFXIV - Chocobo Caravan',
         blurb='Warm gold feathers, caravan-wood brown and a very good bird.',
         style=Style(pal('fff2b0', 'e8a21e', '5a3305', 'c7452a', '8fd16a', 'ffd35a', 'd83a2a', '7a4a1c'), 'blunt', 'chocobo', rounded=1.1)),
    dict(franchise='FFXIV', slug='Void-and-Moon', name='FFXIV - Void and Moon',
         blurb='Voidgate violet, silver crescents and a moonlit magenta edge.',
         style=Style(pal('8a5ae0', '1c0a48', 'd9b3ff', 'ff6ad8', 'b78cff', 'a060ff', 'ff4a7a', '120626', 'e9d6ff'), 'sleek', 'voidmoon')),
    # ------------------------------------------------------------------ WoW
    dict(franchise='WoW', slug='Stormwind-Lionheart', name='WoW - Stormwind Lionheart',
         blurb='Alliance-blue steel, gold trim and a knight\'s heater shield.',
         style=Style(pal('7aaaff', '1f48b0', '071a4a', 'f4c542', 'ffe27a', '6aa0ff', 'e03a3a', '143384'), 'classic', 'stormwind')),
    dict(franchise='WoW', slug='Orgrimmar-Warband', name='WoW - Orgrimmar Warband',
         blurb='Horde crimson, bronze rivets and a spiked iron pauldron.',
         style=Style(pal('e8583a', '5a0d0a', '140606', 'd6a24b', 'ff8a4a', 'ff4a20', 'ffd23a', '240a08', 'ffd9a8'), 'shard', 'orgrimmar')),
    dict(franchise='WoW', slug='Frostbound-Throne', name='WoW - Frostbound Throne',
         blurb='Runeblade frost, glacier glow and Northrend ice.',
         style=Style(pal('eaf8ff', '4a9ae0', '081a44', '7fe8ff', 'b8f0ff', '7fd8ff', 'ff5a7a', '0d2250'), 'wing', 'frostbound')),
    # ----------------------------------------------------------- Goosebumps
    dict(franchise='Goosebumps', slug='Monster-Blood', name='Goosebumps - Monster Blood',
         blurb='Neon-green goo, rising bubbles and a label-purple accent.',
         style=Style(pal('c8ff6a', '2f9a14', '0a3a05', 'a64ae0', 'ffe14a', '8aff3a', 'ff3a5a', '123a0a'), 'blunt', 'monsterblood', rounded=2.0)),
    dict(franchise='Goosebumps', slug='Lawn-Gnomes', name='Goosebumps - Revenge of the Lawn Gnomes',
         blurb='Pointy red hats, glowing eyes and grass-green menace.',
         style=Style(pal('ff6a5a', 'a0121a', '2c0305', '4ac060', 'ffffff', 'ff3a2a', 'ffd23a', '1c3a14'), 'classic', 'lawngnome')),
    # ------------------------------------------------------------------ GW2
    dict(franchise='GW2', slug='Tyrian-Legends', name='GW2 - Tyrian Legends Ensemble',
         blurb='Blish, Taimi, Tybalt, Canach and Joko take turns across the full pointer set.',
         style=Style(pal('ffe9b0', 'c8782a', '3a1a05', '3ee0ff', 'ffcf5a', '3ee0ff', 'e0343a', '1c1a30'), 'wing', 'charr_tybalt', emblem_by_role=ENSEMBLE)),
    dict(franchise='GW2', slug='Blish-and-Taimi', name='GW2 - Blish and Taimi Magitech',
         blurb='Golemite cyan, asuran violet and goggle-lens glow.',
         style=Style(pal('dff9ff', '2a9ad8', '07213f', 'ff9a2a', 'c58cff', '3ee0ff', 'ff4a8a', '14183a'), 'sleek',
                     'golem_blish', emblem_by_role={r: ('golem_blish' if i % 2 == 0 else 'asura_taimi') for i, (r, _, _) in enumerate(ROLES)})),
    dict(franchise='GW2', slug='Canach-Joko-Tybalt', name='GW2 - Canach, Joko and Tybalt',
         blurb='Hooded thorns, undead gold and charr fire in a dramatic dark palette.',
         style=Style(pal('e8c46a', '3a2410', '0a0604', '43ff9a', 'ff8a2a', '43ff9a', 'ff3a3a', '100c0a', 'ffe9a8'), 'shard',
                     'sylvari_canach', emblem_by_role=cycle(['sylvari_canach', 'lich_joko', 'charr_tybalt']))),
    # -------------------------------------------------------------- Pokemon
    dict(franchise='Pokemon', slug='Kanto-Companions', name='Pokemon - Kanto Companions',
         blurb='Capture-sphere red and white with a Kanto sunshine-yellow trim.',
         style=Style(pal('ff6a5a', 'b0141c', '1a0a12', 'ffe14a', '6ac8ff', 'ff5a5a', 'ffd23a', '2a1020'), 'blunt', 'monsterball', rounded=1.0)),
    dict(franchise='Pokemon', slug='Ghost-Parade', name='Pokemon - Ghost Parade',
         blurb='Friendly lavender ghosts drifting through purple haze.',
         style=Style(pal('e8d6ff', '8a5ad0', '2a124f', 'ff7ac0', 'c9a0ff', 'b06bff', 'ff4a8a', '1a0a33'), 'blunt', 'ghostling', rounded=1.5)),
    # ------------------------------------------------------------ Simpsons
    dict(franchise='Simpsons', slug='Springfield-Donuts', name='Simpsons - Springfield Donuts',
         blurb='Springfield yellow, pink frosting and a sprinkle-covered treat.',
         style=Style(pal('ffe85a', 'f0b81a', '4a3205', 'ff4aa0', '4ac8ff', 'ffe85a', 'e0343a', '3a5aa8'), 'blunt', 'donut', rounded=1.0)),
    dict(franchise='Simpsons', slug='Nuclear-Nightshift', name='Simpsons - Nuclear Nightshift',
         blurb='Midnight power-plant greens, warning yellow and a glowing core.',
         style=Style(pal('6a9a46', '121f0c', '060a04', 'ffe14a', 'b6ff6a', '5aff3a', 'ff5a2a', '10180a', 'b6ff6a'), 'shard', 'nuclear')),
    # ------------------------------------------------------------ Cute/classic
    dict(franchise='Cute-Classic', slug='Sanrio-Friends-Remastered', name='Sanrio Friends Remastered',
         blurb='Pastel pink and sky-blue friends with ribbons and soft round pointers.',
         style=Style(pal('ffffff', 'ffc4dc', '7a3a68', 'ff6aa8', '9ad8ff', 'ffb0d0', 'ff6a8a', 'fff0f8', 'ffffff'), 'blunt', 'friend', rounded=2.2)),
    dict(franchise='Cute-Classic', slug='Strawberry-Dream-Bakery', name='Strawberry Dream Bakery',
         blurb='Cream, strawberry and leaf-green sweetness from a dream bakery.',
         style=Style(pal('fff0e0', 'ff8aa0', '7a1a3a', 'ffe08a', '9af07a', 'ffb0c0', 'e0343a', 'fff4ea'), 'blunt', 'strawberry', rounded=2.0)),
    dict(franchise='Cute-Classic', slug='Spooky-Paws', name='Spooky Paws',
         blurb='Black-cat paws, amber glow and tiny spooky sparkles.',
         style=Style(pal('6a5a8a', '14101c', '08060c', 'ff8a1a', 'c58cff', 'ff8a1a', 'ff4a3a', '120e1a', 'ff9a3a'), 'sleek', 'pawprint', rounded=1.0)),
]
