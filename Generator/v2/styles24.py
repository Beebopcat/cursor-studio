"""The 24-set roster x 4 styles (A relic/weapon, B mascot, C HUD/gauntlet/pixel, C2 extra Style C).

Concept names for A/B/C follow the Gemini 'Cursor Studio' proposal the user approved; C2 is the added Style C variant.
"""
from roles2 import Style2
from styles import P, GB
from roles import ROLES

PAL = dict(
    crystal=P('eafcff', '3d8fe8', '0a2a63', 'f5d36a', '8fe8ff', '8fe8ff', '12306e'),
    crystalgold=P('ffe9a8', 'b98322', '0b1d3d', '3ee0d0', 'ffe9a8', '5ff0ff', '0e2a52'),
    steel=P('eef3fa', '7a8aa8', '0a1430', '5ff0ff', 'f5d36a', '8fe8ff', '1a2440'),
    choco=P('fff08a', 'f0a81a', '5a3305', 'c7452a', '8fd16a', 'ffd35a', '7a4a1c'),
    leather=P('d9a070', '6a3a14', '2a1405', 'ffd35a', 'c7452a', 'ffd35a', '3a2010'),
    void=P('b57cff', '3a1670', '0a0418', 'ff5ad8', 'b78cff', 'c070ff', '120626'),
    obsidian=P('7a6a9a', '1a1028', '05020c', 'f5d36a', 'b57cff', 'c070ff', '120626', halo='e0c8ff'),
    ruby=P('ff8a6a', 'a0141a', '2a0305', 'ffd35a', 'ff9a3a', 'ff5a20', '2a0a08'),
    iron=P('8a8a96', '25252e', '0a0a0e', 'ff8a2a', 'ffd35a', 'ff6a1a', '1a1414', halo='ffd9a8'),
    frost=P('eafaff', '3d90e0', '081a44', '7fe8ff', 'b8f0ff', '7fe0ff', '0d2250'),
    saronite=P('6a8aa8', '182838', '04080f', '7fe8ff', 'b8f0ff', '5ad8ff', '0a1424', halo='bfefff'),
    holy=P('fff4c8', 'd8a22a', '3a2405', 'ffffff', 'ffe27a', 'ffe27a', '5a3a14'),
    silver=P('f4f6ff', '8a96b8', '141a40', 'f5d36a', '4f8dff', 'ffe27a', '1a2a5a'),
    arcane=P('e8d0ff', '7a3ad8', '1a0533', 'f5d36a', '5aff7a', 'c070ff', '1a0a3a'),
    slime=P('c8ff6a', '2f9a14', '0a3a05', 'a64ae0', 'ffe14a', '8aff3a', '123a0a', halo='e8ffc8'),
    gnome=P('ff5a4a', 'a0121a', '2c0305', 'f4c542', 'ff9ac0', 'ff3a2a', '1c3a14', halo='ffe9d0'),
    golem=P('f4ecd8', 'a08860', '2a1a08', '3ee0ff', 'f5d36a', '3ee0ff', '1a2a3a'),
    charr=P('ffb257', 'b8500c', '3a1405', 'e04a2a', 'ffd35a', 'ff8a2a', '2a1408'),
    taimi=P('7af0e0', '1a8a8a', '052a2a', 'ff5ad0', 'c58cff', '3ee0ff', '0a2030'),
    sylvari=P('9cf0a8', '1f7a3a', '04170c', 'f5d36a', 'c8ff9a', '5aff7a', '0a2a14'),
    joko=P('ffe27a', 'b07a14', '3a2005', '43ff9a', '2a5fc8', '43ff9a', '1a1408'),
    prism=P('ff8a6a', 'b0141c', '2a0305', 'ffd35a', '6ac8ff', 'ff6a3a', '1c1a30'),
    magitech=P('3ee0ff', '0a3a6a', '02101e', 'ff5ad0', 'c58cff', '3ee0ff', '04182e'),
    drama=P('e8c46a', '3a2410', '0a0604', '43ff9a', 'ff8a2a', '43ff9a', '100c0a', halo='ffe9a8'),
    pika=P('fff08a', 'f0b800', '3a2400', 'e03a3a', '8a4a1a', 'ffe14a', '2a1020'),
    ghost=P('c9a0ff', '5a2ab0', '12052a', 'ff5a7a', 'c9a0ff', 'b06bff', '160a30'),
    simp=P('ffd90f', 'f0a010', '14100a', 'ff4aa0', '4ac8ff', 'ffd90f', '3a5aa8'),
    nuke=P('b6ff4a', '3a8a10', '0a1405', 'ffe14a', 'ff9a3a', '5aff3a', '10180a'),
    pastel=P('ffffff', 'ffc4dc', '7a3a68', 'ff6aa8', '9ad8ff', 'ffb0d0', 'fff0f8'),
    berry=P('fff0e0', 'ff8aa0', '7a1a3a', 'ffe08a', '9af07a', 'ffb0c0', 'fff4ea'),
    spooky=P('5a4a78', '15151f', '08060c', 'ff8a1a', 'c58cff', 'ff8a1a', '120e1a', halo='ff9a3a'),
)


