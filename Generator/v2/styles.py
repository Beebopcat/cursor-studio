"""54 style proposals: 18 sets x 3 directions (A/B/C)."""
from roles2 import Style2
from toolkit import hexc
from roles import ROLES


def P(c1, c2, ol, ac, ac2, glow, plate, bad='ff4a5a', halo='ffffff', gb=None):
    d = dict(c1=hexc(c1), c2=hexc(c2), ol=hexc(ol), ac=hexc(ac), ac2=hexc(ac2), glow=hexc(glow),
             plate=hexc(plate), bad=hexc(bad), halo=hexc(halo, 235) if halo else None)
    if gb:
        d['gb'] = gb
    return d


def alt(names):
    return {r: names[i % len(names)] for i, (r, _, _) in enumerate(ROLES)}


ENS = {'Arrow': 'charr_tybalt', 'Help': 'asura_taimi', 'AppStarting': 'golem_blish', 'Wait': 'lich_joko',
       'Crosshair': 'sylvari_canach', 'IBeam': 'golem_blish', 'NWPen': 'asura_taimi', 'No': 'lich_joko',
       'SizeNS': 'charr_tybalt', 'SizeWE': 'sylvari_canach', 'SizeNWSE': 'golem_blish', 'SizeNESW': 'asura_taimi',
       'SizeAll': 'lich_joko', 'UpArrow': 'sylvari_canach', 'Hand': 'charr_tybalt', 'Pin': 'sylvari_canach', 'Person': 'asura_taimi'}
BT = alt(['golem_blish', 'asura_taimi'])
CJT = alt(['sylvari_canach', 'lich_joko', 'charr_tybalt'])
GB = [(15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15)]

# (franchise, slug, display name, [styles])
CATALOG = []


def add(fr, slug, name, *styles):
    CATALOG.append(dict(franchise=fr, slug=slug, name=name, styles=list(styles)))


def S(key, label, blurb, pal, material, ptr, emblem, fx='glint', charm=True, ebr=None):
    return Style2(key, label, blurb, pal, material, ptr, emblem, fx, charm, ebr)


# ============================================================== FFXIV
add('FFXIV', 'Crystal-Dawn', 'FFXIV - Crystal Dawn',
    S('A', 'Aether Shard', 'The pointer itself is a cut aether crystal: hard facets, cyan core light, drifting aether motes.',
      P('eafcff', '3d8fe8', '0a2a63', 'f5d36a', '8fe8ff', '8fe8ff', '12306e'), 'facet', 'shard', 'crystal', 'motes'),
    S('B', 'Crystarium Gold', 'Eorzean UI heraldry: brushed gold bevels over deep Crystarium navy with a teal crystal inset.',
      P('ffe9a8', 'b98322', '0b1d3d', '3ee0d0', 'ffe9a8', '5ff0ff', '0e2a52'), 'metal', 'wing', 'crystal', 'glint'),
    S('C', 'Dawn Rays', 'A glowing line-light pointer in sunrise amber and dusk violet with a rotating sunburst core.',
      P('ffd9a0', 'ff9a5a', '1c0e2a', 'ffe9a0', 'ff7ab0', 'ffc070', '2a1038'), 'neon', 'sleek', 'sunburst', 'glint'))
add('FFXIV', 'Chocobo-Caravan', 'FFXIV - Chocobo Caravan',
    S('A', 'Chocobo Feather', 'The pointer is a golden chocobo feather with real barbs; a chocobo head charm flutters its crest.',
      P('fff08a', 'f0a81a', '6a3a05', 'e04a2a', '8fd16a', 'ffd35a', '7a4a1c'), 'gloss', 'feather', 'chocobo', 'motes', charm=False),
    S('B', 'Pixel Chocobo', '16-bit JRPG sprite style: hard pixels, 1px outlines and a bobbing chocobo - authentic at 32px.',
      P('fff08a', 'f0a81a', '3a1f05', 'e04a2a', '8fd16a', 'ffd35a', '7a4a1c', halo=None), 'pixel', 'blunt', 'chocobo', 'glint'),
    S('C', 'Caravan Banner', 'A die-cut sticker banner on a caravan pole with a spinning wagon wheel - warm, crafted, storybook.',
      P('ffd9a0', 'd8602a', '4a2008', 'ffd35a', '8fd16a', 'ffd35a', '7a4a1c'), 'sticker', 'banner', 'wheel', 'glint', charm='flag'))
