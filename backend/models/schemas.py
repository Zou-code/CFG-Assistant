from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum

class LanguageEnum(str, Enum):
    PYTHON = "Python"
    JAVA = "Java"
    C = "C"

class ModelEnum(str, Enum):
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4O = "gpt-4o"
    GPT_35_TURBO = "gpt-3.5-turbo"
    DEEPSEEK_CHAT = "deepseek-chat"

class ClientEnum(str, Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"

class CFGGenerationRequest(BaseModel):
    code: str = Field(..., description="源代码内容")
    language: LanguageEnum = Field(..., description="编程语言")
    model_name: ModelEnum = Field(default=ModelEnum.GPT_4, description="使用的模型")
    client_name: ClientEnum = Field(default=ClientEnum.OPENAI, description="客户端类型")
    temperature: float = Field(default=0.0, ge=0.0, le=2.0, description="模型温度参数")
    api_key: Optional[str] = Field(None, description="API密钥（可选，覆盖默认配置）")

class CFGGenerationResponse(BaseModel):
    success: bool = Field(..., description="生成是否成功")
    message: str = Field(..., description="响应消息")
    graph_data: Optional[Dict[str, Any]] = Field(None, description="图形数据")
    graph_code: Optional[str] = Field(None, description="生成的Graphviz代码")
    image_url: Optional[str] = Field(None, description="生成的图片URL")
    processing_time: Optional[float] = Field(None, description="处理时间（秒）")

class ModelConfigRequest(BaseModel):
    model_name: ModelEnum = Field(..., description="模型名称")
    client_name: ClientEnum = Field(..., description="客户端类型")
    api_key: str = Field(..., description="API密钥")
    temperature: float = Field(default=0.0, ge=0.0, le=2.0, description="温度参数")
    max_tokens: Optional[int] = Field(None, ge=1, le=4096, description="最大token数")

class ModelConfigResponse(BaseModel):
    success: bool = Field(..., description="配置是否成功")
    message: str = Field(..., description="响应消息")
    model_info: Optional[Dict[str, Any]] = Field(None, description="模型信息")

class ErrorResponse(BaseModel):
    success: bool = Field(default=False, description="操作是否成功")
    error: str = Field(..., description="错误信息")
    error_code: Optional[str] = Field(None, description="错误代码")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详情")

class HealthResponse(BaseModel):
    status: str = Field(..., description="服务状态")
    timestamp: str = Field(..., description="检查时间")
    version: str = Field(..., description="API版本")

class SupportedLanguagesResponse(BaseModel):
    languages: List[str] = Field(..., description="支持的编程语言列表")

class SupportedModelsResponse(BaseModel):
    models: List[Dict[str, str]] = Field(..., description="支持的模型列表")