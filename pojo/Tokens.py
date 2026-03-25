from pydantic import BaseModel
class Tokens(BaseModel):
    def __init__(self):
        self.accessToken: str
        self.refreshToken: str
        super().__init__()