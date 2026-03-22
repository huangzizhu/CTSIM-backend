from functools import wraps
from typing import Dict, Type, Callable, Coroutine, Any
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from Exception.TokenAuthException import TokenAuthException
from Response import ResponseModel, Response


class GlobalExceptionHandler:
    def __init__(self):
        self.exceptionHandlerMap: Dict[Type[Exception], Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]] = {}


    def ExceptionHandler(self, exception: Type[Exception]):
        """
            自定义装饰器：标记函数为指定异常的处理器，并自动加入全局映射

            参数:
                exc_class: 要处理的异常类（如 TokenError、RequestValidationError）
        """

        def decorator(handler_func: Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]):
            # 保留原函数的元信息（如函数名、文档字符串）
            @wraps(handler_func)
            async def wrapper(request: Request, exc: Exception):
                # 执行原处理器函数逻辑
                return await handler_func(request, exc)

            self.exceptionHandlerMap[exception] = wrapper
            return wrapper
        return decorator

    def registerAllHandler(self,app: FastAPI):
        for exc_class, handler in self.exceptionHandlerMap.items():
            app.add_exception_handler(exc_class, handler)

    @ExceptionHandler(TokenAuthException)
    async def handleTokenAuthException(self, request: Request, exception: TokenAuthException) -> ResponseModel:
        return Response.error(msg=exception.message)