def px(name, **over):
    p = dict(PAL[name])
    p['halo'] = None
    p.update(over)
    return p


def E(main, busy=None, extra=None):
    m = {'Wait': busy or main, 'Pin': busy or main, 'SizeAll': busy or main}
    if extra:
        m.update(extra)
    return m


def cyc(names):
    return {r: names[i % len(names)] for i, (r, _, _) in enumerate(ROLES)}


SETS24 = []


def add(num, group, slug, name, *styles):
    SETS24.append(dict(num=num, group=group, slug=f'{num:02d}-{slug}', name=name, styles=list(styles)))


def S(key, label, blurb, pal, material, ptr, emblem, fx='glint', charm=True, ebr=None):
    return Style2(key, label, blurb, pal, material, ptr, emblem, fx, charm, ebr)


# ---------------------------------------------------------------- FFXIV
add(1, 'FFXIV', 'Crystal-Dawn', 'FFXIV - Crystal Dawn',
    S('A', 'Aetherial Glaive Relic', 'Gold-filigree glaive with a cyan crystal spearhead and a shimmering blade sweep.', PAL['crystalgold'], 'metal', 'glaive', 'crystal', 'motes', False, E('crystal', 'mothercrystal')),
    S('B', 'Floating Mothercrystal', 'The Mothercrystal cluster rides your pointer with orbiting aether shards and a pulsing core.', PAL['crystal'], 'facet', 'mini', 'mothercrystal', 'motes', 'mascot'),
    S('C', 'Eorzean Silver Gauntlet', 'Armored paladin gauntlet pointer with a glowing cyan fingertip aura.', PAL['steel'], 'metal', 'gauntlet', 'crystal', 'motes', False),
    S('C2', 'Crystal HUD Pixel', '16-bit Eorzean menu-cursor pixel art with a blinking aether crystal.', px('crystal'), 'pixel', 'classic', 'crystal', 'glint'))
add(2, 'FFXIV', 'Chocobo-Caravan', 'FFXIV - Chocobo Caravan',
    S('A', 'Golden Plume Blade', 'Feathered bronze-and-gold pointer with a glowing amber gem.', PAL['choco'], 'gloss', 'feather', 'chocobo', 'motes', False, E('chocobo', 'wheel')),
    S('B', 'Chocobo Mascot', 'A bare-headed golden chocobo (no hat) bobbing beside your pointer, crest feathers fluttering.', PAL['choco'], 'gloss', 'mini', 'chocobo', 'motes', 'mascot', E('chocobo', 'chocobo')),
    S('C', 'Caravan Tack Gauntlet', 'Studded leather bracer gauntlet with a golden chocobo emblem.', PAL['leather'], 'metal', 'gauntlet', 'chocobo', 'glint', False, E('chocobo', 'wheel')),
    S('C2', 'Pixel Chocobo Caravan', '16-bit JRPG sprites: a hatless pixel chocobo and a rolling caravan wheel.', px('choco'), 'pixel', 'blunt', 'chocobo', 'glint', True, E('chocobo', 'wheel')))
