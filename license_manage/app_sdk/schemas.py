from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CreateAppSdk(BaseModel):
    sdk_name: str = None
    path: str
    comment: str = None
    sdk_version: str
    class Config:
        orm_mode = True

class ReadAppSdk(CreateAppSdk):
    id: int
    create_time: datetime

class ReadAppSdks(BaseModel):
    data: List[ReadAppSdk]

class ReadAppSdkPage(BaseModel):
    data: List[ReadAppSdk]
    total_page: Optional[int] = None


class PageInfo(BaseModel):
    page: int = Field(default=1, description="当前页")
    page_num: int = Field(default=10, description="每页大小")


