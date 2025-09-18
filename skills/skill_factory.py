# skills/skill_factory.py
from typing import Type
from skills.skill import Skill
from skills.fireball import Fireball
from skills.heal import Heal
from skills.piercing_strike import PiercingStrike

class SkillFactory:
    _registry = {
        "Fireball": Fireball,
        "Heal": Heal,
        "PiercingStrike": PiercingStrike,
    }

    @classmethod
    def create(cls, name: str) -> Skill:
        if name not in cls._registry:
            raise ValueError(f"Unbekannte Fähigkeit: {name}")
        return cls._registry[name]()
