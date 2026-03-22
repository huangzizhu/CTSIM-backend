from abc import ABC, abstractmethod


class RuleDataBase(ABC):
    def __init__(self, name: str):
        self.name: str = name
