from abc import ABC, abstractmethod
from fastapi import APIRouter
from gateway.service.AbstractService import AbstractService


class AbstractController(ABC):
    def __init__(self, name: str, router: APIRouter):
        self.name: str = name
        self.router: APIRouter = router

    @abstractmethod
    def routerSetup(self):
        pass

