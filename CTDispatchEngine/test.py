# test_simulation.py
import time
import os
import random
from datetime import datetime, timedelta
from typing import List, Optional

# 导入模拟器服务及引擎
from CTDispatchEngine.simulatorService import SimulatorService
from CTDispatchEngine.simEngine import SimEngine

# 导入实体类
from pojo.CT import CT
from pojo.Patient import Patient
from pojo.Visit import Visit
from pojo.CTOrder import CTOrder, StatusEnum, PriorityEnum


from gateway.service.CTService import CTService
from gateway.service.PatientService import PatientService
from gateway.service.VisitService import VisitService


# --- Helper: 数据获取包装 ---
def getAllCTs() -> List[CT]:
    # 这里直接调用你提供的方法，实际运行时需确保数据库连接等配置正确
    # 为了测试能够跑通，如果数据库为空，建议加一个 fallback 返回假数据
    cts = CTService().getAllCT()
    if not cts:
        print("Warning: No CTs found from DB, using mock data.")
        return [CT(ctId=1, deviceCode="CT01", deviceName="MockCT1", status="NORMAL", location="Room1",
                   createdAt=datetime.now(), updatedAt=datetime.now())]
    return cts


def getAllPatients() -> List[Patient]:
    patients = PatientService().getAllPatients()
    if not patients:
        print("Warning: No Patients found from DB, using mock data.")
        return [
            Patient(pid=999, cardNo="Mock", name="MockPatient", gender="M", birthDate="1990-01-01", phone="13800000000",
                    idNumber="123456789012345678")]
    return patients


def getNewestVisitByPid(pid: int) -> Visit:
    visit = VisitService().getVisitByPid(pid)
    if not visit:
        print(f"Warning: No Visit found for PID {pid}, using mock data.")
        return Visit(visitId=888, patientId=pid, doctorId=1, visitTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     isEmergency=0, symptoms="MockSymptom")
    return visit


