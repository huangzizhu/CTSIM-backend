from CTDispatchEngine.RuleBase import RuleBase
from CTDispatchEngine.PatientData import PatientData
from CTDispatchEngine.RuleEngineContext import RuleEngineContext


class NoneRule(RuleBase):
    def __init__(self):
        super().__init__("NoneRule", 100)

    def evaluate(self, data: PatientData, context: RuleEngineContext) -> RuleEngineContext:
        context.score = 100
        context.isFinished = True
        return context