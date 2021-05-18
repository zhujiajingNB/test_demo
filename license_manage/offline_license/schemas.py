from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CreateOfflineLicense(BaseModel):
    offline_version: str
    path: str
    create_time: datetime
    comment: str = None

    class Config:
        orm_mode = True

class ReadOfflineLicense(CreateOfflineLicense):
    id: int


class ReadOfflineLicenses(BaseModel):
    data: List[ReadOfflineLicense]

class ReadOfflineLicensePage(BaseModel):
    data: List[ReadOfflineLicense]
    total_page: Optional[int] = None


class PageInfo(BaseModel):
    page: int = Field(default=1, description="当前页")
    page_num: int = Field(default=10, description="每页大小")


