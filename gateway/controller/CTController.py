from typing import List
from fastapi import APIRouter,Path
from utils.Log import Log
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

        @Log
        @self.router.post("/order")
        def addCTOrder(order: CTOrderCreate) -> ResponseModel:
            ctOrder: CTOrder = self.CTService.addCTOrder(order)
            return Response.success(ctOrder)

        @self.router.get("/order/p/all/{pid}")
        def getAllCTOrdersByPID(pid: int = Path(..., ge=1)) -> ResponseModel:
            ctOrders: List[CTOrder] = self.CTService.getAllCTOrdersByPID(pid)
            return Response.success(ctOrders)

        # 获取最新的Order
        @self.router.get("/order/p/{pid}")
        def getNewestCTOrderByPID(pid: int = Path(..., ge=1)) -> ResponseModel:
            ctOrder: CTOrder | None = self.CTService.getNewestCTOrderByPID(pid)
            return Response.success(ctOrder)

        @self.router.get("/order/c/{CTOrderId}")
        def getCTOrderByID(CTOrderId: int = Path(..., ge=1)) -> ResponseModel:
            ctOrder: CTOrder = self.CTService.getCTOrderByID(CTOrderId)
            return Response.success(ctOrder)

        @Log
        @self.router.put("/order")
        def updateOrder(order: CTOrderUpdate) -> ResponseModel:
            ctOrder: CTOrder | None = self.CTService.updateOrder(order)
            return Response.success(ctOrder)


        @Log
        @self.router.delete("/order/c/{CTOrderId}")
        def cancelOrder(CTOrderId: int) -> ResponseModel:
            self.CTService.cancelOrder(CTOrderId)
            return Response.success()







