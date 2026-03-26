
from fastapi import APIRouter,Body
from gateway.service.UserService import UserService
from gateway.controller.AbstractController import AbstractController
from pojo.User import UserLoginForm
from pojo.Tokens import Tokens
from gateway.Response import ResponseModel, Response

class PatientController(AbstractController):
    def __init__(self):
        self.router = APIRouter(prefix="/patient", tags=["患者管理"])
        self.userService: UserService = UserService()
        super().__init__("patientController", self.router)
        self.routerSetup()

    def routerSetup(self):
        pass