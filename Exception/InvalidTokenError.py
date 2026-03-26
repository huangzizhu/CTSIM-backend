class InvalidTokenError(Exception):
    def __init__(self, message="Invalid refresh token."):
        self.message = message