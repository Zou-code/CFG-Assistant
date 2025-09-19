from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # API配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CFG Generation API"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173"
    ]
    
    # 文件上传配置
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    STATIC_DIR: str = "static"
    
    # CFG生成配置
    SUPPORTED_LANGUAGES: List[str] = ["Python", "Java", "C"]
    DEFAULT_TEMPERATURE: float = 0.0
    
    # 模型配置
    SUPPORTED_MODELS: List[str] = [
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-3.5-turbo",
        "deepseek-chat"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局设置实例
settings = Settings()

# 确保必要的目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.STATIC_DIR, exist_ok=True)