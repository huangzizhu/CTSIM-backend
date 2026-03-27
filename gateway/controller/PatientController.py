
from fastapi import APIRouter,Body


from gateway.controller.AbstractController import AbstractController
from gateway.service.PatientService import PatientService
from pojo.User import UserLoginForm
from pojo.Tokens import Tokens
from pojo.Patient import CreatePatient,UpdatePatient
from gateway.Response import ResponseModel, Response

class PatientController(AbstractController):
    def __init__(self):
        self.router = APIRouter(prefix="/patient", tags=["患者管理"])
        self.patientService = PatientService()
        super().__init__("patientController", self.router)
        self.routerSetup()

    def routerSetup(self):

        @self.router.post("")
        def addPatient(patient: CreatePatient = Body(...)) -> ResponseModel:
            self.patientService.addPatient(patient)
            return Response.success()


        @self.router.put("")
        def updatePatient(patient: UpdatePatient = Body(...)) -> ResponseModel:
            self.patientService.updatePatient(patient)
            return Response.success()