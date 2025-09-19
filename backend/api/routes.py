from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
import asyncio
from typing import Dict, Any

from models.schemas import (
    CFGGenerationRequest, CFGGenerationResponse, ErrorResponse,
    ModelConfigRequest, ModelConfigResponse, HealthResponse,
    SupportedLanguagesResponse, SupportedModelsResponse,
    LanguageEnum, ModelEnum, ClientEnum
)
from services.cfg_service import cfg_service
from core.config import settings

# CFG生成相关路由
cfg_router = APIRouter()

@cfg_router.post("/generate", response_model=CFGGenerationResponse)
async def generate_cfg(request: CFGGenerationRequest):
    """
    生成控制流图
    """
    try:
        # 验证输入
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="代码内容不能为空")
        
        if request.language not in [lang.value for lang in LanguageEnum]:
            raise HTTPException(status_code=400, detail=f"不支持的编程语言: {request.language}")
        
        if request.model_name not in [model.value for model in ModelEnum]:
            raise HTTPException(status_code=400, detail=f"不支持的模型: {request.model_name}")
        
        # 调用CFG生成服务
        result = await cfg_service.generate_cfg(request)
        
        if result["success"]:
            return CFGGenerationResponse(**result)
        else:
            raise HTTPException(status_code=500, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@cfg_router.get("/languages", response_model=SupportedLanguagesResponse)
async def get_supported_languages():
    """
    获取支持的编程语言列表
    """
    return SupportedLanguagesResponse(
        languages=[lang.value for lang in LanguageEnum]
    )

@cfg_router.get("/status")
async def get_cfg_status():
    """
    获取CFG服务状态
    """
    return {
        "service": "CFG Generation",
        "status": "running",
        "supported_languages": [lang.value for lang in LanguageEnum],
        "timestamp": datetime.now().isoformat()
    }

# 模型管理相关路由
model_router = APIRouter()

@model_router.get("/list", response_model=SupportedModelsResponse)
async def get_supported_models():
    """
    获取支持的模型列表
    """
    models = []
    for model in ModelEnum:
        client = "openai" if model.value.startswith("gpt") else "deepseek"
        models.append({
            "name": model.value,
            "display_name": model.value.upper().replace("-", " "),
            "client": client,
            "description": f"{model.value} model"
        })
    
    return SupportedModelsResponse(models=models)

@model_router.post("/config", response_model=ModelConfigResponse)
async def configure_model(request: ModelConfigRequest):
    """
    配置模型参数
    """
    try:
        # 验证模型和客户端组合
        if request.client_name == ClientEnum.OPENAI and not request.model_name.value.startswith("gpt"):
            raise HTTPException(status_code=400, detail="OpenAI客户端只支持GPT模型")
        
        if request.client_name == ClientEnum.DEEPSEEK and request.model_name != ModelEnum.DEEPSEEK_CHAT:
            raise HTTPException(status_code=400, detail="DeepSeek客户端只支持deepseek-chat模型")
        
        # 这里可以添加模型配置验证逻辑
        # 例如测试API密钥是否有效
        
        model_info = {
            "model_name": request.model_name.value,
            "client_name": request.client_name.value,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "configured_at": datetime.now().isoformat()
        }
        
        return ModelConfigResponse(
            success=True,
            message="模型配置成功",
            model_info=model_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"配置模型失败: {str(e)}")

@model_router.get("/test/{model_name}")
async def test_model(model_name: str, client_name: str = "openai", api_key: str = None):
    """
    测试模型连接
    """
    try:
        # 验证模型名称
        if model_name not in [model.value for model in ModelEnum]:
            raise HTTPException(status_code=400, detail=f"不支持的模型: {model_name}")
        
        # 实际测试模型连接
        from util.LLM_util import LLM_util
        
        # 创建临时的LLM客户端进行测试
        llm_client = LLM_util(
            model_name=model_name,
            client_name=client_name,
            api_key=api_key  # 使用传入的API密钥
        )
        
        # 发送一个简单的测试请求
        test_prompt = "Hello, this is a test message. Please respond with 'OK'."
        response = llm_client.call_LLM(test_prompt)
        
        if response and "OK" in response:
            return {
                "model_name": model_name,
                "client_name": client_name,
                "status": "available",
                "test_time": datetime.now().isoformat(),
                "message": "模型连接正常"
            }
        else:
            raise HTTPException(status_code=401, detail="API密钥无效或模型无法访问")
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid" in error_msg.lower():
            raise HTTPException(status_code=401, detail="API密钥无效或权限不足")
        elif "timeout" in error_msg.lower():
            raise HTTPException(status_code=408, detail="连接超时，请检查网络连接")
        else:
            raise HTTPException(status_code=500, detail=f"测试模型失败: {error_msg}")

# 通用错误处理 - 这应该在主应用程序中设置，不是在路由器中
# @cfg_router.exception_handler(Exception)
# @model_router.exception_handler(Exception)
# async def general_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=500,
#         content=ErrorResponse(
#             error=str(exc),
#             error_code="INTERNAL_ERROR"
#         ).dict()
#     )