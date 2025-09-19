# characters/enemy.py
import random
from typing import List, Callable
from characters.character import Character

class Enemy(Character):
    def __init__(self, name, hp, attack, defense, xp_reward=1, gold_reward=10,
                 crit_chance=0.05, dodge_chance=0.02, armor=0.0, is_boss=False):
        super().__init__(name, hp, attack, defense)
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.crit_chance = crit_chance
        self.dodge_chance = min(max(dodge_chance, 0.0), 0.6)
        self.armor = min(max(armor, 0.0), 0.8)
        self.is_boss = is_boss
        self.drop_table: List[Callable] = []

    def add_drop(self, ctor):
        self.drop_table.append(ctor)

    def take_turn(self, opponent, logger):
        logger.log(f"\n👹 {self.name}'s Runde! ({self.hp} HP)")
        attack_pattern = ["attack"] #add "idle" to reduce difficulty
        action = random.choice(attack_pattern)
        if action == "attack":
            base = max(0, self.attack - opponent.defense)
            self.attempt_attack(opponent, base_damage=base, logger=logger, label="Angriff")
        else:
            logger.log(f"{self.name} zögert...")
