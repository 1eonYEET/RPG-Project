from characters.character import Character
from skilltree.engine import SkillTreeEngine
from systems.inventory import Inventory
from skills.fireball import Fireball
from skills.heal import Heal

class PlayerCharacter(Character):
    def __init__(self, name: str, hp: int, attack: int, defense: int):
        super().__init__(name, hp, attack, defense)

        # Ressourcen
        self.mana = 10
        self.max_mana = 10
        self.gold = 0
        self.total_gold_earned = 0
        self.heal_potions = 3   # Start mit 3 Heiltränken

        # Startwerte / Archetyp-Defaults (werden ggf. durch Archetypen überschrieben)
        self.archetype = "Adventurer"
        self.armor = 0.10
        self.crit_chance = 0.10
        self.dodge_chance = 0.05
        self.heal_power = 1.0
        self.spell_power = 1.0
        self.life_steal = 0

        # Progression
        self.level = 1
        self.xp = 0
        self.xp_to_next = 3

        # Inventar (passive, stackende Items)
        self.inventory = Inventory(owner=self)

        # Skills
        self.skills = self.load_skills()

        #Skilltree
        self.unlocked_nodes = []
        self._skill_engine = SkillTreeEngine()

        self.companion = None

    def load_skills(self):
        return [Fireball(), Heal()]

    # -------- Level/XP --------
    def gain_xp(self, amount, notifier):
        self.xp += amount
        notifier.notify(f"✨ Du erhältst {amount} XP! ({self.xp}/{self.xp_to_next})")

        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self._update_xp_thresholds()
            notifier.notify(f"\n📈 LEVEL UP! Du bist jetzt Level {self.level}!")

            # Nur Skilltree-Entscheidung, keine separaten Stat-Boni mehr
            self._skill_engine.present_and_apply(self, notifier)

        notifier.notify(f"➡️ Nächstes Level bei {self.xp_to_next} XP. (Aktuell: {self.xp} XP)")

    '''def level_up_menu(self, notifier):
        print("Wähle deinen Bonus:")
        print("1. +10 Max-HP")
        print("2. +2 Angriff")
        print("3. +5% Rüstung (max 80%)")
        print("4. +5% Krit-Chance (max 100%)")
        print("5. +3% Ausweichchance (max 60%)")
        choice = input("Deine Wahl: ")
        if choice == "1":
            self.max_hp += 10
            self.hp += 10
            notifier.notify("❤️ Max-HP erhöht!")
        elif choice == "2":
            self.attack += 2
            notifier.notify("🗡️ Angriff erhöht!")
        elif choice == "3":
            self.armor = min(self.armor + 0.05, 0.8)
            notifier.notify(f"🛡️ Rüstung erhöht! ({int(self.armor * 100)}%)")
        elif choice == "4":
            self.crit_chance = min(self.crit_chance + 0.05, 1.0)
            notifier.notify(f"🎯 Krit-Chance erhöht! ({int(self.crit_chance * 100)}%)")
        elif choice == "5":
            self.dodge_chance = min(self.dodge_chance + 0.03, 0.60)
            notifier.notify(f"🚶‍♂️ Ausweichchance erhöht! ({int(self.dodge_chance * 100)}%)")
        else:
            notifier.notify("❌ Ungültige Eingabe. Kein Bonus erhalten.")'''

    # -------- Zug: Inventar ansehen verbraucht keinen Zug --------
    def take_turn(self, opponent, logger):
        while True:
            print(f"\n🧙 Deine Runde! ({self.hp} HP, {self.mana} Mana)")
            print("0. Inventar ansehen (verbraucht keinen Zug)")
            print(f"1. Angreifen")
            print(f"2. Heiltrank benutzen (x{self.heal_potions})")
            print("3. Fähigkeit einsetzen")
            choice = input("Wähle eine Aktion: ").strip()

            if choice == "0":
                self._show_inventory()
                continue  # kein Zugverbrauch

            if choice == "1":
                base = max(0, self.attack - opponent.defense)
                if self.attempt_attack(opponent, base_damage=base, logger=logger, label="Angriff"):
                    self.apply_life_steal(damage=base, logger=logger)
                break

            elif choice == "2":
                if self.heal_potions <= 0:
                    logger.log("🧪 Kein Heiltrank mehr übrig!")
                    # trotzdem darf man noch was anderes wählen
                    continue
                heal_base = 20
                heal_amount = int(heal_base * self.heal_power)  # Tank profitiert z. B. stärker
                before = self.hp
                self.hp = min(self.max_hp, self.hp + heal_amount)
                actual = self.hp - before
                self.heal_potions -= 1
                logger.log(f"🧪 Du trinkst einen Heiltrank (+{actual} HP). Verbleibend: x{self.heal_potions}")
                break

            elif choice == "3":
                self.show_and_use_skill(opponent, logger)
                break

            else:
                logger.log("❌ Ungültige Eingabe.")

    def _show_inventory(self):
        print("\n🎒 INVENTAR (passive Effekte, stackend):")
        if self.inventory.is_empty() and self.heal_potions <= 0:
            print("  – leer –")
            return
        # Heiltränke zuerst
        if self.heal_potions > 0:
            print(f"  Heiltrank x{self.heal_potions} — Heilt 20 HP (skaliert mit Heilbonus)")
        # Dann Items
        for line in self.inventory.list_items():
            print(" ", line)

    def show_and_use_skill(self, opponent, logger):
        print("\n✨ Verfügbare Fähigkeiten:")
        for idx, skill in enumerate(self.skills, start=1):
            print(f"{idx}. {skill.get_name()} (Kosten: {skill.mana_cost})")
        try:
            skill_choice = int(input("Welche Fähigkeit verwenden? ")) - 1
            skill = self.skills[skill_choice]
            if self.mana < skill.mana_cost:
                logger.log("🚫 Nicht genug Mana!")
                return
            self.mana -= skill.mana_cost
            skill.use(self, opponent, logger)
        except (ValueError, IndexError):
            logger.log("❌ Ungültige Auswahl.")

    def _update_xp_thresholds(self):
        if self.level <= 3:
            self.xp_to_next = 3 + (self.level - 1)
            if self.level == 3:
                self.xp_to_next = 6
        elif self.level == 4:
            self.xp_to_next = 8
        elif self.level == 5:
            self.xp_to_next = 10
        else:
            self.xp_to_next += 2

    def apply_life_steal(self, damage, logger):
        before = self.hp
        heal_amount = int(damage * self.life_steal)
        self.hp = min(self.max_hp, self.hp + heal_amount)
        actual = self.hp - before
        if actual > 0:
            logger.log(f"🩸 Du heilst dich mit Lifesteal um (+{actual} HP).")

    def add_max_health(self, amount):
        self.max_hp += amount

    def summon_companion(self, companion):
        self.companion = companion