add(3, 'FFXIV', 'Void-and-Moon', 'FFXIV - Void and Moon',
    S('A', 'Abyssal Voidblade', 'Obsidian-and-gold reaper dagger infused with pulsing purple voidlight.', PAL['obsidian'], 'metal', 'dagger', 'voidmoon', 'wisps', False),
    S('B', 'Lunar Eclipse Avatar', 'A grinning purple crescent moon with a glowing crimson void eye.', PAL['void'], 'gloss', 'mini', 'moonface', 'wisps', 'mascot', E('moonface', 'moonface')),
    S('C', 'Arcane Void Reticle', 'Rotating runic spell circle with a violet target spear in neon HUD light.', PAL['void'], 'neon', 'spear', 'rune', 'wisps', False, E('rune', 'voidmoon')),
    S('C2', 'Void Pixel', 'Retro pixel crescent and void-gate sprites in deep violet.', px('void'), 'pixel', 'wisp', 'voidmoon', 'glint'))
add(4, 'FFXIV', 'A-Realm-Reborn', 'FFXIV - A Realm Reborn',
    S('A', 'Bahamut Crimson Relic', 'Ornate gold-and-ruby relic sword radiating Calamity flare embers.', PAL['ruby'], 'metal', 'greatsword', 'meteor', 'embers', False),
    S('B', 'Blazing Dalamud Meteor', 'The descending crimson moon Dalamud with an animated flame trail.', PAL['ruby'], 'gloss', 'mini', 'meteor', 'embers', 'mascot'),
    S('C', 'Meteor Sigil Gauntlet', 'Black-iron Grand Company gauntlet projecting a glowing orange target rune.', PAL['iron'], 'metal', 'gauntlet', 'meteor', 'embers', False, E('meteor', 'rune')),
    S('C2', 'Calamity Pixel', 'Pixel-art falling meteor and ember sprites, Eorzea 1.0 style.', px('ruby'), 'pixel', 'shard', 'meteor', 'embers'))
# ------------------------------------------------------------------ WoW
add(5, 'WoW', 'Frostmourne-Icecrown', 'WoW - Frostmourne Icecrown',
    S('A', 'Frostmourne Runeblade', 'Runeblade with a horned skull guard, glowing runes and icy mist.', PAL['frost'], 'facet', 'runeblade', 'frostbound', 'snow', False, E('frostbound', 'helm')),
    S('B', 'Helm of Domination', 'The crown of the Lich King with blazing blue eyes in a blizzard swirl.', PAL['saronite'], 'metal', 'mini', 'helm', 'snow', 'mascot', E('helm', 'helm')),
    S('C', 'Icecrown War-Gauntlet', 'Spiked saronite death-knight gauntlet etched with frost runes.', PAL['saronite'], 'metal', 'gauntlet', 'rune', 'snow', False, E('rune', 'helm')),
    S('C2', 'Frozen Throne HUD', 'Ice-blue neon interface pointer with a rotating rune circle.', PAL['frost'], 'neon', 'wing', 'rune', 'snow', True, E('rune', 'helm')))
add(6, 'WoW', 'Ashbringer-Silver-Hand', 'WoW - Ashbringer and Silver Hand',
    S('A', 'Radiant Ashbringer', 'Golden greatsword with a levitating Holy Light orb and spark trail.', PAL['holy'], 'metal', 'greatsword', 'holyorb', 'motes', False, E('holyorb', 'hearthstone')),
    S('B', 'Swirling Hearthstone', 'Golden-framed hearthstone with a rotating azure portal spiral.', PAL['silver'], 'gloss', 'mini', 'hearthstone', 'motes', 'mascot', E('hearthstone', 'hearthstone')),
    S('C', 'Silver Hand Gauntlet', 'Gold paladin plate gauntlet with glowing holy runes.', PAL['holy'], 'metal', 'gauntlet', 'holyorb', 'motes', False, E('stormwind', 'holyorb')),
    S('C2', 'Light HUD Pixel', 'Pixel-art holy sword and hearthstone sprites.', px('holy'), 'pixel', 'sword', 'holyorb', 'glint', False, E('holyorb', 'hearthstone')))
