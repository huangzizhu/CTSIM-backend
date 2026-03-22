from Strategy import Strategy
from StrategyContext import StrategyContext


class AbstractInputStrategy(Strategy):
    def __init__(self, name: str):
        super().__init__(name)


class FileInputStrategy(AbstractInputStrategy):
    def __init__(self, name: str, filePath: str):
        super().__init__(name)
        self.filePath = filePath

class InputStrategyContext(StrategyContext):
    def __init__(self, strategy: AbstractInputStrategy):
        super().__init__(strategy)

