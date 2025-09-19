from characters.character import Character

class Companion(Character):
    """
    Basisklasse für Begleiter. Jeder Companion kann mit use_ability() auf einen Kampf-Trigger reagieren.
    """
    def __init__(self, name, hp, ability_type, description = "", ability_data=None):
        super().__init__(name, hp, attack=0, defense=0)
        self.ability_type = ability_type
        self.ability_data = ability_data or {}
        self.description = description
        self.used_this_fight = False  # Für einmalige Effekte

    def reset_combat_flags(self):
        self.used_this_fight = False

    def use_ability(self, trigger, player, enemy=None, logger=None):
        """
        Muss von Subklassen überschrieben werden.
        trigger: str, z.B. 'pre_fight', 'turn_start', 'turn_end', 'on_damage', 'post_fight'
        """
        pass