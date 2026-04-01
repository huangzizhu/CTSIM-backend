from typing import Optional, Literal
from pydantic import BaseModel, Field, conint, ConfigDict
from datetime import datetime

class Log(BaseModel):
    logId: int = Field( gt=0, description="日志记录 ID")
    functionName: str = Field( description="被调用的函数名称")
    inputParams: Optional[dict] = Field(None, description="函数入参，以 JSON 格式存储")
    returnValue: Optional[dict] = Field(None, description="函数返回值，以 JSON 格式存储")
    userId: int = Field( gt=0, description="操作用户 ID")
    ipAddress: str = Field( description="请求来源的 IP 地址")
    source: str = Field( description="请求来源（如 WEB, API, APP 等）")
    operationTime: Optional[datetime] = Field(None, description="记录的操作时间")
    operationType: str = Field( description="操作类型（GET, POST, etc.）")
    executionTime: Optional[float] = Field(None, description="函数执行时长（单位：秒）")
    errorMessage: Optional[str] = Field(None, description="错误信息（如有）")
    requestPath: str = Field( description="请求的路径")
    httpMethod: str = Field( description="HTTP 方法（GET, POST, etc.）")
    model_config = ConfigDict(
        from_attributes=True,
        str_min_length=1,  # 设置最小长度
        str_strip_whitespace=True  # 去除前后空白
    )
