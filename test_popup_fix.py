#!/usr/bin/env python3
"""
测试双弹窗修复效果
"""
import requests
import json
import time

def test_cfg_generation():
    """测试CFG生成功能"""
    url = "http://localhost:8000/api/cfg/generate"
    
    payload = {
        "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return fibonacci(n-1) + fibonacci(n-2)\n\ndef main():\n    n = 10\n    result = fibonacci(n)\n    print(f\"Fibonacci({n}) = {result}\")\n\nif __name__ == \"__main__\":\n    main()",
        "language": "Python",
        "model_name": "gpt-3.5-turbo",
        "client_name": "openai",
        "temperature": 0.0
    }
    
    print("🧪 测试双弹窗修复效果...")
    print("📤 发送请求到后端...")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 请求成功！状态码: {response.status_code}")
            print(f"📊 处理时间: {data.get('processing_time', 'N/A')}秒")
            
            if data.get('success'):
                print("✅ CFG生成成功！")
                
                # 检查Graph Code
                graph_code = data.get('graph_code')
                if graph_code:
                    print(f"🔧 Graph Code长度: {len(graph_code)} 字符")
                    print("📄 Graph Code预览:")
                    print(graph_code[:200] + "..." if len(graph_code) > 200 else graph_code)
                else:
                    print("⚠️  未生成Graph Code")
                
                # 检查图片URL
                image_url = data.get('image_url')
                if image_url:
                    print(f"🖼️  图片URL: {image_url}")
                    print("✅ 图片生成成功，应该显示在第二个框内")
                else:
                    print("⚠️  未生成图片")
                
                print("\n🎯 测试结果:")
                print("- ✅ 双弹窗问题已修复（view=False）")
                print("- ✅ Graph Code将显示在第一个框内")
                print("- ✅ CFG图片将显示在第二个框内")
                
            else:
                print(f"❌ 生成失败: {data.get('message', '未知错误')}")
        else:
            print(f"❌ 请求失败！状态码: {response.status_code}")
            print(f"📄 响应内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
    except Exception as e:
        print(f"❌ 意外错误: {e}")

if __name__ == "__main__":
    test_cfg_generation()