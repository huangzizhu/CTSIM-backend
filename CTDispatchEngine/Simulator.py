from pojo.Patient import Patient as PatientData
from pojo.CT import CT as CTData
from simpy import Environment,PriorityStore,Interrupt
from CTDispatchEngine.RuleEngineContext import RuleEngineContext
class Patient:
    def __init__(self, patient: PatientData,context: RuleEngineContext):
        self.info: PatientData = patient
        self.priority: int = context.score

class CTMachine:
    def __init__(self, ct: CTData, env: Environment):
        self.ct: CTData = ct
        self.env: Environment = env
        self.queue: PriorityStore = PriorityStore(self.env)
        self.currentPatient: Patient | None = None
        self.counter: int = 0
        self.process = env.process(self.run())

    def addPatient(self, patient: Patient):
        self.counter += 1
        item = (patient.priority, self.counter, patient)
        return self.queue.put(item)
    def run(self):
        while True:
            # 取下一个病人
            priority: int
            seq: int
            patient: Patient
            priority, seq, patient = yield self.queue.get()
            self.currentPatient = patient
            start = self.env.now
            patient = patient.info.st or start

            print(f'[{self.env.now:.2f}] {self.name} 开始给 {patient.name} 扫描，剩余 {patient.remaining:.2f}')

            try:
                # 模拟扫描 patient.remaining 时间
                yield self.env.timeout(patient.remaining)
                # 没被打断，正常完成
                patient.finish_time = self.env.now
                print(f'[{self.env.now:.2f}] {self.name} 完成 {patient.name} 的扫描')
                self.currentPatient = None
            except Interrupt:
                # 被抢占
                used = self.env.now - start
                patient.remaining -= used
                print(
                    f'[{self.env.now:.2f}] {self.name} 扫描 {patient.name} 被打断，'
                    f'已用 {used:.2f}，剩余 {patient.remaining:.2f}'
                )
                self.currentPatient = None
                # 还没扫完的话，再次入队（保持原优先级）
                if patient.remaining > 0:
                    self.addPatient(patient)

