from typing import Optional, Literal
from pydantic import BaseModel, Field, conint,ConfigDict
from datetime import datetime

class VisitBase(BaseModel):
    patientId: int = Field(..., gt=0, description="患者ID，对应 patients.pid")
    doctorId: int = Field(..., gt=0, description="医生ID，对应 users.uid")

    visitTime: str = Field(
        ...,
        description="就诊时间，格式建议 YYYY-MM-DD HH:MM:SS"
    )
    isEmergency: int = Field(
        ...,
        ge=0,
        le=1,
        description="是否急诊：0=否，1=是"
    )
    symptoms: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="症状描述"
    )

    department: Optional[str] = Field(
        None,
        max_length=100,
        description="科室名称"
    )
    diagnosis: Optional[str] = Field(
        None,
        max_length=1000,
        description="诊断结果"
    )
    triageLevel: Optional[conint(ge=1, le=4)] = Field(
        None,
        description="分级（1-4 级，可按业务定义）"
    )
    status: Literal["ongoing", "finished", "canceled"] = Field(
        "ongoing",
        description="就诊状态"
    )
    createdTime: Optional[datetime] = Field(
        None,
        description="记录创建时间，通常由系统生成"
    )
    updatedTime: Optional[datetime] = Field(
        None,
        description="记录最后更新时间"
    )
    model_config = ConfigDict(
        from_attributes=True,
        str_min_length=1,  # 设置最小长度
        str_strip_whitespace=True  # 去除前后空白
    )


class VisitCreate(VisitBase):
    """
    创建就诊记录时使用：
    - 必须有 patientId, doctorId, visitTime, isEmergency, symptoms
    - status 有默认 'ongoing'
    - createdTime/updatedTime 一般由服务端忽略/覆盖
    """
    pass


class VisitUpdate(BaseModel):
    """
    更新就诊记录时使用：
    - visitId 必须
    - 其他字段全部可选，只更新传入的字段
    """
    visitId: int = Field(..., gt=0, description="就诊记录ID")

    patientId: Optional[int] = Field(None, gt=0)
    doctorId: Optional[int] = Field(None, gt=0)

    visitTime: Optional[str] = None
    isEmergency: Optional[int] = Field(None, ge=0, le=1)
    symptoms: Optional[str] = Field(None, min_length=1, max_length=1000)

    department: Optional[str] = Field(None, max_length=100)
    diagnosis: Optional[str] = Field(None, max_length=1000)
    triageLevel: Optional[conint(ge=1, le=4)] = None
    status: Optional[Literal["ongoing", "finished", "canceled"]] = None




class Visit(VisitBase):
    """
    查询/返回给前端时使用的完整实体
    """
    visitId: int = Field(..., gt=0, description="就诊记录ID")
