# skilltree/schema.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Literal, Union

@dataclass
class AddStatsEffect:
    hp: int = 0
    attack: int = 0
    defense: int = 0
    mana: int = 0
    armor_add: float = 0.0
    crit_add: float = 0.0
    dodge_add: float = 0.0
    spell_power: float = 0.0
    heal_power: float = 0.0
    life_steal: float = 0.0

@dataclass
class AddSkillEffect:
    skill_name: str

EffectSpec = Union[AddStatsEffect, AddSkillEffect]

@dataclass
class NodeOption:
    id: str
    name: str
    desc: str
    level: int
    archetype: str  # "generic" oder Klassenname
    requires: List[str] = field(default_factory=list)
    effect: EffectSpec = None
