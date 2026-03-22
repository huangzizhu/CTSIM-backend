import Strategy
from StrategyContext import StrategyContext


class AbstractOutputStrategy(Strategy):
    def __init__(self, name: str):
        super().__init__(name)

class FileOutputStrategy(AbstractOutputStrategy):
    def __init__(self, name: str, filePath: str):
        super().__init__(name)
        self.filePath = filePath

class OutputStrategyContext(StrategyContext):
    def __init__(self, strategy: AbstractOutputStrategy):
        super().__init__(strategy)
