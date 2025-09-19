#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_cfg_generation():
    """测试修复后的CFG生成功能"""
    
    # 测试代码
    test_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    num = 10
    if num < 0:
        print("请输入正数")
    else:
        for i in range(num):
            print(fibonacci(i))

if __name__ == "__main__":
    main()
'''
    
    # API请求数据
    request_data = {
        "code": test_code,
        "language": "Python",
        "model_name": "gpt-3.5-turbo",
        "client_name": "openai",
        "temperature": 0.0
    }
    
    print("=== 测试CFG生成API ===")
    print(f"测试代码长度: {len(test_code)} 字符")
    print(f"语言: {request_data['language']}")
    print(f"模型: {request_data['model_name']}")
    print()
    
    try:
        # 发送请求
        response = requests.post(
            "http://localhost:8000/api/cfg/generate",
            json=request_data,
            timeout=60
        )
        
        print(f"HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ CFG生成成功!")
            print(f"处理时间: {result.get('processing_time', 'N/A')} 秒")
            
            # 检查返回的数据结构
            if 'graph_data' in result:
                graph_data = result['graph_data']
                print(f"节点数量: {len(graph_data.get('nodes', []))}")
                print(f"边数量: {len(graph_data.get('edges', []))}")
                
                # 显示节点信息
                if graph_data.get('nodes'):
                    print("\n节点信息:")
                    for i, node in enumerate(graph_data['nodes'][:5]):  # 只显示前5个
                        print(f"  {i+1}. ID: {node.get('id')}, Label: {node.get('label')}")
                    if len(graph_data['nodes']) > 5:
                        print(f"  ... 还有 {len(graph_data['nodes']) - 5} 个节点")
                
                # 显示边信息
                if graph_data.get('edges'):
                    print("\n边信息:")
                    for i, edge in enumerate(graph_data['edges'][:5]):  # 只显示前5个
                        source = edge.get('source') or edge.get('from')
                        target = edge.get('target') or edge.get('to')
                        print(f"  {i+1}. {source} -> {target}")
                    if len(graph_data['edges']) > 5:
                        print(f"  ... 还有 {len(graph_data['edges']) - 5} 条边")
            
            # 检查是否生成了图片
            if 'image_url' in result:
                print(f"\n📷 图片URL: {result['image_url']}")
            
            # 检查是否有图形代码
            if 'graph_code' in result:
                graph_code = result['graph_code']
                print(f"\n📝 图形代码长度: {len(graph_code)} 字符")
                print("图形代码预览:")
                lines = graph_code.split('\n')
                for line in lines[:10]:  # 显示前10行
                    if line.strip():
                        print(f"  {line}")
                if len(lines) > 10:
                    print(f"  ... 还有 {len(lines) - 10} 行")
            
        else:
            print("❌ CFG生成失败!")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_cfg_generation()