
class TokenAuthException(Exception):
    def __init__(self, message="Token authentication failed"):
        self.message = message
        super().__init__(self.message)