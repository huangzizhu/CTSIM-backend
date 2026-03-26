from pydantic import BaseModel

class Tokens(BaseModel):
    accessToken: str
    refreshToken: str