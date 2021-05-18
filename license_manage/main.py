# -*- coding: utf-8 -*-
#
# FastAPI入口
# Author: 朱家井
# Created Time: 2021年05月17日 星期一

from fastapi import FastAPI
import uvicorn
from main_settings import APP_SETTINGS
from fingerprint import app_fin
from offline_license import app_off
from app_sdk import app_sd

app = FastAPI(**APP_SETTINGS)

# 路由配置
app.include_router(app_fin, prefix='/fingerprint', tags=["指纹管理接口"])
app.include_router(app_off, prefix='/offline_license', tags=['离线授权管理接口'])
app.include_router(app_sd, prefix='/app_sdk', tags=['app_sdk管理接口'])

# 测试
@app.get('/test')
async def get_test():
    import sys
    s = sys.path
    print(s)
    print(__file__)
    return None

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)