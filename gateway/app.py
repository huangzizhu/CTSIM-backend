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
from gateway.controller.LogController import LogController
from fastapi.middleware.cors import CORSMiddleware


class Application:

    def __init__(self):
        self.controllers: List[AbstractController] = []
        self.globalExceptionHandler = GlobalExceptionHandler()

    def _registerAllController(self):
        self.controllers.append(UserController())
        self.controllers.append(PatientController())
        self.controllers.append(VisitController())
        self.controllers.append(CTController())
        self.controllers.append(LogController())

    def createApp(self) -> FastAPI:
        self._registerAllController()
        app = FastAPI(
            debug=True,
            title="CT 管理系统后端",
            description="CT 管理系统后端",
            version="0.1.0",
            default_response_class=ResponseModel,
        )
        app.add_middleware(GlobalInterceptor)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        for controller in self.controllers:
            app.include_router(controller.router)

        self.globalExceptionHandler.registerAllHandler(app)
        return app


