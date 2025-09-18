# skills/skill.py
class Skill:
    def __init__(self, name: str, mana_cost: int = 0, description: str = ""):
        self._name = name
        self.mana_cost = mana_cost
        self._description = description  # neu

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description or ""
