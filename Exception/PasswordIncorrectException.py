class PasswordIncorrectException(Exception):
    def __init__(self, message="Password is incorrect."):
        self.message = message
        super().__init__(self.message)