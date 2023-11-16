from typing import Annotated

from fastapi import Depends

from src.utils.service_manager import IServiceManager, ServiceManager

ServiceManagerDep = Annotated[IServiceManager, Depends(ServiceManager)]


class Paginator:
    def __init__(self, limit: int = 0, offset: int = 0):
        self.offset = offset
        self.limit = limit

