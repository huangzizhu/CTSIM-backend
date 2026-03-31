from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# 状态常量
class StatusEnum:
    PENDING = 0     # 待排队
    QUEUING = 1     # 排队中
    SCANNING = 2    # 扫描中
    COMPLETED = 3   # 已完成
    CANCELED = 4    # 已取消
    EXPIRED = 5     # 过期

# 优先级常量
class PriorityEnum:
    NORMAL = 0      # 普通
    EMERGENCY = 1   # 急诊
    VIP = 2         # VIP

# CTOrder 基础类
class CTOrderBase(BaseModel):
    patientId: int = Field(..., description="患者 ID", ge=1)  # 这里加了最小值验证
    visitId: int = Field(..., description="就诊 ID", ge=1)
    ctId: int = Field(..., description="CT 设备 ID", ge=1)
    status: int = Field(..., description="状态，对应 StatusEnum", ge=0, le=5)  # 限制状态值范围 0 到 5
    scheduledTime: datetime = Field(..., description="排队时间")
    queueEnterTime: Optional[datetime] = Field(None, description="进入队列时间")
    startTime: Optional[datetime] = Field(None, description="扫描开始时间")
    endTime: Optional[datetime] = Field(None, description="扫描结束时间")
    expectedDuration: Optional[int] = Field(None, description="预计扫描时长（分钟）", ge=0)  # 预计时长不能小于0
    actualDuration: Optional[int] = Field(None, description="实际扫描时长（分钟）", ge=0)    # 实际时长不能小于0
    priority: Optional[int] = Field(PriorityEnum.NORMAL, description="优先级 0-2 对应 PriorityEnum", ge=0, le=2)
    isEmergency: Optional[bool] = Field(False, description="是否紧急")
    notes: Optional[str] = Field(None, description="备注信息")
    model_config = ConfigDict(
        from_attributes=True,
        str_min_length=1,  # 设置最小长度
        str_strip_whitespace=True  # 去除前后空白
    )

# CTOrder 创建类
class CTOrderCreate(CTOrderBase):
    pass

# CTOrder 更新类
class CTOrderUpdate(CTOrderBase):
    pass

# CTOrder 数据库存储类
class CTOrderInDB(CTOrderBase):
    orderId: int = Field(..., description="订单 ID", ge=1)
    createdAt: datetime = Field(..., description="创建时间")
    updatedAt: datetime = Field(..., description="更新时间")
    canceledAt: Optional[datetime] = Field(None, description="取消时间")

# CTOrder 实体类
class CTOrder(CTOrderBase):
    orderId: int = Field(..., description="订单 ID", ge=1)
    createdAt: datetime = Field(..., description="创建时间")
    updatedAt: datetime = Field(..., description="更新时间")
    canceledAt: Optional[datetime] = Field(None, description="取消时间")
    status: int = Field(..., description="状态", ge=0, le=5)  # 使用状态常量的范围验证
    priority: Optional[int] = Field(PriorityEnum.NORMAL, description="优先级", ge=0, le=2)