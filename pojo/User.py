from pydantic import BaseModel,Field
class UserLoginForm(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="不能为空，最短3字符，最长20字符"
    )
    hashedPassword: str = Field(
        ...,
        description="不能为空"
    )

class User(BaseModel):
    username: str
    hashedPassword: str
    userId: int
    level: int
