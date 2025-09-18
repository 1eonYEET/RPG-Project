# systems/run_tracker.py
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Literal, Optional

RunSortKey = Literal["kills", "gold", "level", "name", "class"]

DATA_DIR = Path("data")
RUNS_FILE = DATA_DIR / "runs.jsonl"


@dataclass
class RunRecord:
    name: str            # Spielername
    klass: str           # gewählte Klasse/Archetyp (z. B. "Tank")
    gold: int            # gesammeltes Gold am Run-Ende
    level: int           # Spielerlevel am Run-Ende
    kills: int           # Anzahl getöteter Gegner
    dt: str              # ISO Zeitstempel (nur Anzeigezweck)

    @staticmethod
    def from_dict(d: dict) -> "RunRecord":
        # Rückwärtskompatibel laden (fehlende Felder abfedern)
        return RunRecord(
            name=d.get("name", "Unbekannt"),
            klass=d.get("klass", d.get("class", "Unbekannt")),
            gold=int(d.get("gold", 0)),
            level=int(d.get("level", 1)),
            kills=int(d.get("kills", 0)),
            dt=d.get("dt", datetime.utcnow().isoformat(timespec="seconds"))
        )


class RunTracker:
    def __init__(self, file_path: Path = RUNS_FILE):
        self.file_path = file_path
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.touch()

    def log_run(self, record: RunRecord) -> None:
        """Hängt einen Run als JSON-Linie an."""
        with self.file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")

    def load_runs(self) -> List[RunRecord]:
        runs: List[RunRecord] = []
        if not self.file_path.exists():
            return runs
        with self.file_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    runs.append(RunRecord.from_dict(json.loads(line)))
                except Exception:
                    # verschlucke fehlerhafte Zeilen statt alles zu brechen
                    continue
        return runs

    def leaderboard(
        self,
        sort_by: RunSortKey = "kills",
        limit: int = 10,
        desc: bool = True,
        filter_klass: Optional[str] = None
    ) -> List[RunRecord]:
        """Sortiert Runs nach gewünschtem Schlüssel; optional nach Klasse filtern."""
        runs = self.load_runs()
        if filter_klass:
            runs = [r for r in runs if r.klass.lower() == filter_klass.lower()]

        key_funcs = {
            "kills": lambda r: (r.kills, r.gold, r.level, r.name.lower()),
            "gold":  lambda r: (r.gold, r.kills, r.level, r.name.lower()),
            "level": lambda r: (r.level, r.kills, r.gold, r.name.lower()),
            "name":  lambda r: (r.name.lower(), r.kills, r.gold, r.level),
            "klass": lambda r: (r.klass.lower(), r.kills, r.gold, r.level),
        }
        key_fn = key_funcs.get(sort_by, key_funcs["kills"])
        runs.sort(key=key_fn, reverse=desc)
        return runs[:limit]

    def print_leaderboard(
        self,
        sort_by: RunSortKey = "kills",
        limit: int = 10,
        desc: bool = True,
        filter_klass: Optional[str] = None
    ) -> None:
        rows = self.leaderboard(sort_by=sort_by, limit=limit, desc=desc, filter_klass=filter_klass)
        title = f"🏆 Leaderboard (Sort: {sort_by}{'↓' if desc else '↑'}"
        if filter_klass:
            title += f", Klasse: {filter_klass}"
        title += ")"

        # Spaltenbreiten dynamisch
        name_w = max(4, *(len(r.name) for r in rows), default=4)
        klass_w = max(5, *(len(r.klass) for r in rows), default=5)

        print("\n" + title)
        print("─" * (name_w + klass_w + 28))
        print(f"{'Platz':<5} {'Name':<{name_w}}  {'Klasse':<{klass_w}}  {'Kills':>5}  {'Gold':>5}  {'Lvl':>3}  {'Datum'}")
        print("-" * (name_w + klass_w + 28))
        for i, r in enumerate(rows, start=1):
            print(f"{i:<5} {r.name:<{name_w}}  {r.klass:<{klass_w}}  {r.kills:>5}  {r.gold:>5}  {r.level:>3}  {r.dt}")
        print()