add(7, 'WoW', 'Dalaran-Arcane-Emerald-Dream', 'WoW - Dalaran Arcane and Emerald Dream',
    S('A', 'Kirin Tor Crystal Blade', 'Floating violet arcane crystal sword with orbiting mana shards.', PAL['arcane'], 'facet', 'sword', 'vcrystal', 'motes', False, E('vcrystal', 'eyevines')),
    S('B', 'Eye of Dalaran and Dream', 'Golden Kirin Tor eye wrapped in glowing Emerald Dream vines.', PAL['arcane'], 'gloss', 'mini', 'eyevines', 'motes', 'mascot', E('eyevines', 'eyevines')),
    S('C', 'Archmage Runic Gauntlet', 'Violet-and-gold gauntlet traced with living emerald filigree.', PAL['arcane'], 'metal', 'gauntlet', 'eyevines', 'motes', False, E('vcrystal', 'eyevines')),
    S('C2', 'Arcane Neon Sigil', 'Violet neon spell-HUD pointer with a turning rune sigil.', PAL['arcane'], 'neon', 'sleek', 'rune', 'motes', True, E('rune', 'eyevines')))
# ----------------------------------------------------------- Goosebumps
add(8, 'Goosebumps', 'Monster-Blood', 'Goosebumps - Monster Blood',
    S('A', 'Glossy Slime and Canister', 'Translucent oozing green Monster Blood pointer and a purple canister.', PAL['slime'], 'gel', 'drip', 'canister', 'bubbles', False, E('monsterblood', 'canister')),
    S('B', 'Living Slime Mascot', 'A bubbling green slime creature with a hazard-canister spinner.', PAL['slime'], 'gloss', 'mini', 'monsterblood', 'bubbles', 'mascot', E('monsterblood', 'canister')),
    S('C', 'Retro 16-Bit Neon Pixel', 'Crisp 90s arcade pixel art: a dripping neon-green pointer and a purple tub.', px('slime'), 'pixel', 'drip', 'canister', 'drips', False, E('monsterblood', 'canister')),
    S('C2', 'Paperback Cover Ink', 'Book-cover horror ink: black outlines, hatching, acid green and label purple.', P('7dff3a', '0a4a10', '05080a', 'a64ae0', 'ffe14a', '8aff3a', '10051a'), 'ink', 'classic', 'monsterblood', 'drips', True, E('monsterblood', 'canister')))
add(9, 'Goosebumps', 'Lawn-Gnomes', 'Goosebumps - Revenge of the Lawn Gnomes',
    S('A', 'Ceramic Gnome and Flamingo', 'Glazed red-cap gnome hat pointer with a glossy pink lawn flamingo.', PAL['gnome'], 'gloss', 'hat', 'lawngnome', 'eyes', True, E('lawngnome', 'flamingo')),
    S('B', 'Sinister Gnome Mascot', 'A grinning yellow-eyed mischief gnome with a startled flamingo spinner.', PAL['gnome'], 'flat', 'mini', 'lawngnome', 'eyes', 'mascot', E('lawngnome', 'flamingo')),
    S('C', 'Retro 16-Bit Pixel Gnome', 'Neon-outlined pixel-art lawn gnome and pink flamingo.', px('gnome'), 'pixel', 'classic', 'lawngnome', 'eyes', True, E('lawngnome', 'flamingo')),
    S('C2', 'Haunted Garden Neon', 'Moonlit-garden neon with glowing red gnome eyes.', P('6aff6a', '0a3a14', '02080a', 'ff3a3a', '6aff6a', '5aff5a', '06140c'), 'neon', 'wisp', 'lawngnome', 'eyes', True, E('lawngnome', 'flamingo')))
# ----------------------------------------------------------------- GW2
add(10, 'GW2', 'Blish', 'GW2 - Blish (Golemite)',
    S('A', 'Golem Chassis Spear', 'Blish\'s ivory-and-gold golem plating with a glowing cyan spearhead.', PAL['golem'], 'metal', 'glaive', 'golemhead', 'motes', False),
    S('B', 'Hovering Blish Optic', 'Blish\'s round golem head with a scanning cyan visor beside a hardlight arrow.', PAL['golem'], 'gloss', 'mini', 'golemhead', 'motes', 'mascot'),
    S('C', 'Painterly Hardlight Chevron', 'Painterly cyan-and-gold brushstroke chevron with asuran glyphs.', PAL['golem'], 'paint', 'brush', 'golemhead', 'motes', False),
    S('C2', 'Golemite Pixel', 'Pixel-art golem optic and gear sprites.', px('golem'), 'pixel', 'blunt', 'golemhead', 'glint', True, E('golemhead', 'gear')))
