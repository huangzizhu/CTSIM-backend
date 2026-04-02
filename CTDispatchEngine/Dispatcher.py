from CTDispatchEngine.NoneRule import NoneRule
from RuleEngine import RuleEngine

class Dispatcher:
    def __init__(self):
        self.ruleEngine = RuleEngine()
        self.ruleEngine.registerRule(NoneRule())  # Register the default NoneRule

    def dispatchPatients(self, patients):
        pass

    模拟器