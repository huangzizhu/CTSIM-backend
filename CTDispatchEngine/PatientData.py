
from typing import List

from pojo.Patient import Patient
from pojo.Visit import Visit
from pojo.CT import CT
from pojo.CTOrder import CTOrder

class PatientData:
    def __init__(self, name: str, patient: Patient, visit: Visit):
        self.name: str = name
        self.patient: Patient = patient
        self.visit: Visit = visit


