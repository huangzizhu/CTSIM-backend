from gateway.controller.AbstractController import AbstractController
from gateway.Response import ResponseModel
from fastapi import FastAPI,Depends
from typing import List
from gateway.GlobalInterceptor import GlobalInterceptor
from gateway.GlobalExceptionHandler import GlobalExceptionHandler
from gateway.controller.UserController import UserController
from gateway.controller.PatientController import PatientController
from gateway.controller.VisitController import VisitController
from gateway.controller.CTController import CTController


class Application:

    def __init__(self):
        self.controllers: List[AbstractController] = []
        self.globalExceptionHandler = GlobalExceptionHandler()

    def _registerAllController(self):
        self.controllers.append(UserController())
        self.controllers.append(PatientController())
        self.controllers.append(VisitController())
        self.controllers.append(CTController())

    def createApp(self) -> FastAPI:
        self._registerAllController()
        app = FastAPI(
            debug=True,
            title="CT 管理系统后端",
            description="CT 管理系统后端",
            version="0.1.0",
            default_response_class=ResponseModel,
            dependencies=[Depends(GlobalInterceptor)]
        )
        for controller in self.controllers:
            app.include_router(controller.router)

        self.globalExceptionHandler.registerAllHandler(app)
        return app


