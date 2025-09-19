from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from api.routes import cfg_router, model_router
from core.config import settings

app = FastAPI(
    title="CFG Generation API",
    description="API for generating Control Flow Graphs from code",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册路由
app.include_router(cfg_router, prefix="/api/cfg", tags=["CFG Generation"])
app.include_router(model_router, prefix="/api/models", tags=["Model Management"])

@app.get("/")
async def root():
    return {"message": "CFG Generation API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )