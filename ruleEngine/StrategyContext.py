import Strategy


class StrategyContext:

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def setStrategy(self, strategy: Strategy):
        self._strategy = strategy
