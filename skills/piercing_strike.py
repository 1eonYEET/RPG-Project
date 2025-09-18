# skills/piercing_strike.py
from skills.skill import Skill

class PiercingStrike(Skill):
    """
    Durchdringender Schlag:
    Physischer Treffer, der 25% der gegnerischen DEF ignoriert.
    (Einfach, gut testbar; kein Crit/Dodge, analog zu vorhandenen Skills.)
    """
    def __init__(self):
        super().__init__("Durchdringender Schlag", mana_cost=4)

    def use(self, user, target, logger):
        # 25% DEF ignorieren → effektive DEF verringern
        effective_def = max(0, int(target.defense * 0.75))
        base = max(0, user.attack + 5 - effective_def)
        damage = base
        logger.log(f"🗡️ {user.name} setzt {self.get_name()} ein und verursacht {damage} Schaden (DEF teils ignoriert)!")
        target.receive_damage(damage)