add(11, 'GW2', 'Tybalt-Leftpaw', 'GW2 - Tybalt Leftpaw',
    S('A', 'Lightbringer Crest and Dagger', 'Tybalt\'s charr crest under a winged Order of Whispers dagger.', PAL['charr'], 'metal', 'dagger', 'charr_tybalt', 'glint', False, E('charr_tybalt', 'wingdagger')),
    S('B', 'Bitten Cider Apple and Paw', 'A glossy bitten cider apple with Tybalt\'s charr paw.', PAL['charr'], 'gloss', 'mini', 'apple', 'motes', 'mascot', E('charrpaw', 'apple')),
    S('C', 'Painterly Clockwork Stroke', 'A fiery amber brushstroke arrow driven by interlocking gears.', PAL['charr'], 'paint', 'brush', 'gear', 'embers', False, E('charr_tybalt', 'gear')),
    S('C2', 'Charr Pixel', 'Pixel-art Tybalt head, apple and paw sprites.', px('charr'), 'pixel', 'classic', 'charr_tybalt', 'glint', True, E('charr_tybalt', 'apple')))
add(12, 'GW2', 'Taimi-and-Scruffy', 'GW2 - Taimi and Scruffy 2.0',
    S('A', 'Scruffy Mech and Holo-Bow Spear', 'Teal-and-pink Scruffy 2.0 under Taimi\'s neon spear tip.', PAL['taimi'], 'metal', 'spear', 'scruffy', 'motes', False, E('asura_taimi', 'scruffy')),
    S('B', 'Chibi Taimi and Scruffy', 'Expressive Taimi mascot beside your pointer, Scruffy as the spinner.', PAL['taimi'], 'gloss', 'mini', 'asura_taimi', 'motes', 'mascot', E('asura_taimi', 'scruffy')),
    S('C', 'Neon Hardlight Bow', 'Magenta-and-cyan asuran hologram emitter projecting a laser pointer.', PAL['magitech'], 'neon', 'emitter', 'scruffy', 'motes', False, E('asura_taimi', 'scruffy')),
    S('C2', 'Taimi Pixel', 'Pixel-art Taimi and Scruffy sprites.', px('taimi'), 'pixel', 'blunt', 'asura_taimi', 'glint', True, E('asura_taimi', 'scruffy')))
add(13, 'GW2', 'Canach', 'GW2 - Canach',
    S('A', 'Bioluminescent Vine Spear', 'Thorny emerald sylvari spear glowing with green sap and spores.', PAL['sylvari'], 'facet', 'spear', 'sylvari_canach', 'motes', False, E('sylvari_canach', 'blossom')),
    S('B', 'Jungle Blossom Bomb', 'Canach\'s bioluminescent golden-emerald blossom bomb with a lit fuse.', PAL['sylvari'], 'gloss', 'mini', 'blossom', 'motes', 'mascot', E('sylvari_canach', 'blossom')),
    S('C', 'Mercenary Shield-Dagger', 'Ironwood-and-brass shield-dagger with a thorny emerald blade.', PAL['sylvari'], 'metal', 'dagger', 'sylvari_canach', 'glint', False, E('sylvari_canach', 'blossom')),
    S('C2', 'Sylvari Pixel', 'Pixel-art leaf blade and blossom bomb.', px('sylvari'), 'pixel', 'leaf', 'blossom', 'glint', False, E('sylvari_canach', 'blossom')))
