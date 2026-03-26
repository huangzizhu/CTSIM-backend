from fastapi import Request


class GlobalInterceptor:
    def __init__(self):
        self.anonymous = False

    def __call__(self, request: Request):
        if self.anonymous:
            return None
