# battle/battle_manager.py
from companions.triggers import CompanionTrigger
from display.status_display import StatusDisplay
from messaging.battle_logger import BattleLogger

class BattleManager:
    def __init__(self, player, enemy, notifier):
        self.player = player
        self.enemy = enemy
        self.notifier = notifier
        self.status_display = StatusDisplay(notifier)
        self.logger = BattleLogger(notifier)
        self._round_number = 0

    def start(self):
        self.notifier.notify(f"⚔️ Der Kampf gegen {self.enemy.name} beginnt!")

        # Companion-Fähigkeit zu Beginn des Kampfes
        if self.player.companion and self.player.kills > 0:
            self.player.companion.reset_combat_flags()
            self.player.companion.use_ability(CompanionTrigger.PRE_FIGHT, self.player, self.enemy, self.logger)
            self.logger.flush()

        if getattr(self.enemy, "is_boss", False) and getattr(self.enemy, "portrait", None):
            self.notifier.notify(f"\n{self.enemy.portrait}")

        self.player._combat_id = getattr(self.player, "_combat_id", 0) + 1

        while self.player.is_alive() and self.enemy.is_alive():
            self._round_number += 1

            # Rundenkopf & Statusanzeige (nur vor Spielerzug)
            self.notifier.notify(f"\n🌀 Runde {self._round_number}")
            self.status_display.show(self.player, self.enemy)

            # Companion-Fähigkeit zu Beginn jeder Runde
            if self.player.companion:
                self.player.companion.use_ability(CompanionTrigger.TURN_START, self.player, self.enemy, self.logger)
                self.logger.flush()

            # Spielerzug
            self.player.take_turn(self.enemy, self.logger)
            self.logger.flush()


            # Optional für Effekte am Rundenende
            if self.player.companion:
                self.player.companion.use_ability(CompanionTrigger.TURN_END, self.player, self.enemy, self.logger)
                self.logger.flush()

            if not self.enemy.is_alive():
                if not hasattr(self.player, "kills"):
                    self.player.kills = 0
                self.player.kills += 1

                self.notifier.notify(f"🎉 Du hast {self.enemy.name} besiegt!")
                if hasattr(self.enemy, "gold_reward"):
                    self.player.gold += self.enemy.gold_reward
                    # Gesamt-Gold mitzählen (Shop-Ausgaben ändern diesen Wert NICHT)
                    if not hasattr(self.player, "total_gold_earned"):
                        self.player.total_gold_earned = 0
                    self.player.total_gold_earned += self.enemy.gold_reward
                    self.notifier.notify(f"💰 Beute: +{self.enemy.gold_reward}g (Geldbeutel: {self.player.gold}g)")
                if hasattr(self.enemy, "xp_reward"):
                    self.player.gain_xp(self.enemy.xp_reward, self.notifier)

                if getattr(self.enemy, "drop_table", None):
                    for ctor in self.enemy.drop_table:
                        item = ctor()
                        self.player.inventory.add_item(item)
                        self.notifier.notify(f"🎁 Drop erhalten: {item.name()} — {item.description()}")

                # Nach Kampf
                if self.player.companion:
                    self.player.companion.use_ability(CompanionTrigger.POST_FIGHT, self.player, self.enemy, self.logger)
                    self.logger.flush()

                break

            # Gegnerzug
            self.enemy.take_turn(self.player, self.logger)
            self.logger.flush()

            if not self.player.is_alive():
                self.notifier.notify("☠️ Du wurdest besiegt...")
                break
