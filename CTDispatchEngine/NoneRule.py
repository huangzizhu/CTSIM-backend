from CTDispatchEngine.RuleBase import RuleBase
from CTDispatchEngine.RuleDataBase import RuleDataBase
from CTDispatchEngine.RuleEngineContext import RuleEngineContext


class NoneRule(RuleBase):
    def __init__(self):
        super().__init__("NoneRule", 100)

    def evaluate(self, data: RuleDataBase, context: RuleEngineContext) -> RuleEngineContext:
        context.participatedRules.append(self)
        return context