from fastapi import APIRouter,Body
from gateway.service.UserService import UserService
from gateway.controller.AbstractController import AbstractController
from pojo.User import UserLoginForm
from pojo.Tokens import Tokens
from gateway.Response import ResponseModel, Response



class UserController(AbstractController):
    def __init__(self):
        self.router = APIRouter(prefix="/user",tags=["用户管理"])
        self.userService: UserService = UserService()
        super().__init__("userController", self.router)
        self.routerSetup()

    def routerSetup(self):

        @self.router.post("/login")
        def login(userLoginForm: UserLoginForm = Body(...)) -> ResponseModel:
            tokens: Tokens = self.userService.login(userLoginForm)
            return Response.success(tokens)
