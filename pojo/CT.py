from datetime import datetime
from typing import Optional

from pydantic import BaseModel,ConfigDict


class CT(BaseModel):
    ctId: int
    deviceCode: str
    deviceName: str
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    category: Optional[str] = None
    status: str
    location: str
    notes: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    model_config = ConfigDict(
        from_attributes=True,
        str_min_length=1,  # 设置最小长度
        str_strip_whitespace=True  # 去除前后空白
    )