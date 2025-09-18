# skilltree/repo.py
import json
from pathlib import Path
from typing import Dict, List
from skilltree.schema import NodeOption, AddStatsEffect, AddSkillEffect

class SkillTreeRepository:
    def __init__(self, json_path: str = "data/skilltree.json"):
        self.json_path = Path(json_path)
        self._index: Dict[str, List[NodeOption]] = {}
        self._load()

    def _load(self):
        data = json.loads(self.json_path.read_text(encoding="utf-8"))
        index: Dict[str, List[NodeOption]] = {}
        for archetype, levels in data.items():
            for level_str, options in levels.items():
                level = int(level_str)
                for opt in options:
                    effect = None
                    if "effect" in opt:
                        eff = opt["effect"]
                        if "add_stats" in eff:
                            effect = AddStatsEffect(**eff["add_stats"])
                        elif "add_skill" in eff:
                            effect = AddSkillEffect(skill_name=eff["add_skill"])

                    node = NodeOption(
                        id=opt["id"],
                        name=opt["name"],
                        desc=opt.get("desc", ""),
                        level=level,
                        archetype=archetype,
                        requires=opt.get("requires", []),
                        effect=effect
                    )
                    index.setdefault(archetype, []).append(node)
        self._index = index

    def options_for(self, archetype: str, level: int) -> List[NodeOption]:
        """
        Liefert alle Optionen für (archetype, level) inkl. 'generic' an diesem Level.
        """
        res = [n for n in self._index.get("generic", []) if n.level == level]
        if archetype in self._index:
            res += [n for n in self._index[archetype] if n.level == level]
        return res
