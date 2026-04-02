from typing import Dict, Type, Callable, Coroutine, Any
from fastapi import Request, FastAPI
import inspect

from starlette.responses import JSONResponse

from Exception.PatientNotFoundException import PatientNotFoundException
from gateway.Response import ResponseModel, Response

from Exception.TokenAuthException import TokenAuthException
from Exception.TokenExpiredException import TokenExpiryException
from Exception.InvalidTokenError import InvalidTokenError
from Exception.UserNotFoundException import UserNotFoundException
from Exception.PasswordIncorrectException import PasswordIncorrectException
from Exception.DataBaseException import DataBaseException
from Exception.VisitNotFoundException import VisitNotFoundException
from Exception.CTOrderNotFoundException import CTOrderNotFoundException
from Exception.CTNotFoundException import CTNotFoundException


def ExceptionHandler(exception: Type[Exception]):
    def decorator(func):
        setattr(func, "_exception_class", exception)
        return func
    return decorator

class GlobalExceptionHandler:
    def __init__(self):
        self.exceptionHandlerMap: Dict[
            Type[Exception],
            Callable[[Request, Exception], Coroutine[Any, Any, ResponseModel]]
        ] = {}
        self._collectHandlers()

    #一个一个函数收集，装饰器标记异常类型，反射获取函数上的标记，构建异常类型到函数的映射
    def _collectHandlers(self):
        for _, method in inspect.getmembers(self, predicate=inspect.ismethod):
            exc_class = getattr(method, "_exception_class", None)
            if exc_class is not None:
                self.exceptionHandlerMap[exc_class] = method
    #注册所有处理器
    def registerAllHandler(self, app: FastAPI):
        for exc_class, handler in self.exceptionHandlerMap.items():
            app.add_exception_handler(exc_class, handler)

    @ExceptionHandler(TokenAuthException)
    async def handleTokenAuthException(self, request: Request, exception: TokenAuthException) -> JSONResponse:
        return JSONResponse(
            content={
                "code": 0,
                "msg": exception.message,
                "data": None}
             ,
            status_code=401
        )

    @ExceptionHandler(TokenExpiryException)
    async def handleTokenExpiryException(self, request: Request, exception: TokenExpiryException) -> JSONResponse:
        return JSONResponse(
            content={
                "code": 0,
                "msg": exception.message,
                "data": None}
             ,
            status_code=401
        )

    @ExceptionHandler(InvalidTokenError)
    async def handleInvalidTokenError(self, request: Request, exception: InvalidTokenError) -> ResponseModel:
        return Response.error(msg=exception.message)

    @ExceptionHandler(UserNotFoundException)
    async def handleUserNotFoundException(self, request: Request, exception: UserNotFoundException) -> ResponseModel:
        return Response.error(msg=exception.message)

    @ExceptionHandler(PasswordIncorrectException)
    async def handlePasswordIncorrectException(self, request: Request, exception: PasswordIncorrectException)-> ResponseModel:
        return Response.error(msg=exception.message)

    @ExceptionHandler(DataBaseException)
    async def handleDataBaseException(self, request: Request, exception: DataBaseException) -> ResponseModel:
        return Response.error(msg=exception.message)

    @ExceptionHandler(PatientNotFoundException)
    async def handlePatientNotFoundException(self, request: Request, exception: PatientNotFoundException) -> ResponseModel:
        return Response.error(msg=exception.message)

    @ExceptionHandler(VisitNotFoundException)
    async def handleVisitNotFoundException(self, request: Request, exception: VisitNotFoundException) -> ResponseModel:
        return Response.error(msg=exception.message)

    @ExceptionHandler(CTOrderNotFoundException)
    async def handleCTOrderNotFoundException(self, request: Request, exception: CTOrderNotFoundException) -> ResponseModel:
        return Response.error(msg=exception.message)

    @ExceptionHandler(CTNotFoundException)
    async def handleCTNotFoundException(self, request: Request, exception: CTNotFoundException) -> ResponseModel:
        return Response.error(msg=exception.message)
