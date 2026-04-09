from typing import List

from CTDispatchEngine.PatientData import PatientData
from CTDispatchEngine.RuleBase import RuleBase
from CTDispatchEngine.RuleEngineContext import RuleEngineContext



class RuleEngine:
    def __init__(self):
        self.rules: List[RuleBase] = []

    def registerRule(self, rule: RuleBase):
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority)

    def removeRule(self, ruleName: str):
        self.rules = [rule for rule in self.rules if rule.ruleName != ruleName]

    def evaluate(self, data: PatientData) -> RuleEngineContext:
        context: RuleEngineContext = RuleEngineContext()
        for rule in self.rules:
            rule.evaluate(data, context)
            if context.isFinished:
                return context
        return context
