# skilltree/effects.py
from skilltree.schema import AddStatsEffect, AddSkillEffect, EffectSpec
from skills.skill_factory import SkillFactory


def _fmt_pct(x: float) -> str:
    return f"{int(round(x * 100))}%"


class EffectApplier:
    """
    Kapselt die Anwendung von Effekten (SRP) + nicht-mutierende Vorschau.
    Achtet auf Caps: armor ≤ 0.8, crit ≤ 1.0, dodge ≤ 0.6.
    """

    # ---------- Vorschau (mutiert NICHT) ----------
    def preview(self, player, effect: EffectSpec):
        """
        Liefert eine Liste beschreibender Strings wie:
        ['ATK: 12 -> 15', 'Rüstung: 10% -> 13%'].
        Für AddSkillEffect: ['Neue Fähigkeit: ... — Beschreibung (Kosten: X Mana)'].
        """
        lines = []
        if isinstance(effect, AddStatsEffect):
            # einfache Stats
            if effect.hp:
                cur = getattr(player, "max_hp", 0)
                lines.append(f"Max-HP: {cur} -> {cur + effect.hp}")
            if effect.attack:
                cur = getattr(player, "attack", 0)
                lines.append(f"ATK: {cur} -> {cur + effect.attack}")
            if effect.defense:
                cur = getattr(player, "defense", 0)
                lines.append(f"DEF: {cur} -> {cur + effect.defense}")
            if effect.mana:
                cur = getattr(player, "max_mana", 0)
                lines.append(f"Max-Mana: {cur} -> {cur + effect.mana}")

            # prozentuale/capped Werte
            if effect.armor_add:
                cur = getattr(player, "armor", 0.0)
                new = min(0.8, cur + effect.armor_add)
                lines.append(f"Rüstung: {_fmt_pct(cur)} -> {_fmt_pct(new)}")
            if effect.crit_add:
                cur = getattr(player, "crit_chance", 0.0)
                new = min(1.0, cur + effect.crit_add)
                lines.append(f"Krit: {_fmt_pct(cur)} -> {_fmt_pct(new)}")
            if effect.dodge_add:
                cur = getattr(player, "dodge_chance", 0.0)
                new = min(0.6, cur + effect.dodge_add)
                lines.append(f"Ausweichen: {_fmt_pct(cur)} -> {_fmt_pct(new)}")

            if effect.spell_power:
                cur = getattr(player, "spell_power", 0.0)
                lines.append(f"Zauberkraft: {cur:.2f} -> {cur + effect.spell_power:.2f}")
            if effect.heal_power:
                cur = getattr(player, "heal_power", 0.0)
                lines.append(f"Heilbonus: {cur:.2f} -> {cur + effect.heal_power:.2f}")

        elif isinstance(effect, AddSkillEffect):
            try:
                skill = SkillFactory.create(effect.skill_name)
                desc = skill.get_description() if hasattr(skill, "get_description") else ""
                cost = getattr(skill, "mana_cost", None)
                if desc and cost is not None:
                    lines.append(
                        f"Neue Fähigkeit: {skill.get_name()} — {desc} (Kosten: {cost} Mana)"
                    )
                elif desc:
                    lines.append(f"Neue Fähigkeit: {skill.get_name()} — {desc}")
                else:
                    lines.append(f"Neue Fähigkeit: {skill.get_name()}")
            except Exception:
                lines.append(f"Neue Fähigkeit: {effect.skill_name}")
        return lines

    # ---------- Anwenden (mutiert) ----------
    def apply(self, player, effect: EffectSpec, notifier):
        if isinstance(effect, AddStatsEffect):
            self._apply_stats(player, effect, notifier)
        elif isinstance(effect, AddSkillEffect):
            self._add_skill(player, effect, notifier)

    def _apply_stats(self, p, e: AddStatsEffect, notifier):
        if e.hp:
            p.max_hp += e.hp
            p.hp += e.hp
            notifier.notify(f"❤️ Max-HP +{e.hp}")
        if e.attack:
            p.attack += e.attack
            notifier.notify(f"🗡️ Angriff +{e.attack}")
        if e.defense:
            p.defense += e.defense
            notifier.notify(f"🛡️ Verteidigung +{e.defense}")
        if e.mana:
            p.max_mana += e.mana
            p.mana += e.mana
            notifier.notify(f"🔷 Max-Mana +{e.mana}")

        # Prozentwerte mit Caps
        if e.armor_add:
            p.armor = min(0.8, p.armor + e.armor_add)
            notifier.notify(
                f"🛡️ Rüstung +{int(e.armor_add*100)}% (jetzt {int(p.armor*100)}%)"
            )
        if e.crit_add:
            p.crit_chance = min(1.0, p.crit_chance + e.crit_add)
            notifier.notify(
                f"🎯 Krit +{int(e.crit_add*100)}% (jetzt {int(p.crit_chance*100)}%)"
            )
        if e.dodge_add:
            p.dodge_chance = min(0.6, p.dodge_chance + e.dodge_add)
            notifier.notify(
                f"💨 Ausweichen +{int(e.dodge_add*100)}% (jetzt {int(p.dodge_chance*100)}%)"
            )

        if e.spell_power:
            p.spell_power += e.spell_power
            notifier.notify(f"🔮 Zauberkraft +{int(e.spell_power*100)}%")
        if e.heal_power:
            p.heal_power += e.heal_power
            notifier.notify(f"💖 Heilbonus +{int(e.heal_power*100)}%")

    def _add_skill(self, p, e: AddSkillEffect, notifier):
        skill = SkillFactory.create(e.skill_name)
        if any(s.get_name() == skill.get_name() for s in p.skills):
            notifier.notify(f"ℹ️ Fähigkeit {skill.get_name()} ist bereits freigeschaltet.")
            return
        p.skills.append(skill)
        notifier.notify(
            f"✨ Neue Fähigkeit freigeschaltet: {skill.get_name()} — {skill.get_description()}"
        )