add('FFXIV', 'Void-and-Moon', 'FFXIV - Void and Moon',
    S('A', 'Voidgate', 'Dark void body with a violet neon rim, swirling void wisps and a crescent core.',
      P('b57cff', '3a1670', '0a0418', 'ff5ad8', 'b78cff', 'c070ff', '120626'), 'neon', 'wisp', 'voidmoon', 'wisps'),
    S('B', 'Moonlit Silver', 'Polished silver-blue metal under moonlight with falling star motes.',
      P('f4f6ff', '7c8ac8', '141a40', 'c8b4ff', 'e8ecff', '9fb0ff', '1a1f4a'), 'metal', 'sleek', 'voidmoon', 'motes'),
    S('C', 'Eclipse Gel', 'Deep violet translucent gel with a magenta rim light, like glass in an eclipse.',
      P('9a5af0', '3a1280', '140640', 'ff6ad8', '7affff', 'd080ff', '1a0a3a'), 'gel', 'shard', 'voidmoon', 'wisps'))
# ================================================================ WoW
add('WoW', 'Stormwind-Lionheart', 'WoW - Stormwind Lionheart',
    S('A', 'Lionheart Blade', 'The pointer is a knight\'s longsword: steel blade, gold crossguard, sapphire pommel.',
      P('e6f0ff', '6a82b8', '0a1a44', 'f4c542', '4f8dff', '6aa0ff', '143384'), 'metal', 'sword', 'stormwind', 'glint', charm=False),
    S('B', 'Painted Alliance', 'Chunky hand-painted Warcraft look: bold cel shading, gold trim and a heraldic shield charm.',
      P('6aa0ff', '1f48b0', '071a4a', 'f4c542', 'ffe27a', '6aa0ff', '143384'), 'flat', 'wing', 'stormwind', 'glint'),
    S('C', 'Royal Banner', 'A glossy royal banner on a gold-capped pole, waving in a loop, shield crest on the cloth.',
      P('6aa0ff', '1f48b0', '071a4a', 'f4c542', 'ffe27a', '6aa0ff', '5a3a14'), 'gloss', 'banner', 'stormwind', 'glint', charm='flag'))
add('WoW', 'Orgrimmar-Warband', 'WoW - Orgrimmar Warband',
    S('A', 'Warchief Spikes', 'Rusted dark iron with riveted bronze, spiked edge and a glowing ember core.',
      P('b8b0a6', '3a302c', '120808', 'c4301c', 'd6a24b', 'ff5a20', '240a08', halo='ffd9a8'), 'metal', 'spike', 'orgrimmar', 'embers'),
    S('B', 'Forge Neon', 'Black basalt with a molten lava rim and rising embers.',
      P('ff5a20', '6a0d0a', '0e0404', 'ffb020', 'ff3a2a', 'ff5a20', '1a0606', bad='ffd23a'), 'neon', 'shard', 'orgrimmar', 'embers'),
    S('C', 'War Paint', 'Tribal ink style: black linework, crimson fills, bone-white highlights and hatching.',
      P('e04a2a', '3a0a08', '0a0505', 'f4e8d0', 'd6a24b', 'ff4a20', '1a0808', bad='ffd23a'), 'ink', 'wing', 'orgrimmar', 'embers'))
add('WoW', 'Frostbound-Throne', 'WoW - Frostbound Throne',
    S('A', 'Runeblade', 'A faceted ice runeblade as the pointer, frost sparkle and drifting snow.',
      P('eafaff', '3d90e0', '081a44', '7fe8ff', 'b8f0ff', '7fe0ff', '0d2250'), 'facet', 'sword', 'frostbound', 'snow', charm=False),
    S('B', 'Frozen Throne Neon', 'Thin ice-blue neon on black steel with a rotating rune circle.',
      P('9fe8ff', '1a4a9a', '04102a', 'b8f0ff', '5fa8ff', '7fe8ff', '06143a'), 'neon', 'wing', 'rune', 'snow'),
    S('C', 'Glacier Gel', 'Translucent glacier ice with deep blue interior and a bright top gleam.',
      P('dff6ff', '4a9ae0', '0a2a66', '7fe8ff', 'ffffff', '9fe8ff', '0d2250'), 'gel', 'shard', 'frostbound', 'snow'))
