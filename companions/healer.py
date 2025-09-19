from characters.character import Character
from characters.companion import Companion
from companions.triggers import CompanionTrigger


class HealerCompanion(Companion):
    def take_turn(self, opponent: "Character", logger):
        pass

    def __init__(self):
        super().__init__(
            name="Heilender Sprite",
            hp=20,
            ability_type="heal",
            description="Heilt den Spieler vor Kampfbeginn ein bisschen",
            ability_data={"heal_amount": 10}
        )

    def use_ability(self, trigger, player, enemy=None, logger=None):
        # Heilt Spieler am Rundenanfang
        if trigger == CompanionTrigger.PRE_FIGHT:
            heal = self.ability_data["heal_amount"]
            player.hp = min(player.max_hp, player.hp + heal)
            if logger:
                logger.log(f"{self.name} heilt {player.name} um {heal} HP!")