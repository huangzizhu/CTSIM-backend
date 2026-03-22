from fastapi import Request


class GlobalInterceptor:
    def __init__(self, anonymous: bool):
        self.anonymous = anonymous

    def __call__(self, request: Request):
        if self.anonymous:
            return None
