


class RuleEngineContext:

    def __init__(self):
        self.isFinished: bool = False  #是否结束判断
        self.score: int = 0  #危险程度，越高等级越高
        self.level: int = -1  #危险等级，-1表示未评估，0表示安全，1表示低风险，2表示中风险，3表示高风险