# ========================================================== Goosebumps
add('Goosebumps', 'Monster-Blood', 'Goosebumps - Monster Blood',
    S('A', 'Goo Drip', 'The pointer is a dripping blob of neon Monster Blood with rising bubbles and a glossy skin.',
      P('c8ff6a', '2f9a14', '0a3a05', 'a64ae0', 'ffe14a', '8aff3a', '123a0a', halo='e8ffc8'), 'gel', 'drip', 'monsterblood', 'bubbles', charm=False),
    S('B', 'Retro Cover Ink', 'Paperback-cover horror: black ink outlines, hatched shadows, acid green and label purple.',
      P('7dff3a', '0a4a10', '05080a', 'a64ae0', 'ffe14a', '8aff3a', '10051a'), 'ink', 'classic', 'monsterblood', 'drips'),
    S('C', 'Toxic Sticker', 'A slimy die-cut warning sticker with a bubbling goo charm.',
      P('b6f040', '3a8a10', '1a3a05', 'a64ae0', 'ffe14a', '8aff3a', '123a0a'), 'sticker', 'blunt', 'monsterblood', 'bubbles'))
add('Goosebumps', 'Lawn-Gnomes', 'Goosebumps - Revenge of the Lawn Gnomes',
    S('A', 'Pointy Hat', 'The pointer is a gnome\'s tall pointy red hat in bold cel shading; a scheming gnome charm with glinting red eyes rides along.',
      P('ff5a4a', 'a0121a', '2c0305', 'f4c542', 'ff9a8a', 'ff3a2a', '4a3014', halo='ffe9d0'), 'flat', 'hat', 'lawngnome', 'eyes'),
    S('B', 'Haunted Garden', 'Moonlit-garden neon: toxic green rim, ragged wisp pointer and glowing red gnome eyes.',
      P('6aff6a', '0a3a14', '02080a', 'ff3a3a', '6aff6a', '5aff5a', '06140c'), 'neon', 'wisp', 'lawngnome', 'eyes'),
    S('C', 'Garden Sticker', 'A bright garden-centre sticker with a tiny scheming gnome charm.',
      P('ff6a5a', 'b0161c', '2c0305', '4ac060', 'ffffff', 'ff3a2a', '1c3a14'), 'sticker', 'blunt', 'lawngnome', 'glint'))
# ================================================================ GW2
add('GW2', 'Tyrian-Legends', 'GW2 - Tyrian Legends Ensemble',
    S('A', 'Legion Crest', 'Bronze-and-cyan heraldic metalwork; Tybalt, Taimi, Blish, Canach and Joko take turns across roles.',
      P('ffe9b0', 'b8742a', '2a1405', '3ee0ff', 'ffcf5a', '3ee0ff', '1c1a30'), 'metal', 'wing', 'charr_tybalt', 'glint', ebr=ENS),
    S('B', 'Storybook Heroes', 'Painted parchment-and-ink adventure look with a hero\'s sword pointer and dancing sparkles.',
      P('f4e2b8', 'c08a48', '3a2005', 'c4301c', '3ee0ff', 'ffd35a', '3a2a1a'), 'flat', 'sword', 'charr_tybalt', 'motes', charm=False, ebr=ENS),
    S('C', 'Pixel Heroes', 'Retro pixel-art party: all five heroes as crisp 32px sprites.',
      P('ffe9b0', 'c08a48', '2a1405', '3ee0ff', 'ffcf5a', '3ee0ff', '1c1a30', halo=None), 'pixel', 'classic', 'charr_tybalt', 'glint', ebr=ENS))
add('GW2', 'Blish-and-Taimi', 'GW2 - Blish and Taimi Magitech',
    S('A', 'Magitech Blueprint', 'Cyan schematic neon on deep navy: a tesla-wand pointer with orbiting energy motes.',
      P('3ee0ff', '0a3a6a', '02101e', 'ff9a2a', 'c58cff', '3ee0ff', '04182e'), 'neon', 'wand', 'golem_blish', 'motes', charm=False, ebr=BT),
    S('B', 'Golemite Brass', 'Riveted brass golem plating with glowing cyan cores and a spinning gear.',
      P('f0c88a', '8a5a2a', '2a1405', '3ee0ff', 'ff9a2a', '3ee0ff', '1a2a3a'), 'metal', 'blunt', 'gear', 'glint', ebr=alt(['gear', 'golem_blish', 'asura_taimi'])),
    S('C', 'Asura Gel', 'Violet-and-cyan glossy gel with Taimi\'s goggles and Blish\'s glowing golem face.',
      P('d9b6ff', '6a3ac8', '1c0a44', '3ee0ff', '7be7ff', 'c58cff', '241450'), 'gel', 'sleek', 'asura_taimi', 'motes', ebr=alt(['asura_taimi', 'golem_blish'])))
