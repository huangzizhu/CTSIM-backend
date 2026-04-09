# simulationState.py
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
# 假设实体类已导入，这里为了类型检查进行简写，实际开发中需 from ... import ...
from pojo.CTOrder import CTOrder


class CTUnitStatus(BaseModel):
    """
    单个CT设备在模拟环境中的状态
    """
    ctId: int
    deviceName: str
    status: str  # 'IDLE' 或 'BUSY'
    currentOrder: Optional[CTOrder] = None  # 当前正在扫描的订单
    queue: List[CTOrder] = []  # 当前排队中的订单列表

    class Config:
        arbitrary_types_allowed = True


class SimulationSnapshot(BaseModel):
    """
    模拟环境快照，用于持久化存储
    """
    # 快照对应的模拟时间
    simTime: datetime

    # 所有CT的状态映射：Key为ctId, Value为CT状态对象
    ctStatusMap: Dict[int, CTUnitStatus] = {}

    # 版本控制哈希，用于乐观锁判断
    versionHash: str = ""

    # 操作日志，记录每一次调度、插入、完成事件，供数据分析
    operationLogs: List[Dict] = []

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }