from characters.character import Character
from characters.companion import Companion
from companions.triggers import CompanionTrigger

class SacrificeCompanion(Companion):
    def take_turn(self, opponent: "Character", logger):
        pass

    def __init__(self):
        super().__init__(
            name="Opfergeist",
            hp=10,
            ability_type="sacrifice",
            description="Rettet dich einmal pro Kampf vor dem Tod, indem er den tödlichen Schaden auf sich nimmt.",
            ability_data={"saved_this_fight": False}
        )

    def reset_combat_flags(self):
        super().reset_combat_flags()
        self.ability_data["saved_this_fight"] = False

    def use_ability(self, trigger, player, enemy=None, logger=None):
        if trigger == CompanionTrigger.ON_DAMAGE and not self.ability_data["saved_this_fight"]:
            # Prüfe, ob Schaden tödlich wäre
            incoming_damage = getattr(enemy, "pending_damage", None)
            if incoming_damage is None:
                incoming_damage = 0
            if player.hp - incoming_damage <= 0:
                self.ability_data["saved_this_fight"] = True
                player.hp = 1
                if logger:
                    logger.log(
                        f"🛡️ {self.name} opfert sich und rettet {player.name} vor dem sicheren Tod! ({player.name} überlebt!")
                return True  # Schaden wird komplett verhindert!
        return False