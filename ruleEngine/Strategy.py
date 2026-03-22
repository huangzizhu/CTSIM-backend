from abc import ABC, abstractmethod
class Strategy(ABC):

    def __init__(self, name: str) -> None:
        self.name: str = name
