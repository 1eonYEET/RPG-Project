from characters.player import PlayerCharacter

class Tank(PlayerCharacter):
    def __init__(self, name: str):
        # mehr Leben, etwas mehr DEF, weniger ATK
        super().__init__(name=name, hp=70, attack=10, defense=4)
        self.archetype = "Tank"
        self.mana = 10
        self.max_mana = 10
        self.armor = 0.20            # bessere Schadensreduktion
        self.crit_chance = 0.05      # schlechterer Crit
        self.dodge_chance = 0.02     # schlechteres Ausweichen
        self.heal_power = 1.5        # besseres Heilen
        self.spell_power = 0.9       # Spells etwas schwächer
        self.life_steal = 0

class Assassin(PlayerCharacter):
    def __init__(self, name: str):
        # weniger HP/DEF, dafür mehr ATK und Evasion/Crit
        super().__init__(name=name, hp=40, attack=14, defense=2)
        self.archetype = "Assassin"
        self.mana = 10
        self.max_mana = 10
        self.armor = 0.05
        self.crit_chance = 0.25      # hoher Crit
        self.dodge_chance = 0.15     # hohes Ausweichen
        self.heal_power = 0.8        # schwächeres Heilen
        self.spell_power = 1.0
        self.life_steal = 0

class Mage(PlayerCharacter):
    def __init__(self, name: str):
        # mehr Mana, Spells sind effektiver
        super().__init__(name=name, hp=45, attack=11, defense=2)
        self.archetype = "Mage"
        self.mana = 20
        self.max_mana = 20
        self.armor = 0.10
        self.crit_chance = 0.10
        self.dodge_chance = 0.05
        self.heal_power = 1.0
        self.spell_power = 1.5       # Spells stärker
        self.life_steal = 0

class Knight(PlayerCharacter):
    def __init__(self, name: str):
        # balancierter Mix
        super().__init__(name=name, hp=55, attack=12, defense=3)
        self.archetype = "Knight"
        self.mana = 12
        self.max_mana = 12
        self.armor = 0.12
        self.crit_chance = 0.12
        self.dodge_chance = 0.07
        self.heal_power = 1.0
        self.spell_power = 1.0
        self.life_steal = 0

class Vampire(PlayerCharacter):
    def __init__(self, name:str):
        super().__init__(name=name, hp=50, attack=12, defense=2)
        self.archetype= "Vampire"
        self.mana = 15
        self.max_mana = 15
        self.armor = 0.10
        self.crit_chance = 0.10
        self.dodge_chance = 0.10
        self.heal_power = 1.5
        self.spell_power = 1.5
        self.life_steal = 0.15