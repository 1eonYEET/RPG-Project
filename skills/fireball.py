from skills.skill import Skill

class Fireball(Skill):
    def __init__(self):
        super().__init__(
            "Feuerball",
            mana_cost=6,
            description="Schleudert einen Feuerball, der hohen magischen Schaden verursacht. Skaliert mit Zauberkraft."
        )

    def use(self, user, target, logger):
        damage = 20 + int(user.spell_power * 12)
        logger.log(f"🔥 {user.name} wirft einen Feuerball auf {target.name} und verursacht {damage} Schaden!")
        target.receive_damage(damage)
