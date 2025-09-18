from skills.skill import Skill

class Heal(Skill):
    def __init__(self):
        super().__init__("Heilung", mana_cost=5)

    def use(self, user, target, logger):
        mult = getattr(user, "heal_power", 1.0)
        heal_amount = int(15 * mult)
        user.hp = min(user.max_hp, user.hp + heal_amount)
        logger.log(f"💖 {user.name} heilt sich um {heal_amount} HP!")