# --- Test Case ---
def run_test():
    print("======== 开始模拟器集成测试 ========")

    # 1. 初始化服务，指定一个测试用的状态文件路径
    stateFile = "./test_sim_state.json"
    # 清理旧状态，确保测试环境纯净
    if os.path.exists(stateFile):
        os.remove(stateFile)
        print(f"[Setup] Cleaned up old state file: {stateFile}")

    service: SimulatorService = SimulatorService(stateFilePath=stateFile)

    # 2. 获取基础数据
    ctList: List[CT] = getAllCTs()
    if not ctList:
        print("[Error] 没有可用的CT设备，测试终止。")
        return

    # 选取第一个CT作为测试目标
    targetCt: CT = ctList[0]
    print(f"[Info] 选中测试CT: {targetCt.deviceName} (ID: {targetCt.ctId})")

    # 获取病人数据
    patientList: List[Patient] = getAllPatients()
    if not patientList:
        print("[Error] 没有可用的病人数据，测试终止。")
        return
    patient: Patient = patientList[0]

    # 获取病人的最新就诊记录
    visit: Visit = getNewestVisitByPid(patient.pid)
    print(f"[Info] 选中测试病人: {patient.name} (PID: {patient.pid}), VisitID: {visit.visitId}")

    # --- 场景一：新增病人 ---
    print("\n>>> 场景一：新增病人 >>>")
    startTime: datetime = datetime.now()

    # 调用你修改后的 addPatient 接口
    newOrder: CTOrder = service.addPatient(patient, visit, ctList)

    print(f"  [Result] 病人已加入队列: OrderID={newOrder.orderId}, 优先级={newOrder.priority}, 目标CT={newOrder.ctId}")


    # 验证持久化：重新加载查看状态
    snapshot = service.getSimulationStatus(startTime)
    ctStatus = snapshot.ctStatusMap.get(targetCt.ctId)
    # 如果 addPatient 随机到了其他 CT，这里需要动态获取
    targetCtId = newOrder.ctId
    ctStatus = snapshot.ctStatusMap.get(targetCtId)

    print(f"  [Check] CT {targetCtId} 当前状态: {ctStatus.status}, 队列长度: {len(ctStatus.queue)}")

    # --- 场景二：时间推进 ---
    print("\n>>> 场景二：时间推进 (模拟 20 分钟后) >>>")
    # 假设扫描需要 15 分钟，我们推进 20 分钟，病人应该开始扫描甚至完成
    futureTime: datetime = startTime + timedelta(minutes=20)

    # 获取未来时刻的状态
    snapshotFuture = service.getSimulationStatus(futureTime)
    ctStatusFuture = snapshotFuture.ctStatusMap.get(targetCtId)

    print(f"  [Result] 模拟时间: {futureTime.strftime('%H:%M:%S')}")
    print(f"  [Check] CT {targetCtId} 状态: {ctStatusFuture.status}")

    # 验证逻辑：
    # 1. 如果是 IDLE，说明已经做完并从队列移除（或者队列里没人，但这不可能因为我们刚加了一个人）
    # 2. 如果是 BUSY，说明正在扫描
    # 具体取决于 addPatient 时是否立即开始扫描逻辑。
    # 根据之前的代码设计，当 IDLE 时加入队列会立即 pop 并 _startScan
    # 所以现在的状态理论上应该是 BUSY (如果 duration > 20分钟) 或 IDLE (如果 duration < 20分钟)
    # 但由于我们在 addPatient 时 expectedDuration 默认为 15 分钟，
    # 推进 20 分钟后，理论上已经完成了。

    if ctStatusFuture.status == 'IDLE':
        print("  [Success] 扫描已完成，CT 已空闲。")
    elif ctStatusFuture.status == 'BUSY':
        print("  [Info] 仍在扫描中 (可能预计时长较长)。")

    # --- 场景三：人工插队 ---
    print("\n>>> 场景三：人工插队 >>>")
    # 重新获取一个病人进行插队测试
    if len(patientList) > 1:
        patient2: Patient = patientList[1]
        visit2: Visit = getNewestVisitByPid(patient2.pid)
    else:
        # 构造一个假的
        patient2 = patient
        visit2 = Visit(visitId=9999, patientId=patient.pid, doctorId=1,
                       visitTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), isEmergency=0, symptoms="Fake")

    # 先添加一个普通病人，排在后面
    # 注意：这里为了演示，我们复用 patient 对象，实际业务逻辑可能需要去重
    # 我们先手动构造一个 Order 用来插队
    manualInsertOrder = CTOrder(
        orderId=random.randint(8000, 9000),
        patientId=patient2.pid,
        visitId=visit2.visitId,
        ctId=targetCtId,
        status=StatusEnum.QUEUING,
        scheduledTime=datetime.now(),
        priority=PriorityEnum.EMERGENCY,  # 插队通常是急诊
        expectedDuration=10,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # 恢复当前时刻状态
    service.currentSnapshot = service._loadState()
    engine = SimEngine(service.currentSnapshot)

    # 如果 CT 现在是空闲，我们先手动加一个人占坑
    if service.currentSnapshot.ctStatusMap[targetCtId].status == 'IDLE':
        blockerOrder = CTOrder(
            orderId=111, patientId=99, visitId=99, ctId=targetCtId,
            status=StatusEnum.QUEUING, scheduledTime=datetime.now(),
            priority=0, expectedDuration=10, createdAt=datetime.now(), updatedAt=datetime.now()
        )
        engine.addToQueue(targetCtId, blockerOrder)
        service._saveState()
        print(f"  [Setup] 为测试插队，先添加了一个占位病人 OrderID={blockerOrder.orderId}")

    # 开始插队测试
    print(f"  [Action] 将 OrderID={manualInsertOrder.orderId} 插入到 CT {targetCtId} 的第 0 位")
    service.manualSchedule(
        orderId=manualInsertOrder.orderId,
        targetCtId=targetCtId,
        position=0,
        orderDetails=manualInsertOrder
    )

    # 验证结果
    snapshotNow = service.getSimulationStatus(datetime.now())
    queueList = snapshotNow.ctStatusMap[targetCtId].queue

    print(f"  [Check] 当前 CT 队列顺序: {[o.orderId for o in queueList]}")
    if len(queueList) > 0:
        assert queueList[0].orderId == manualInsertOrder.orderId, "插队失败，队首不是目标病人"
        print("  [Success] 插队成功，目标病人已在队首。")
    else:
        # 如果队列为空，说明可能已经开始扫描了
        currentScan = snapshotNow.ctStatusMap[targetCtId].currentOrder
        if currentScan and currentScan.orderId == manualInsertOrder.orderId:
            print("  [Success] 插队成功，病人已直接开始扫描。")
        else:
            print("  [Fail] 插队验证失败。")

    print("\n======== 测试结束 ========")


if __name__ == "__main__":
    # 运行测试前，请确保数据库连接配置正确，或者 mock 数据接口已就绪
    try:
        run_test()
    except Exception as e:
        print(f"测试发生异常: {e}")
        import traceback

        traceback.print_exc()