
class TokenExpiryException(Exception):
    def __init__(self,message: str = "Refresh token has expired."):
        self.message = message
        super().__init__(self.message)
