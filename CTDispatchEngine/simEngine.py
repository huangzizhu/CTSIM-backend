# simEngine.py
import simpy
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from pojo.CTOrder import CTOrder, StatusEnum, PriorityEnum
from CTDispatchEngine.SimulationState import SimulationSnapshot, CTUnitStatus


class SimEngine:
    """
    SimPy模拟引擎封装类
    """

    def __init__(self, snapshot: SimulationSnapshot):
        # SimPy环境
        self.env: simpy.Environment = simpy.Environment()
        # 状态快照引用
        self.snapshot: SimulationSnapshot = snapshot
        # 存储每个CT的结束事件，用于中断控制
        self.scanProcesses: Dict[int, simpy.events.Process] = {}

        # 初始化环境：重建正在进行的扫描进程
        self._initializeRunningTasks()

    def _initializeRunningTasks(self) -> None:
        """
        根据快照恢复现场：如果有CT正在扫描，重建对应的timeout进程
        """
        for ctId, ctStatus in self.snapshot.ctStatusMap.items():
            if ctStatus.status == 'BUSY' and ctStatus.currentOrder:
                order = ctStatus.currentOrder
                # 计算剩余时间
                remainingTime = self._calculateRemainingTime(order)
                if remainingTime > 0:
                    # 启动扫描进程
                    self.scanProcesses[ctId] = self.env.process(self._scanProcess(ctId, order, remainingTime))

    def _calculateRemainingTime(self, order: CTOrder) -> float:
        """
        计算订单剩余扫描时间（分钟）
        """
        now: datetime = self.snapshot.simTime
        # 假设 startTime 不为空，且 expectedDuration 存在
        if order.startTime and order.expectedDuration:
            endTime = order.startTime + timedelta(minutes=order.expectedDuration)
            delta: timedelta = endTime - now
            return max(0, delta.total_seconds() / 60.0)
        return 0.0

    def _scanProcess(self, ctId: int, order: CTOrder, duration: float) -> None:
        """
        模拟扫描过程
        """
        try:
            yield self.env.timeout(duration)
            # 扫描完成，触发回调更新状态
            self._onScanComplete(ctId, order)
        except simpy.Interrupt:
            # 被中断（例如人工干预或现实校正）
            print(f"CT {ctId} scan interrupted for Order {order.orderId}")

    def _onScanComplete(self, ctId: int, completedOrder: CTOrder) -> None:
        """
        扫描完成时的内部处理逻辑
        """
        ctStatus: Optional[CTUnitStatus] = self.snapshot.ctStatusMap.get(ctId)
        if not ctStatus:
            return

        # 1. 更新订单状态
        completedOrder.status = StatusEnum.COMPLETED
        completedOrder.endTime = self.snapshot.simTime + timedelta(minutes=self.env.now)

        # 2. 记录日志
        self.snapshot.operationLogs.append({
            "type": "SCAN_COMPLETE",
            "orderId": completedOrder.orderId,
            "ctId": ctId,
            "time": (self.snapshot.simTime + timedelta(minutes=self.env.now)).isoformat()
        })

        # 3. 检查队列是否有下一个病人
        if ctStatus.queue:
            nextOrder: CTOrder = ctStatus.queue.pop(0)  # 取出队首
            self._startScan(ctId, nextOrder)
        else:
            # 队列为空，CT变为空闲
            ctStatus.status = 'IDLE'
            ctStatus.currentOrder = None

    def _startScan(self, ctId: int, order: CTOrder) -> None:
        """
        开始扫描某个订单
        """
        ctStatus: CTUnitStatus = self.snapshot.ctStatusMap[ctId]

        # 更新状态
        order.status = StatusEnum.SCANNING
        order.startTime = self.snapshot.simTime + timedelta(minutes=self.env.now)
        ctStatus.status = 'BUSY'
        ctStatus.currentOrder = order

        # 启动SimPy进程
        duration: float = float(order.expectedDuration if order.expectedDuration else 10)  # 默认10分钟防错
        self.scanProcesses[ctId] = self.env.process(self._scanProcess(ctId, order, duration))

    def runUntil(self, targetTime: datetime) -> None:
        """
        将模拟运行直到指定的目标时间
        """
        currentTime: datetime = self.snapshot.simTime
        if targetTime <= currentTime:
            return

        # 计算需要推进的分钟数
        deltaMinutes: float = (targetTime - currentTime).total_seconds() / 60.0

        # 更新快照时间基准
        self.snapshot.simTime = targetTime

        # 运行SimPy环境
        # 注意：这里不能简单用 run(deltaMinutes)，因为我们需要支持多次 runUntil 调用
        # SimPy 的 env.run(until=relative_time) 是基于 env.now 的
        # 我们需要将绝对时间差转换为相对时间
        try:
            self.env.run(until=self.env.now + deltaMinutes)
        except Exception as e:
            print(f"Simulation error: {e}")

    def addToQueue(self, ctId: int, order: CTOrder) -> None:
        """
        将订单加入指定CT的队列，并尝试触发扫描
        """
        ctStatus: CTUnitStatus = self.snapshot.ctStatusMap[ctId]

        # 加入队列并排序
        # 优先级数值越大越优先，StatusEnum通常数值越小越优先？参考PriorityEnum定义
        # PriorityEnum: NORMAL=0, EMERGENCY=1, VIP=2
        # 我们按优先级降序排列
        ctStatus.queue.append(order)
        ctStatus.queue.sort(key=lambda x: x.priority, reverse=True)

        # 记录日志
        self.snapshot.operationLogs.append({
            "type": "ENQUEUE",
            "orderId": order.orderId,
            "ctId": ctId,
            "time": self.snapshot.simTime.isoformat()
        })

        # 如果CT空闲，立即开始（在当前时间点触发）
        if ctStatus.status == 'IDLE':
            self._startScan(ctId, ctStatus.queue.pop(0))

    def manualInsert(self, ctId: int, order: CTOrder, position: int) -> None:
        """
        人工插队
        """
        ctStatus: CTUnitStatus = self.snapshot.ctStatusMap[ctId]

        # 插入到指定位置
        actualPos: int = max(0, min(position, len(ctStatus.queue)))
        ctStatus.queue.insert(actualPos, order)

        # 记录日志
        self.snapshot.operationLogs.append({
            "type": "MANUAL_INSERT",
            "orderId": order.orderId,
            "ctId": ctId,
            "position": actualPos,
            "time": self.snapshot.simTime.isoformat()
        })

        # 如果插入到队首且CT空闲，尝试启动
        if actualPos == 0 and ctStatus.status == 'IDLE' and len(ctStatus.queue) > 0:
            self._startScan(ctId, ctStatus.queue.pop(0))