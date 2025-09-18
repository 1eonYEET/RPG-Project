from skills.skill import Skill

class Fireball(Skill):
    def __init__(self):
        super().__init__("Feuerball", mana_cost=5)

    def use(self, user, target, logger):
        base = user.attack + 10
        mult = getattr(user, "spell_power", 1.0)
        damage = int(base * mult)
        logger.log(f"🔥 {user.name} wirft einen Feuerball und verursacht {damage} Schaden!")
        target.receive_damage(damage)