add('GW2', 'Canach-Joko-Tybalt', 'GW2 - Canach, Joko and Tybalt',
    S('A', 'Gilded Dark', 'Black-and-gold dramatic metal, a duelist\'s dagger pointer, three emblems in rotation.',
      P('e8c46a', '3a2410', '0a0604', '43ff9a', 'ff8a2a', '43ff9a', '100c0a', halo='ffe9a8'), 'metal', 'dagger', 'sylvari_canach', 'glint', charm=False, ebr=CJT),
    S('B', 'Spectral Flame', 'Joko\'s necrotic green flame: neon rim, ghostly wisp pointer, golden headdress core.',
      P('43ff9a', '0a3a24', '020a06', 'ffe27a', '43ff9a', '43ff9a', '06140c'), 'neon', 'wisp', 'lich_joko', 'wisps'),
    S('C', 'Duelist Ink', 'Comic-ink drama: heavy blacks, ember orange, hatching and a leaf-blade pointer.',
      P('f0e0c0', '6a2a10', '0a0505', 'ff6a1a', '43ff9a', 'ff8a2a', '140a06'), 'ink', 'leaf', 'charr_tybalt', 'embers', charm=False, ebr=CJT))
# ============================================================== Pokemon
add('Pokemon', 'Kanto-Companions', 'Pokemon - Kanto Companions',
    S('A', 'Capture Gloss', 'High-gloss capture-sphere red and white with a blinking button core.',
      P('ff6a5a', 'b0141c', '1a0a12', 'ffe14a', '6ac8ff', 'ff5a5a', '2a1020', bad='ffd23a'), 'gloss', 'blunt', 'monsterball', 'glint'),
    S('B', 'Pocket Monochrome', 'Four-shade handheld green pixel art - the original 1996 look.',
      P('9bbc0f', '306230', '0f380f', '8bac0f', '9bbc0f', '8bac0f', '0f380f', halo=None, gb=GB), 'pixel', 'classic', 'monsterball', 'glint'),
    S('C', 'Dex Sticker', 'A clean white die-cut sticker with red-blue trainer accents.',
      P('ffffff', 'd6dae8', '1a0a12', 'e03a3a', '3a6ae0', 'ff5a5a', '2a1020'), 'sticker', 'classic', 'monsterball', 'glint'))
add('Pokemon', 'Ghost-Parade', 'Pokemon - Ghost Parade',
    S('A', 'Haunting Gas', 'Violet gas-cloud neon with drifting purple wisps and a smiling ghost core.',
      P('b06bff', '3a1270', '0c0420', 'ff7ac0', 'c9a0ff', 'b06bff', '160a30'), 'neon', 'wisp', 'ghostling', 'wisps'),
    S('B', 'Pixel Ghost', 'Sprite-style purple pixel ghost with a hovering tail.',
      P('d9b6ff', '7a40c8', '1c0a44', 'ff7ac0', 'c9a0ff', 'b06bff', '160a30', halo=None), 'pixel', 'wisp', 'ghostling', 'motes'),
    S('C', 'Plush Ghost', 'Soft lavender sticker with a rounded wisp hem and a cheeky ghost charm.',
      P('f4ecff', 'b9a2ea', '3a1c70', 'ff7ac0', 'c9a0ff', 'b06bff', '1a0a33'), 'sticker', 'wisp', 'ghostling', 'motes'))
# ============================================================== Simpsons
add('Simpsons', 'Springfield-Donuts', 'Simpsons - Springfield Donuts',
    S('A', 'Cel Yellow', 'Show-faithful flat colour: Springfield yellow, thick black outlines, no gradients.',
      P('ffd90f', 'f0a010', '14100a', 'ff4aa0', '4ac8ff', 'ffd90f', '3a5aa8'), 'flat', 'blunt', 'donut', 'glint'),
    S('B', 'Frosted Gloss', 'Glossy pink-frosting candy shine with sprinkle motes.',
      P('ffb0dc', 'e0408e', '7a1450', 'ffd90f', '4ac8ff', 'ff9ad0', '3a5aa8'), 'gloss', 'drip', 'donut', 'motes', charm=False),
    S('C', 'Arcade Donut', '16-bit arcade-cabinet pixels in yellow and pink.',
      P('ffd90f', 'f0a010', '14100a', 'ff4aa0', '4ac8ff', 'ffd90f', '3a5aa8', halo=None), 'pixel', 'classic', 'donut', 'glint'))
