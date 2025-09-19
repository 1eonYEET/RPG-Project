from characters.character import Character
from characters.companion import Companion
from companions.triggers import CompanionTrigger

class GoldCompanion(Companion):
    def take_turn(self, opponent: "Character", logger):
        pass

    def __init__(self):
        super().__init__(
            name="Gold-Gremlin",
            hp=15,
            ability_type="gold_bonus",
            description="Erhöht deinen Goldgewinn nach jedem Kampf um 10%",
            ability_data={"gold_bonus_percent": 0.10}
        )

    def use_ability(self, trigger, player, enemy=None, logger=None):
        if trigger == CompanionTrigger.POST_FIGHT and hasattr(enemy, "gold_reward"):
            bonus_percent = self.ability_data.get("gold_bonus_percent", 0.10)
            gold_reward = getattr(enemy, "gold_reward", 0)
            bonus_gold = int(gold_reward * bonus_percent)
            player.gold += bonus_gold
            if not hasattr(player, "total_gold_earned"):
                player.total_gold_earned = 0
            player.total_gold_earned += bonus_gold
            if logger:
                logger.log(f"🪙 {self.name} schenkt {player.name} {bonus_gold} Bonus-Gold ({int(bonus_percent*100)}%) für den Sieg!")