add(14, 'GW2', 'Palawa-Joko', 'GW2 - Palawa Joko',
    S('A', 'Awakened Crescent Staff', 'Golden crescent scepter wreathed in necrotic green soulfire.', PAL['joko'], 'metal', 'staff', 'lich_joko', 'wisps', False, E('lich_joko', 'scarab')),
    S('B', 'Undying Lich Pharaoh', 'Joko\'s golden headdress and skull blazing with emerald fire.', PAL['joko'], 'gloss', 'mini', 'lich_joko', 'wisps', 'mascot', E('lich_joko', 'scarab')),
    S('C', 'Mummified Royal Scarab', 'A golden Vabbian scarab leaving a necrotic green trail.', PAL['joko'], 'neon', 'shard', 'scarab', 'wisps', True, E('scarab', 'lich_joko')),
    S('C2', 'Joko Pixel', 'Pixel-art pharaoh skull and scarab sprites.', px('joko'), 'pixel', 'classic', 'lich_joko', 'glint', True, E('lich_joko', 'scarab')))
add(15, 'GW2', 'Tyrian-Legends', 'GW2 - Tyrian Legends Ensemble',
    S('A', 'Prismatic Spear and Dragon', 'A prismatic crystal spear with a fiery crimson dragon wing.', PAL['prism'], 'facet', 'glaive', 'dragonwing', 'motes', False, E('dragonwing', 'commander')),
    S('B', 'Commander Tag Crest', 'A colour-cycling commander tag rides your pointer, heroes take turns on the other pointers.', PAL['prism'], 'gloss', 'mini', 'commander', 'motes', 'mascot',
      cyc(['commander', 'charr_tybalt', 'asura_taimi', 'golem_blish', 'sylvari_canach', 'lich_joko'])),
    S('C', 'Painterly Dragon Wing', 'A fiery crimson brushstroke dragon-wing pointer, ArenaNet concept-art style.', PAL['prism'], 'paint', 'brush', 'dragonwing', 'embers', False, E('dragonwing', 'commander')),
    S('C2', 'Pixel Heroes', 'Pixel-art party: all five heroes as crisp 32 px sprites.', px('golem'), 'pixel', 'classic', 'charr_tybalt', 'glint', True,
      cyc(['charr_tybalt', 'asura_taimi', 'golem_blish', 'sylvari_canach', 'lich_joko'])))
add(16, 'GW2', 'Blish-and-Taimi-Magitech', 'GW2 - Blish and Taimi Magitech',
    S('A', 'Golem Hardlight Gauntlet', 'Gold-and-ivory golem gauntlet laced with neon magenta circuitry.', PAL['golem'], 'metal', 'gauntlet', 'golemhead', 'motes', False, E('golemhead', 'polyhedron')),
    S('B', 'Eternal Alchemy Polyhedron', 'Interlocking cyan-and-pink holo-polyhedron core turning beside your pointer.', PAL['magitech'], 'gloss', 'mini', 'polyhedron', 'motes', 'mascot', cyc(['polyhedron', 'golemhead', 'asura_taimi'])),
    S('C', 'Holographic Target Emitter', 'Sleek cyan-and-magenta laser emitter with a target reticle.', PAL['magitech'], 'neon', 'emitter', 'polyhedron', 'motes', False, cyc(['golem_blish', 'asura_taimi'])),
    S('C2', 'Magitech Pixel', 'Pixel-art golem and asura gadget sprites.', px('magitech'), 'pixel', 'wand', 'golem_blish', 'glint', False, cyc(['golem_blish', 'asura_taimi'])))
add(17, 'GW2', 'Canach-Joko-Tybalt', 'GW2 - Canach, Joko and Tybalt',
    S('A', 'Apple, Crescent and Thorn Dagger', 'A dagger uniting Tybalt\'s apple, Joko\'s crescent and Canach\'s thorns.', PAL['drama'], 'metal', 'dagger', 'apple', 'glint', False, cyc(['apple', 'lich_joko', 'sylvari_canach'])),
    S('B', 'Dramatic Tri-Crest', 'Bitten apple, blossom bomb and golden scarab take turns beside your pointer.', PAL['drama'], 'gloss', 'mini', 'apple', 'wisps', 'mascot', cyc(['apple', 'blossom', 'scarab'])),
    S('C', 'Dark Painterly Blade', 'A sweeping obsidian, gold and crimson brushstroke war-pointer.', PAL['drama'], 'paint', 'brush', 'lich_joko', 'embers', False, cyc(['sylvari_canach', 'lich_joko', 'charr_tybalt'])),
    S('C2', 'Trio Pixel', 'Pixel-art sprites of all three rivals.', px('drama'), 'pixel', 'classic', 'lich_joko', 'glint', True, cyc(['sylvari_canach', 'lich_joko', 'charr_tybalt'])))