add('Simpsons', 'Nuclear-Nightshift', 'Simpsons - Nuclear Nightshift',
    S('A', 'Cel Meltdown', 'Flat show-style green glow, warning yellow trim and a radiation core.',
      P('b6ff4a', '3a8a10', '0a1405', 'ffe14a', '5aff3a', '5aff3a', '10180a'), 'flat', 'shard', 'nuclear', 'glint'),
    S('B', 'Glow Rod', 'Neon green control-rod pointer with orbiting glow motes at night.',
      P('5aff3a', '0a4a10', '020a02', 'ffe14a', 'b6ff6a', '5aff3a', '10180a', bad='ff5a2a'), 'neon', 'wand', 'nuclear', 'motes', charm=False),
    S('C', 'Toxic Gel', 'Dripping translucent green sludge with floating bubbles.',
      P('b6ff4a', '2a8a1a', '0a2a05', 'ffe14a', '5aff3a', '5aff3a', '10180a'), 'gel', 'drip', 'nuclear', 'bubbles', charm=False))
# ================================================================= Cute
add('Cute-Classic', 'Sanrio-Friends-Remastered', 'Sanrio Friends Remastered',
    S('A', 'Pastel Sticker', 'Soft pink die-cut sticker pointer with a ribbon-bunny friend charm.',
      P('ffffff', 'ffc4dc', '7a3a68', 'ff6aa8', '9ad8ff', 'ffb0d0', 'fff0f8'), 'sticker', 'blunt', 'friend', 'motes'),
    S('B', 'Candy Gel', 'Glossy candy-gel pointer in pink and sky blue with floating bubbles.',
      P('ffd0e4', 'ff7ab8', '8a2a68', '9ad8ff', 'fff2a0', 'ffb0d0', 'fff0f8', halo='ffffff'), 'gel', 'drip', 'friend', 'bubbles', charm=False),
    S('C', 'Pixel Kawaii', 'Pastel pixel-art friends - 90s handheld-pet style.',
      P('ffffff', 'ffc4dc', '7a3a68', 'ff6aa8', '9ad8ff', 'ffb0d0', 'fff0f8', halo=None), 'pixel', 'classic', 'friend', 'motes'))
add('Cute-Classic', 'Strawberry-Dream-Bakery', 'Strawberry Dream Bakery',
    S('A', 'Berry Sticker', 'Cream-and-strawberry die-cut sticker with a sparkly berry charm.',
      P('fff0e0', 'ff8aa0', '7a1a3a', 'ffe08a', '9af07a', 'ffb0c0', 'fff4ea'), 'sticker', 'blunt', 'strawberry', 'motes'),
    S('B', 'Cream Drip', 'Glossy strawberry cream with a drippy edge and berry core.',
      P('fff0e8', 'ff7a96', '7a1a3a', 'ffe08a', '9af07a', 'ffb0c0', 'fff4ea', halo='ffffff'), 'gloss', 'drip', 'strawberry', 'drips', charm=False),
    S('C', 'Doodle Flat', 'Playful flat doodle: bold outlines, two-tone fills, cut-paper charm.',
      P('ffd0d8', 'ff6a86', '5a1030', 'ffe08a', '9af07a', 'ffb0c0', 'fff4ea'), 'flat', 'classic', 'strawberry', 'motes'))
add('Cute-Classic', 'Spooky-Paws', 'Spooky Paws',
    S('A', 'Black Cat Flat', 'Flat black-cat silhouettes with amber outline, purple paw beans and glinting eyes.',
      P('5a4a78', '15151f', '08060c', 'ff8a1a', 'c58cff', 'ff8a1a', '120e1a', halo='ff9a3a'), 'flat', 'sleek', 'pawprint', 'eyes'),
    S('B', 'Pumpkin Neon', 'Jack-o\'-lantern orange neon on midnight black with floating embers.',
      P('ff8a1a', '5a2a0a', '06040a', 'ffd35a', 'c58cff', 'ff8a1a', '120e1a'), 'neon', 'wisp', 'pumpkin', 'embers'),
    S('C', 'Moonlit Sticker', 'Purple-night sticker with a glowing pumpkin charm and star motes.',
      P('b89cff', '5a3aa8', '1c0a44', 'ff8a1a', 'ffd35a', 'ff8a1a', '120e1a'), 'sticker', 'blunt', 'pumpkin', 'motes'))
