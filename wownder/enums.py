from flask_babel import gettext as _

CURRENT_MAX_LEVEL = 110

RACE = {
    1: _('Human'),
    2: _('Orc'),
    3: _('Dwarf'),
    4: _('Night Elf'),
    5: _('Undead'),
    6: _('Tauren'),
    7: _('Gnome'),
    8: _('Troll'),
    9: _('Goblin'),
    10: _('Blood Elf'),
    11: _('Draenei'),
    22: _('Worgen'),
    24: _('Pandaren'),
    25: _('Pandaren'),
    26: _('Pandaren'),
}

CLASS = {
    1:  _('Warrior'),
    2:  _('Paladin'),
    3:  _('Hunter'),
    4:  _('Rogue'),
    5:  _('Priest'),
    6:  _('Death Knight'),
    7:  _('Shaman'),
    8:  _('Mage'),
    9:  _('Warlock'),
    10: _('Monk'),
    11: _('Druid'),
    12: _('Demon Hunter'),
}

QUALITY = {
    1: 'Common',
    2: 'Uncommon',
    3: 'Rare',
    4: 'Epic',
    5: 'Legendary',
}

RACE_TO_FACTION = {
    1:  _('Alliance'),
    2:  _('Horde'),
    3:  _('Alliance'),
    4:  _('Alliance'),
    5:  _('Horde'),
    6:  _('Horde'),
    7:  _('Alliance'),
    8:  _('Horde'),
    9:  _('Horde'),
    10: _('Horde'),
    11: _('Alliance'),
    22: _('Alliance'),
    24: _('?'),
    25: _('Alliance'),
    26: _('Horde'),
}

EXPANSION = {
    0: ('wow', 'World of Warcraft'),
    1: ('bc', 'The Burning Crusade'),
    2: ('lk', 'Wrath of the Lich King'),
    3: ('cata', 'Cataclysm'),
    4: ('mop', 'Mists of Pandaria'),
}

RAIDS = {
    'wow': (2717, 2677, 3429, 3428),
    'bc': (3457, 3836, 3923, 3607, 3845, 3606, 3959, 4075),
    'lk': (4603, 3456, 4493, 4500, 4273, 2159, 4722, 4812, 4987),
    'cata': (5600, 5094, 5334, 5638, 5723, 5892),
    'mop': (6125, 6297, 6067),
}
