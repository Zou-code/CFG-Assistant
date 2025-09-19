from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="CFG Generation API",
    description="API for generating Control Flow Graphs from code",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CFG Generation API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/cfg/languages")
async def get_supported_languages():
    return {"languages": ["Python", "Java", "C"]}

@app.get("/api/models/list")
async def get_supported_models():
    return {
        "models": [
            {"name": "gpt-4", "client": "openai"},
            {"name": "gpt-4-turbo", "client": "openai"},
            {"name": "gpt-3.5-turbo", "client": "openai"},
            {"name": "deepseek-chat", "client": "deepseek"}
        ]
    }

@app.post("/api/cfg/generate")
async def generate_cfg(request: dict):
    # 简单的模拟响应
    return {
        "success": True,
        "message": "CFG生成成功",
        "graph_data": {
            "nodes": [
                {"id": "start", "label": "开始", "type": "start"},
                {"id": "process1", "label": "处理1", "type": "process"},
                {"id": "end", "label": "结束", "type": "end"}
            ],
            "edges": [
                {"from": "start", "to": "process1"},
                {"from": "process1", "to": "end"}
            ]
        },
        "processing_time": 1.5
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )