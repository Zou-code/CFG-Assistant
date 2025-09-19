import requests
import json

# 测试API端点
API_BASE = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print("✅ 健康检查通过\n")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}\n")

def test_languages():
    """测试获取支持的语言"""
    print("🔍 测试获取支持的语言...")
    try:
        response = requests.get(f"{API_BASE}/api/cfg/languages")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print("✅ 语言列表获取成功\n")
    except Exception as e:
        print(f"❌ 语言列表获取失败: {e}\n")

def test_models():
    """测试获取支持的模型"""
    print("🔍 测试获取支持的模型...")
    try:
        response = requests.get(f"{API_BASE}/api/models/list")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print("✅ 模型列表获取成功\n")
    except Exception as e:
        print(f"❌ 模型列表获取失败: {e}\n")

def test_cfg_generation():
    """测试CFG生成"""
    print("🔍 测试CFG生成...")
    try:
        data = {
            "code": """def hello():
    print('Hello World')

def main():
    hello()
    
if __name__ == "__main__":
    main()""",
            "language": "Python"
        }
        
        response = requests.post(
            f"{API_BASE}/api/cfg/generate",
            headers={"Content-Type": "application/json"},
            json=data
        )
        
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200 and result.get('success'):
            print("✅ CFG生成成功\n")
        else:
            print("⚠️ CFG生成返回了响应，但可能有问题\n")
            
    except Exception as e:
        print(f"❌ CFG生成失败: {e}\n")

if __name__ == "__main__":
    print("🚀 开始API测试...\n")
    
    test_health()
    test_languages()
    test_models()
    test_cfg_generation()
    
    print("🎉 API测试完成！")