from abc import ABC, abstractmethod

class Skill(ABC):
    def __init__(self, name: str, mana_cost: int):
        self.name = name
        self.mana_cost = mana_cost

    @abstractmethod
    def use(self, user, target, logger):
        pass

    def get_name(self):
        return self.name
