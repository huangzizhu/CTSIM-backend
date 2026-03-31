from typing import List
from fastapi import APIRouter

from gateway.Response import Response,ResponseModel
from gateway.controller.AbstractController import AbstractController
from gateway.service.CTService import CTService
from pojo.CT import CT
from pojo.CTOrder import CTOrderCreate,CTOrderUpdate,CTOrder


class CTController(AbstractController):
    def __init__(self):
        self.router = APIRouter(prefix="/ct",tags=["CT管理"])
        self.CTService: CTService = CTService()
        super().__init__("CTController", self.router)
        self.routerSetup()

    def routerSetup(self):

        @self.router.get("")
        def getAllCT() -> ResponseModel:
            cts: List[CT] = self.CTService.getAllCT()
            return Response.success(cts)

        @self.router.post("/order")
        def addCTOrder(order: CTOrderCreate) -> ResponseModel:
            ctOrder: CTOrder = self.CTService.addCTOrder(order)
            return Response.success(ctOrder)

        @self.router.get("/order/p/all/{pid}")
        def getAllCTOrdersByPID(pid: int) -> ResponseModel:
            ctOrders: List[CTOrder] = self.CTService.getAllCTOrdersByPID(pid)
            return Response.success(ctOrders)

        # 获取最新的Order
        @self.router.get("/order/p/{pid}")
        def getNewestCTOrderByPID(pid: int) -> ResponseModel:
            ctOrder: CTOrder | None = self.CTService.getNewestCTOrderByPID(pid)
            return Response.success(ctOrder)

        @self.router.get("/order/c/{CTOrderId}")
        def getCTOrderByID(CtorId: int) -> ResponseModel:
            ctOrder: CTOrder = self.CTService.getCTOrderByID(CtorId)
            return Response.success(ctOrder)