# ------------------------------------------------------------- Pokemon
add(18, 'Pokemon', 'Kanto-Companions', 'Pokemon - Kanto Companions',
    S('A', 'Glossy Tail and Capture Ball', 'A smooth glossy yellow lightning-tail pointer with a red-and-white capture ball.', PAL['pika'], 'gloss', 'boltptr', 'monsterball', 'motes', False, E('bolt', 'monsterball')),
    S('B', 'Anime Spark Tail', 'Cel-shaded lightning bolt crackling with sparks and a capture ball.', PAL['pika'], 'flat', 'mini', 'bolt', 'motes', 'mascot', E('bolt', 'monsterball')),
    S('C', '16-Bit GBA Pixel', 'Neon-outlined pixel bolt and classic pixel capture ball.', px('pika'), 'pixel', 'boltptr', 'monsterball', 'glint', False, E('bolt', 'monsterball')),
    S('C2', 'Pocket Monochrome', 'Four-shade green handheld pixel art, the original 1996 look.', px('pika', gb=GB), 'pixel', 'classic', 'monsterball', 'glint'))
add(19, 'Pokemon', 'Ghost-Parade', 'Pokemon - Ghost Parade',
    S('A', 'Shadow Spirit and Soul Candle', 'A glossy amethyst ghost pointer with a glowing violet soul candle.', PAL['ghost'], 'gel', 'wisp', 'candle', 'wisps', True, E('gringhost', 'candle')),
    S('B', 'Grinning Ghost and Candle', 'An expressive grinning shadow ghost and a happy little candle.', PAL['ghost'], 'gloss', 'mini', 'gringhost', 'wisps', 'mascot', E('gringhost', 'candle')),
    S('C', 'Lavender Tower Pixel', 'Retro purple pixel ghost and flickering pixel candle.', px('ghost'), 'pixel', 'wisp', 'gringhost', 'glint', True, E('gringhost', 'candle')),
    S('C2', 'Haunting Gas Neon', 'Violet gas-cloud neon with drifting purple wisps.', PAL['ghost'], 'neon', 'wisp', 'ghostling', 'wisps', True, E('ghostling', 'candle')))
# ------------------------------------------------------------ Simpsons
add(20, 'Simpsons', 'Springfield-Donuts', 'Simpsons - Springfield Donuts',
    S('A', 'Plush 3D Hand and Donut', 'A soft yellow four-finger cartoon hand pointer and a glossy pink donut.', PAL['simp'], 'gel', 'cartoonhand', 'donut', 'motes', False),
    S('B', 'Cel-Shaded Cartoon Hand', 'Bold inked yellow hand and a smiling pink-frosted donut, show-style flat colour.', PAL['simp'], 'flat', 'cartoonhand', 'donut', 'glint', False),
    S('C', 'Arcade 16-Bit Pixel', 'Arcade-cabinet pixel-art yellow hand and sprinkled donut.', px('simp'), 'pixel', 'cartoonhand', 'donut', 'glint', False),
    S('C2', 'Springfield Sticker', 'Die-cut sticker pointer with a sprinkle donut charm.', PAL['simp'], 'sticker', 'blunt', 'donut', 'motes'))
add(21, 'Simpsons', 'Nuclear-Nightshift', 'Simpsons - Nuclear Nightshift',
    S('A', 'Glowing Carbon Rod and Fish', 'Neon-green glowing carbon rod pointer and a three-eyed fish.', PAL['nuke'], 'gloss', 'rodptr', 'fish3', 'motes', False, E('nuclear', 'fish3')),
    S('B', 'Oozing Cartoon Rod', 'A dripping radioactive cel-shaded rod and a wide-eyed three-eyed fish.', PAL['nuke'], 'flat', 'mini', 'fish3', 'drips', 'mascot', E('rod', 'fish3')),
    S('C', 'Sector 7G Pixel', 'Pixel-art plutonium rod and a pixel three-eyed fish spinner.', px('nuke'), 'pixel', 'rodptr', 'fish3', 'glint', False, E('nuclear', 'fish3')),
    S('C2', 'Control Room Neon', 'Night-shift control-panel neon with a radiation core.', P('5aff3a', '0a4a10', '020a02', 'ffe14a', 'b6ff6a', '5aff3a', '10180a', bad='ff5a2a'), 'neon', 'shard', 'nuclear', 'motes', True, E('nuclear', 'fish3')))
