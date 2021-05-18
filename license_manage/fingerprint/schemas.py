from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CreateFingerPrint(BaseModel):
    customer_name: str = None
    path: str
    create_time: datetime
    comment: str = None
    class Config:
        orm_mode = True

class ReadFingerPrint(CreateFingerPrint):
    id: int


class ReadFingerPrints(BaseModel):
    data: List[ReadFingerPrint]

class ReadFingerPrintPage(BaseModel):
    data: List[ReadFingerPrint]
    total_page: Optional[int] = None


class PageInfo(BaseModel):
    page: int = Field(default=1, description="当前页")
    page_num: int = Field(default=10, description="每页大小")


