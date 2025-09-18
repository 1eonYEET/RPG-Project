# display/status_display.py

class StatusDisplay:
    def __init__(self, notifier, bar_length=20):
        self.notifier = notifier
        self.bar_length = bar_length

    def show(self, player, enemy):
        # Balken vorbereiten
        player_hp_bar   = self._create_bar(getattr(player, "hp", 0), getattr(player, "max_hp", 0))
        player_mana_bar = self._create_bar(getattr(player, "mana", 0), getattr(player, "max_mana", 0))
        player_xp_bar   = self._create_bar(getattr(player, "xp", 0), getattr(player, "xp_to_next", 1))
        enemy_hp_bar    = self._create_bar(getattr(enemy, "hp", 0), getattr(enemy, "max_hp", 0))

        # Archetypen-Icons
        archetype_icons = {
            "Tank": "🛡️",
            "Assassin": "🗡️",
            "Mage": "🔮",
            "Knight": "⚔️"
        }
        archetype_name = getattr(player, "archetype", "Adventurer")
        icon = archetype_icons.get(archetype_name, "🧙")

        # Inventar-Zeile (passive, stackende Items)
        inv = getattr(player, "inventory", None)
        if inv and not inv.is_empty():
            # list_items() liefert bereits "Name xN — Beschreibung"
            # Für die Statuszeile zeigen wir nur "Name xN"
            names_only = []
            for entry in inv.list_items():
                names_only.append(entry.split(" — ")[0])
            inv_text = " | ".join(names_only)
        else:
            inv_text = "-"

        # Prozentwerte sicher formatieren
        p_arm   = int(round(100 * float(getattr(player, "armor", 0.0))))
        p_crit  = int(round(100 * float(getattr(player, "crit_chance", 0.0))))
        p_dodge = int(round(100 * float(getattr(player, "dodge_chance", 0.0))))

        e_arm   = int(round(100 * float(getattr(enemy, "armor", 0.0))))
        e_crit  = int(round(100 * float(getattr(enemy, "crit_chance", 0.0))))
        e_dodge = int(round(100 * float(getattr(enemy, "dodge_chance", 0.0))))

        # Boss-Markierung
        enemy_prefix = "👑 " if getattr(enemy, "is_boss", False) else "👹 "

        # Ausgabe
        self.notifier.notify(f"""
📊 STATUS
────────────────────────────
{icon} Spieler: {getattr(player, 'name', 'Spieler')} (Lvl {getattr(player, 'level', 1)}, {archetype_name})
   HP:    {getattr(player, 'hp', 0)}/{getattr(player, 'max_hp', 0)} {player_hp_bar}
   Mana:  {getattr(player, 'mana', 0)}/{getattr(player, 'max_mana', 0)} {player_mana_bar}
   XP:    {getattr(player, 'xp', 0)}/{getattr(player, 'xp_to_next', 1)} {player_xp_bar}
   ATK:   {getattr(player, 'attack', 0)}   DEF: {getattr(player, 'defense', 0)}
   ARM:   {p_arm}%   CRIT: {p_crit}%   DODGE: {p_dodge}%
   GOLD:  {getattr(player, 'gold', 0)}g
   ITEMS: {inv_text}
────────────────────────────
{enemy_prefix}Gegner: {getattr(enemy, 'name', 'Gegner')}
   HP:    {getattr(enemy, 'hp', 0)}/{getattr(enemy, 'max_hp', 0)} {enemy_hp_bar}
   ATK:   {getattr(enemy, 'attack', 0)}
   DEF:   {getattr(enemy, 'defense', 0)}
   ARM:   {e_arm}%   CRIT: {e_crit}%   DODGE: {e_dodge}%
""")

    def _create_bar(self, value, max_value):
        try:
            value = int(value)
            max_value = int(max_value)
        except (TypeError, ValueError):
            return "[" + "░" * self.bar_length + "]"

        if max_value <= 0:
            return "[" + "░" * self.bar_length + "]"

        value = max(0, min(value, max_value))
        filled_length = int(self.bar_length * value / max_value)
        empty_length = self.bar_length - filled_length
        return "[" + "█" * filled_length + "░" * empty_length + "]"
