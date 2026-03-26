from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any, Union
from fastapi.encoders import jsonable_encoder


class ResponseModel(JSONResponse):
    def __init__(self, code: int, msg: str, data: Optional[Any] = None):
        content = {
            "code": code,
            "msg": msg,
            "data": data
        }
        super().__init__(content=jsonable_encoder(content))


class Response:

    @staticmethod
    def success(data: Optional[Any] = None, msg: str = "success") -> ResponseModel:
        """成功响应"""
        return ResponseModel(code=1, msg=msg, data=data)

    @staticmethod
    def error(data: Optional[Any] = None, msg: str = "error") -> ResponseModel:
        """失败响应"""
        return ResponseModel(code=0, msg=msg, data=data)