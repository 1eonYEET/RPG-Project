# systems/run_tracker.py
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Literal, Optional

RunSortKey = Literal["kills", "total_gold", "level", "name", "klass"]

DATA_DIR = Path("data")
RUNS_FILE = DATA_DIR / "runs.jsonl"


@dataclass
class RunRecord:
    name: str             # Spielername
    klass: str            # gewählte Klasse/Archetyp
    total_gold: int       # ✅ gesamtes verdientes Gold im Run
    level: int            # Level am Run-Ende
    kills: int            # Anzahl getöteter Gegner
    dt: str               # ISO Zeitstempel (nur Anzeige)

    @staticmethod
    def from_dict(d: dict) -> "RunRecord":
        """
        Rückwärtskompatibel laden:
        - alte Einträge hatten 'gold' = aktueller Bestand; wir interpretieren ihn als total_gold (best effort)
        """
        total = d.get("total_gold")
        if total is None:
            total = d.get("gold", 0)
        return RunRecord(
            name=d.get("name", "Unbekannt"),
            klass=d.get("klass", d.get("class", "Unbekannt")),
            total_gold=int(total),
            level=int(d.get("level", 1)),
            kills=int(d.get("kills", 0)),
            dt=d.get("dt", datetime.utcnow().isoformat(timespec="seconds")),
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
                    continue
        return runs

    def leaderboard(
        self,
        sort_by: RunSortKey = "kills",
        limit: int = 10,
        desc: bool = True,
        filter_klass: Optional[str] = None
    ) -> List[RunRecord]:
        runs = self.load_runs()
        if filter_klass:
            runs = [r for r in runs if r.klass.lower() == filter_klass.lower()]

        key_funcs = {
            "kills":       lambda r: (r.kills, r.total_gold, r.level, r.name.lower()),
            "total_gold":  lambda r: (r.total_gold, r.kills, r.level, r.name.lower()),
            "level":       lambda r: (r.level, r.kills, r.total_gold, r.name.lower()),
            "name":        lambda r: (r.name.lower(), r.kills, r.total_gold, r.level),
            "klass":       lambda r: (r.klass.lower(), r.kills, r.total_gold, r.level),
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

        # Spaltenbreiten robust berechnen (keine default-Arg-Kollisionen)
        name_w = max([4] + [len(r.name) for r in rows]) if rows else 4
        klass_w = max([5] + [len(r.klass) for r in rows]) if rows else 5

        print("\n" + title)
        print("─" * (name_w + klass_w + 34))
        print(f"{'Platz':<5} {'Name':<{name_w}}  {'Klasse':<{klass_w}}  {'Kills':>5}  {'GoldΣ':>7}  {'Lvl':>3}  {'Datum'}")
        print("-" * (name_w + klass_w + 34))
        for i, r in enumerate(rows, start=1):
            print(f"{i:<5} {r.name:<{name_w}}  {r.klass:<{klass_w}}  {r.kills:>5}  {r.total_gold:>7}  {r.level:>3}  {r.dt}")
        print()
