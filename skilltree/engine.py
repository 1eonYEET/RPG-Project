# skilltree/engine.py
from typing import List
from skilltree.repo import SkillTreeRepository
from skilltree.schema import NodeOption
from skilltree.effects import EffectApplier

class SkillTreeEngine:
    """
    Ermittelt die wählbaren Optionen bei Level-Up, zeigt Vorher→Nachher,
    prüft Requirements und wendet den Effekt an.
    """
    def __init__(self, repo: SkillTreeRepository = None):
        self.repo = repo or SkillTreeRepository()
        self.applier = EffectApplier()

    def get_choices(self, player) -> List[NodeOption]:
        opts = self.repo.options_for(getattr(player, "archetype", "generic"), player.level)
        unlocked = set(getattr(player, "unlocked_nodes", []))
        def req_ok(n: NodeOption) -> bool:
            return all(r in unlocked for r in n.requires)
        return [n for n in opts if n.id not in unlocked and req_ok(n)]

    def present_and_apply(self, player, notifier, input_fn=input):
        choices = self.get_choices(player)
        if not choices:
            notifier.notify("ℹ️ Keine Skilltree-Optionen auf diesem Level verfügbar.")
            return

        print("\n🌿 Skilltree – wähle EINE Option:")
        for i, c in enumerate(choices, start=1):
            # Vorher→Nachher-Previews pro Option
            preview_lines = self.applier.preview(player, c.effect) if c.effect else []
            preview = " | ".join(preview_lines) if preview_lines else ""
            suffix = f"  ({preview})" if preview else ""
            print(f"{i}. {c.name} — {c.desc}{suffix}")

        try:
            idx = int(input_fn("Deine Wahl: ").strip()) - 1
            pick = choices[idx]
        except (ValueError, IndexError):
            notifier.notify("❌ Ungültige Auswahl. Kein Skilltree-Bonus vergeben.")
            return

        # Anwenden
        if pick.effect:
            self.applier.apply(player, pick.effect, notifier)

        if not hasattr(player, "unlocked_nodes"):
            player.unlocked_nodes = []
        player.unlocked_nodes.append(pick.id)

        notifier.notify(f"✅ Gewählt: {pick.name}")
