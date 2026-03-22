from abc import ABC, abstractmethod

from RuleDataBase import RuleDataBase
from RuleEngineContext import RuleEngineContext


class RuleBase(ABC):

    def __init__(self, ruleName: str, priority: int):
        self.ruleName: str = ruleName
        self.priority: int = priority

    @abstractmethod
    def evaluate(self, data: RuleDataBase, context:RuleEngineContext) -> RuleEngineContext:
        pass
