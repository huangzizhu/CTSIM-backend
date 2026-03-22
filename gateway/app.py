from AbstractController import AbstractController
from Response import ResponseModel
from fastapi import FastAPI,Depends
from typing import List
from GlobalInterceptor import GlobalInterceptor
from GlobalExceptionHandler import GlobalExceptionHandler


class Application:

    def __init__(self):
        self.controllers: List[AbstractController] = []
        self.globalExceptionHandler = GlobalExceptionHandler()


    def createApp(self) -> FastAPI:
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


