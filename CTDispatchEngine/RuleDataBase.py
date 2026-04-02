from abc import ABC, abstractmethod
from pojo.Patient import Patient
from pojo.Visit import Visit
from pojo.CT import CT
from pojo.CTOrder import CTOrder

class RuleDataBase(ABC):
    def __init__(self, name: str, patient: Patient, visit: Visit, ct: CT, ctOrder: CTOrder):
        self.name: str = name
        self.patient: Patient = patient
        self.visit: Visit = visit
        self.ct: CT = ct
        self.ctOder: CTOrder = ctOrder


