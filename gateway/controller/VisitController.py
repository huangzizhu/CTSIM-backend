from fastapi import APIRouter,Body
from sqlalchemy.testing.warnings import setup_filters

from gateway.controller.AbstractController import AbstractController
from gateway.service.VisitService import VisitService
from pojo.Visit import VisitCreate,Visit,VisitUpdate
from gateway.Response import ResponseModel,Response
from typing import List


class VisitController(AbstractController):

    def __init__(self):
        self.router = APIRouter(prefix="/visit", tags=["就诊管理"])
        self.visitService = VisitService()
        super().__init__("visitController", self.router)
        self.routerSetup()

    def routerSetup(self):

        @self.router.post("")
        def addVisit(visit: VisitCreate = Body(...)) -> ResponseModel:
            self.visitService.addVisit(visit)
            return Response.success()

        # 根据pid查询所有就诊记录
        @self.router.get("/all/{pid}")
        def getAllVisitsByPid(pid: int) -> ResponseModel:
            visits: List[Visit]  = self.visitService.getAllVisitsByPid(pid)
            return Response.success(visits)

        # 根据pid查询最新就诊记录
        @self.router.get("/{pid}")
        def getVisitByPid(pid: int) -> ResponseModel:
            visit: Visit = self.visitService.getVisitByPid(pid)
            return Response.success(visit)

        @self.router.put("")
        def updateVisit(visit: VisitUpdate) -> ResponseModel:
            self.visitService.updateVisit(visit)
            return Response.success()

        @self.router.delete("/{visitId}")
        def deleteVisitByVisitId(visitId: int) -> ResponseModel:
            self.visitService.deleteVisitByVisitId(visitId)
            return Response.success()



