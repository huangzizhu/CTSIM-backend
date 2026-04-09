# simulatorService.py
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel

# 导入实体类和之前的模块
from pojo.CT import CT
from pojo.CTOrder import CTOrder, CTOrderCreate, StatusEnum
from pojo.Patient import Patient
from pojo.Visit import Visit
from RuleEngine import RuleEngine
from RuleEngineContext import RuleEngineContext
from CTDispatchEngine.SimulationState import SimulationSnapshot, CTUnitStatus
from CTDispatchEngine.simEngine import SimEngine
from CTDispatchEngine.PatientData import PatientData

class SimulatorService:
    def __init__(self, stateFilePath: str = "./simulation_state.json"):
        self.stateFilePath: str = stateFilePath
        self.currentSnapshot: Optional[SimulationSnapshot] = None
        self.ruleEngine: RuleEngine = RuleEngine()  # 假设已初始化规则

    def _loadState(self) -> SimulationSnapshot:
        """
        从文件恢复现场，如果文件不存在则创建默认现场
        """
        try:
            with open(self.stateFilePath, 'r', encoding='utf-8') as f:
                data: Dict = json.load(f)
                snapshot: SimulationSnapshot = SimulationSnapshot.parse_obj(data)
                return snapshot
        except (FileNotFoundError, json.JSONDecodeError):
            # 初始化默认状态
            print("No state file found or invalid file. Initializing new state.")
            return SimulationSnapshot(simTime=datetime.now())

    def _saveState(self) -> None:
        """
        持久化当前状态到文件，并更新哈希
        """
        if not self.currentSnapshot:
            return

        # 序列化时排除哈希字段以计算新哈希
        dataDict: Dict = self.currentSnapshot.dict(exclude={"versionHash"})
        jsonString: str = json.dumps(dataDict, default=str, sort_keys=True)

        # 计算哈希
        newHash: str = hashlib.sha256(jsonString.encode('utf-8')).hexdigest()
        self.currentSnapshot.versionHash = newHash

        # 写入文件
        with open(self.stateFilePath, 'w', encoding='utf-8') as f:
            f.write(self.currentSnapshot.model_dump_json(indent=2))

    def _initCTIfAbsent(self, ctId: int, deviceName: str) -> None:
        """
        辅助函数：确保CT存在于状态映射中
        """
        if not self.currentSnapshot:
            return
        if ctId not in self.currentSnapshot.ctStatusMap:
            self.currentSnapshot.ctStatusMap[ctId] = CTUnitStatus(
                ctId=ctId,
                deviceName=deviceName,
                status='IDLE',
                queue=[]
            )

    def getSimulationStatus(self, queryTime: datetime) -> SimulationSnapshot:
        """
        接口：查询指定时间点的模拟状态
        逻辑：加载 -> 运行 -> 返回
        """
        # 1. 加载状态
        self.currentSnapshot = self._loadState()

        # 2. 创建引擎并运行到目标时间
        engine: SimEngine = SimEngine(self.currentSnapshot)
        engine.runUntil(queryTime)

        # 3. 更新快照时间并持久化
        self.currentSnapshot.simTime = queryTime
        self._saveState()

        return self.currentSnapshot

    def addPatient(self, patient: Patient, visit: Visit, ctList: List[CT]) -> CTOrder:
        """
        接口：新增病人并自动调度
        """
        # 1. 恢复现场
        self.currentSnapshot = self._loadState()

        # 2. 调用规则引擎获取上下文
        context: RuleEngineContext = self.ruleEngine.evaluate(PatientData('data', patient, visit))
        priority: int = context.score if context.score > 0 else 0  # 简化逻辑

        # 3. 随机/策略选择CT
        import random
        targetCt: CT = random.choice(ctList)
        self._initCTIfAbsent(targetCt.ctId, targetCt.deviceName)

        # 4. 构建 Order
        newOrder: CTOrder = CTOrder(
            orderId=random.randint(1000, 9999),  # 实际应由数据库生成
            patientId=patient.pid,
            visitId=visit.visitId,
            ctId=targetCt.ctId,
            status=StatusEnum.QUEUING,
            scheduledTime=datetime.now(),
            priority=priority,
            expectedDuration=50,
            queueEnterTime=None,
            startTime=None,
            endTime=None,
            actualDuration=None,
            isEmergency=False,
            notes=None,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
            canceledAt=None
        )

        # 5. 放入引擎
        engine: SimEngine = SimEngine(self.currentSnapshot)
        engine.addToQueue(targetCt.ctId, newOrder)

        # 6. 持久化
        self._saveState()

        return newOrder

    def manualSchedule(self, orderId: int, targetCtId: int, position: int, orderDetails: CTOrder) -> bool:
        """
        接口：人工干预，插队
        """
        self.currentSnapshot = self._loadState()

        engine: SimEngine = SimEngine(self.currentSnapshot)

        # 确保目标CT存在
        self._initCTIfAbsent(targetCtId, f"CT-{targetCtId}")

        # 构建订单 (这里假设外部传入完整的订单对象)
        # 如果订单已在其他队列，需要先移除 (简化逻辑，假设是外部移动)
        engine.manualInsert(targetCtId, orderDetails, position)

        self._saveState()
        return True

    def updateRealityStatus(self, orderId: int, realStatus: int, realEndTime: Optional[datetime]) -> bool:
        """
        接口：根据现实修正模拟状态
        """
        self.currentSnapshot = self._loadState()
        engine: SimEngine = SimEngine(self.currentSnapshot)
        # 查找该订单所在的CT
        foundCtId: Optional[int] = None
        foundOrder: Optional[CTOrder] = None

        for ctId, ctStatus in self.currentSnapshot.ctStatusMap.items():
            # 检查正在扫描的
            if ctStatus.currentOrder and ctStatus.currentOrder.orderId == orderId:
                foundCtId = ctId
                foundOrder = ctStatus.currentOrder
                break
            # 检查队列里的
            for o in ctStatus.queue:
                if o.orderId == orderId:
                    foundCtId = ctId
                    foundOrder = o
                    break

        if not foundCtId:
            print("Order not found in simulation.")
            return False

        # 模拟修正逻辑：
        # 如果现实中已完成，而模拟中还在扫描或排队，强制完成
        if realStatus == StatusEnum.COMPLETED:
            ctStatus = self.currentSnapshot.ctStatusMap[foundCtId]

            # 如果在队列中，直接移除
            if foundOrder in ctStatus.queue:
                ctStatus.queue.remove(foundOrder)

            # 如果正在扫描，需要强制结束进程
            if ctStatus.currentOrder and ctStatus.currentOrder.orderId == orderId:
                # 中断SimPy进程
                if foundCtId in engine.scanProcesses:
                    proc = engine.scanProcesses[foundCtId]
                    if proc.is_alive:
                        proc.interrupt("RealityUpdate")

                # 更新状态
                ctStatus.status = 'IDLE'
                ctStatus.currentOrder = None

                # 检查是否有排队的人，立即开始下一个（如果有）
                if ctStatus.queue:
                    nextOrder = ctStatus.queue.pop(0)
                    engine._startScan(foundCtId, nextOrder)

            # 记录修正日志
            self.currentSnapshot.operationLogs.append({
                "type": "REALITY_UPDATE",
                "orderId": orderId,
                "time": datetime.now().isoformat()
            })

            self._saveState()
            return True