#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_cfg_generation_detailed():
    """详细测试CFG生成功能"""
    
    # 简单的测试代码
    test_code = '''
def simple_function():
    x = 1
    if x > 0:
        print("positive")
    else:
        print("negative")
    return x
'''
    
    # API请求数据
    request_data = {
        "code": test_code,
        "language": "Python",
        "model_name": "gpt-3.5-turbo",
        "client_name": "openai",
        "temperature": 0.0
    }
    
    print("=== 详细测试CFG生成API ===")
    print(f"测试代码:\n{test_code}")
    print(f"语言: {request_data['language']}")
    print(f"模型: {request_data['model_name']}")
    print(f"客户端: {request_data['client_name']}")
    print()
    
    try:
        # 发送请求
        print("🚀 发送API请求...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8000/api/cfg/generate",
            json=request_data,
            timeout=120  # 增加超时时间
        )
        
        end_time = time.time()
        print(f"⏱️ 请求耗时: {end_time - start_time:.2f} 秒")
        print(f"📊 HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功!")
            
            # 详细分析返回结果
            print(f"🔍 返回结果分析:")
            print(f"  - success: {result.get('success')}")
            print(f"  - message: {result.get('message')}")
            print(f"  - processing_time: {result.get('processing_time')} 秒")
            
            # 检查图形代码
            if 'graph_code' in result:
                graph_code = result['graph_code']
                print(f"  - graph_code 长度: {len(graph_code)} 字符")
                print(f"  - graph_code 预览:")
                lines = graph_code.split('\n')
                for i, line in enumerate(lines[:15]):  # 显示前15行
                    print(f"    {i+1:2d}: {line}")
                if len(lines) > 15:
                    print(f"    ... 还有 {len(lines) - 15} 行")
                
                # 检查是否包含真实的CFG内容
                if "dot.node(" in graph_code and "dot.edge(" in graph_code:
                    print("  ✅ 包含真实的CFG节点和边定义")
                else:
                    print("  ⚠️ 可能是模拟数据，缺少真实的CFG内容")
            else:
                print("  ❌ 没有返回graph_code")
            
            # 检查图形数据
            if 'graph_data' in result:
                graph_data = result['graph_data']
                print(f"  - 节点数量: {len(graph_data.get('nodes', []))}")
                print(f"  - 边数量: {len(graph_data.get('edges', []))}")
                
                # 显示具体的节点和边
                nodes = graph_data.get('nodes', [])
                edges = graph_data.get('edges', [])
                
                if nodes:
                    print("  - 节点详情:")
                    for node in nodes[:5]:
                        print(f"    * {node}")
                
                if edges:
                    print("  - 边详情:")
                    for edge in edges[:5]:
                        print(f"    * {edge}")
            else:
                print("  ❌ 没有返回graph_data")
            
            # 检查图片URL
            if 'image_url' in result:
                print(f"  - 图片URL: {result['image_url']}")
            else:
                print("  ❌ 没有生成图片")
            
            # 检查警告信息
            if 'warning' in result:
                print(f"  ⚠️ 警告: {result['warning']}")
            
        else:
            print("❌ API调用失败!")
            print(f"错误响应: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时!")
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_cfg_generation_detailed()