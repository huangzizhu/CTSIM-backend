from fastapi import APIRouter,Body
from gateway.controller.AbstractController import AbstractController
from gateway.service.ConsultationService import ConsultationService
from typing import List


class ConsultationController(AbstractController):

    def __init__(self):
        self.router = APIRouter(prefix="/visit", tags=["就诊管理"])
        self.consultationService = ConsultationService()
        super().__init__("patientController", self.router)
        self.routerSetup()

    def routerSetup(self):
        pass