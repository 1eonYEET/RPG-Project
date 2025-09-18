# game/wave_manager.py
import random
from characters.enemy import Enemy
from items.sword_iron import IronSword
from items.armor_leather import LeatherArmor
from items.charm_lucky import LuckyCharm
from game.boss_pool import get_random_boss

class WaveManager:
    """
    - Jede 5. Welle ist ein Boss.
    - Gegner skalieren NICHT pro Welle, sondern nur, wenn ein Boss besiegt wurde (tier++).
    - NEU: Nach JEDEM Boss-Sieg erhalten alle zukünftigen Gegner einen zusätzlichen globalen Buff (stackend).
    """
    BOSS_EVERY = 5

    def __init__(self):
        self.wave_number = 0
        self.tier = 0  # steigt NUR nach Boss-Sieg
        self.global_buff_stacks = 0  # NEU: steigt NUR nach Boss-Sieg

        # Boss-Multiplikatoren/Aufschläge
        self.boss_hp_mult   = 2.0
        self.boss_atk_mult  = 1.35
        self.boss_def_add   = 1
        self.boss_xp_bonus  = 3
        self.boss_gold_bonus= 25

        # garantierte Boss-Drops
        self.boss_drop_pool = [IronSword, LeatherArmor, LuckyCharm]

    # -------------------- Tier-Basiswerte (Balancing) --------------------
    def _params_for_tier(self, tier: int):
        if tier <= 0:
            return dict(hp=36, atk=8,  df=2, crit=0.03, dodge=0.01, armor=0.02, xp=2, gold=15)
        if tier == 1:
            return dict(hp=46, atk=10, df=2, crit=0.05, dodge=0.02, armor=0.04, xp=3, gold=20)
        if tier == 2:
            return dict(hp=58, atk=12, df=3, crit=0.07, dodge=0.03, armor=0.06, xp=4, gold=25)
        if tier == 3:
            return dict(hp=72, atk=14, df=3, crit=0.09, dodge=0.04, armor=0.08, xp=5, gold=30)
        extra = tier - 3
        return dict(
            hp   = 72 + 14 * extra,
            atk  = 14 +  2 * extra,
            df   =  3 + (extra // 2),
            crit = min(0.09 + 0.01 * extra, 0.30),
            dodge= min(0.04 + 0.005 * extra, 0.20),
            armor= min(0.08 + 0.02 * extra, 0.50),
            xp   = 5 + 1 * extra,
            gold = 30 + 5 * extra
        )

    # -------------------- Globaler Buff nach Boss-Sieg --------------------
    def _apply_global_buff(self, p: dict) -> dict:
        """Wendet den stackenden Global-Buff auf die Basiswerte an (nur für ZUKÜNFTIGE Gegner)."""
        stacks = self.global_buff_stacks
        if stacks <= 0:
            return p

        # Multiplikative Verstärkung für HP/ATK, additive Caps für die anderen
        hp_mult  = (1.10) ** stacks   # +10% HP je Stack
        atk_mult = (1.08) ** stacks   # +8%  ATK je Stack

        p = p.copy()
        p["hp"]   = int(p["hp"]  * hp_mult)
        p["atk"]  = int(p["atk"] * atk_mult)
        p["df"]   = p["df"] + (stacks // 2)  # +1 DEF pro 2 Stacks
        p["crit"] = min(0.30, p["crit"]  + 0.01  * stacks)
        p["dodge"]= min(0.20, p["dodge"] + 0.005 * stacks)
        p["armor"]= min(0.50, p["armor"] + 0.02  * stacks)
        # XP/Gold leicht mitziehen
        p["xp"]   = p["xp"]   + stacks
        p["gold"] = p["gold"] + 3 * stacks
        return p

    def next_enemy(self) -> Enemy:
        self.wave_number += 1
        is_boss = (self.wave_number % self.BOSS_EVERY == 0)

        # Tier-Basis holen und globalen Buff anwenden
        base = self._params_for_tier(self.tier)
        p = self._apply_global_buff(base)

        name = f"Welle-{self.wave_number} Gegner"
        portrait = None

        hp, atk, deff = p["hp"], p["atk"], p["df"]
        crit, dodge, armor = p["crit"], p["dodge"], p["armor"]
        xp, gold = p["xp"], p["gold"]

        if is_boss:
            boss_info = get_random_boss()
            name = f"{boss_info.name} (Boss Welle {self.wave_number})"
            portrait = boss_info.portrait
            hp   = int(hp  * self.boss_hp_mult)
            atk  = int(atk * self.boss_atk_mult)
            deff = deff + self.boss_def_add
            xp  += self.boss_xp_bonus
            gold+= self.boss_gold_bonus

        enemy = Enemy(
            name=name,
            hp=hp,
            attack=atk,
            defense=deff,
            xp_reward=xp,
            gold_reward=gold,
            crit_chance=crit,
            dodge_chance=dodge,
            armor=armor,
            is_boss=is_boss
        )
        enemy.portrait = portrait

        if is_boss and self.boss_drop_pool:
            drop_ctor = random.choice(self.boss_drop_pool)
            enemy.drop_table = [drop_ctor]  # garantiert 1 Drop

        return enemy

    def boss_defeated_increase_tier(self):
        """Nach Boss-Sieg die globale Schwierigkeit erhöhen (Tier + Global-Buff)."""
        self.tier += 1
        self.global_buff_stacks += 1
