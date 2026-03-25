from fastapi import APIRouter
from gateway.service.UserService import UserService
from AbstractController import AbstractController
from pojo.User import UserLoginForm
from pojo.Tokens import Tokens
from gateway.Response import ResponseModel, Response



class UserController(AbstractController):
    def __init__(self):
        router = APIRouter(prefix="/user",tags=["用户管理"])
        self.userService: UserService = UserService()
        super().__init__("userController", router)

    def routerSetup(self):

        @self.router.post("/login")
        def login(userLoginForm: UserLoginForm) -> ResponseModel:
            tokens: Tokens = self.userService.login(userLoginForm)
            return Response.success(tokens)
