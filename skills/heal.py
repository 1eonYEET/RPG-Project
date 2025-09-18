from skills.skill import Skill

class Heal(Skill):
    def __init__(self):
        super().__init__(
            "Heilen",
            mana_cost=5,
            description="Stellt eine moderate Menge HP wieder her. Skaliert mit Heilbonus."
        )

    def use(self, user, target, logger):
        heal_amount = 15 + int(user.heal_power * 10)
        user.hp = min(user.max_hp, user.hp + heal_amount)
        logger.log(f"💖 {user.name} heilt sich um {heal_amount} HP!")