# ---------------------------------------------------------- Cute / classic
add(22, 'Cute-Classic', 'Sanrio-Friends-Remastered', 'Cute - Sanrio Friends Remastered',
    S('A', 'Plush Satin Bow and Angel Wing', 'Soft pastel pink-and-blue satin bow with a fluffy angel wing.', PAL['pastel'], 'gel', 'blunt', 'ribbon', 'motes', True, E('ribbon', 'angelwing')),
    S('B', 'Kawaii Cel-Shaded Bow', 'Crisp outlined pastel ribbon bow and feathered wing, with the bunny friend.', PAL['pastel'], 'flat', 'mini', 'friend', 'motes', 'mascot', E('ribbon', 'angelwing')),
    S('C', 'Remastered Pastel Pixel', 'Desktop-pet pixel art: pink-and-blue bow and angel wing.', px('pastel'), 'pixel', 'classic', 'ribbon', 'motes', True, E('ribbon', 'angelwing')),
    S('C2', 'Pastel Sticker', 'Soft pink die-cut sticker pointer with a ribbon-bunny friend charm.', PAL['pastel'], 'sticker', 'blunt', 'friend', 'motes', True, E('friend', 'ribbon')))
add(23, 'Cute-Classic', 'Strawberry-Dream-Bakery', 'Cute - Strawberry Dream Bakery',
    S('A', 'Glazed Berry and Macarons', 'A glossy ruby strawberry with pastel macarons and a cream dip.', PAL['berry'], 'gloss', 'drip', 'strawberry', 'drips', False, E('strawberry', 'macaron')),
    S('B', 'Patisserie Cel Berry', 'Hand-inked cream-dipped strawberry and mint/rose macarons.', PAL['berry'], 'flat', 'mini', 'strawberry', 'motes', 'mascot', E('strawberry', 'macaron')),
    S('C', 'Cozy Bakery Pixel', 'Pastel pixel strawberry and a pixel macaron stack.', px('berry'), 'pixel', 'classic', 'strawberry', 'motes', True, E('strawberry', 'macaron')),
    S('C2', 'Berry Sticker', 'Cream-and-strawberry die-cut sticker with a sparkly berry charm.', PAL['berry'], 'sticker', 'blunt', 'strawberry', 'motes', True, E('strawberry', 'macaron')))
add(24, 'Cute-Classic', 'Spooky-Paws', 'Cute - Spooky Paws',
    S('A', 'Plush Toe-Beans and Witch Hat', 'A velvety black cat-paw pointer with squishy beans and a moon witch hat.', PAL['spooky'], 'gel', 'sleek', 'pawprint', 'motes', True, E('pawprint', 'witchhat')),
    S('B', 'Illustrated Claws and Hat', 'Cel-shaded black paw with tiny claws and a crescent-buckle witch hat.', PAL['spooky'], 'flat', 'mini', 'witchhat', 'eyes', 'mascot', E('pawprint', 'witchhat')),
    S('C', 'Midnight Pixel Paw', 'Pastel-goth pixel toe-bean paw and pixel witch hat.', px('spooky'), 'pixel', 'sleek', 'pawprint', 'glint', True, E('pawprint', 'witchhat')),
    S('C2', 'Pumpkin Neon', 'Jack-o\'-lantern orange neon on midnight black with floating embers.', P('ff8a1a', '5a2a0a', '06040a', 'ffd35a', 'c58cff', 'ff8a1a', '120e1a'), 'neon', 'wisp', 'pumpkin', 'embers', True, E('pumpkin', 'witchhat')))

assert len(SETS24) == 24 and all(len(s['styles']) == 4 for s in SETS24)
