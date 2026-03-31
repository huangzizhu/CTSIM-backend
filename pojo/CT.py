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
    model_config = ConfigDict(from_attributes=True)