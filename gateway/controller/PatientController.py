
from fastapi import APIRouter,Body


from gateway.controller.AbstractController import AbstractController
from gateway.service.PatientService import PatientService
from pojo.Patient import CreatePatient,UpdatePatient,Patient
from gateway.Response import ResponseModel, Response
from typing import List

class PatientController(AbstractController):
    def __init__(self):
        self.router = APIRouter(prefix="/patient", tags=["患者管理"])
        self.patientService = PatientService()
        super().__init__("patientController", self.router)
        self.routerSetup()

    def routerSetup(self):

        @self.router.post("")
        def addPatient(patient: CreatePatient = Body(...)) -> ResponseModel:
            patient: Patient = self.patientService.addPatient(patient)
            return Response.success(patient)


        @self.router.put("")
        def updatePatient(patient: UpdatePatient = Body(...)) -> ResponseModel:
            newPatient: Patient = self.patientService.updatePatient(patient)
            return Response.success(patient)

        @self.router.get("")
        def getAllPatients() -> ResponseModel:
            patients:List[Patient] = self.patientService.getAllPatients()
            return Response.success(patients)

        @self.router.delete("/{pid}")
        def deletePatient(pid: int) -> ResponseModel:
            self.patientService.deletePatient(pid)
            return Response.success()