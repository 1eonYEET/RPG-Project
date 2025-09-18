# skills/skill_factory.py
from skills.skill import Skill
from skills.fireball import Fireball
from skills.heal import Heal
from skills.piercing_strike import PiercingStrike

# Ultimates
from skills.ultimate_unzerstoerbar import Unzerstoerbar
from skills.ultimate_toedlicher_schlag import ToedlicherSchlag
from skills.ultimate_arkaner_sturm import ArkanerSturm
from skills.ultimate_heldenmut import Heldenmut


class SkillFactory:
    _registry = {
        "Fireball": Fireball,
        "Heal": Heal,
        "PiercingStrike": PiercingStrike,
        "Unzerstoerbar": Unzerstoerbar,
        "ToedlicherSchlag": ToedlicherSchlag,
        "ArkanerSturm": ArkanerSturm,
        "Heldenmut": Heldenmut,
    }

    @classmethod
    def create(cls, name: str) -> Skill:
        try:
            return cls._registry[name]()
        except KeyError:
            raise ValueError(f"Unbekannte Fähigkeit: {name}")
