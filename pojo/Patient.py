from pydantic import BaseModel, Field, constr, condecimal
from typing import Optional


class Patient(BaseModel):
    pid: Optional[int] = None
    cardNo: str
    name: str
    gender: str
    birthDate: str
    phone: str = Field(..., min_length=11, max_length=11, description="手机号码")
    idNumber: str = Field(..., min_length=18, max_length=18, description="身份证号")
    address: Optional[str] = None
    emergencyContactName: Optional[str] = None
    emergencyContactPhone: Optional[str] = None
    createdTime: Optional[str] = None
    updatedTime: Optional[str] = None

    class Config:
        str_min_length = 1
        str_strip_whitespace = True

# 创建病人请求模型
class CreatePatient(Patient):
    cardNo: str = Field(..., max_length=20, description="就诊卡号")
    name: str = Field(..., max_length=50, description="患者姓名")
    gender: str = Field(..., max_length=1, description="性别")
    birthDate: str = Field(..., description="出生日期")
    phone: str = Field(..., description="手机号",min_length=11, max_length=11)
    idNumber: str = Field(..., description="身份证号", min_length=18, max_length=18)
    address: Optional[str] = None
    emergencyContactName: Optional[str] = None
    emergencyContactPhone: Optional[str] = None

# 修改病人请求模型
class UpdatePatient(Patient):
    pid: int = Field(..., description="患者ID")
    cardNo: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=50)
    gender: Optional[str] = Field(None, max_length=1)
    birthDate: Optional[str] = None
    phone: Optional[str] = Field(None,description="手机号",min_length=11, max_length=11)
    idNumber: Optional[str] = Field(None,description="身份证号", min_length=18, max_length=18)
    address: Optional[str] = None
    emergencyContactName: Optional[str] = None
    emergencyContactPhone: Optional[str] = None
    createdTime: Optional[str] = None  # 不修改
    updatedTime: Optional[str] = None

    class Config:
        str_min_length = 1
        str_strip_whitespace = True