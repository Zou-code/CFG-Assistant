#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_languages():
    try:
        response = requests.get(f"{BASE_URL}/api/cfg/languages")
        print(f"Languages: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Languages test failed: {e}")

def test_models():
    try:
        response = requests.get(f"{BASE_URL}/api/models/list")
        print(f"Models: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Models test failed: {e}")

def test_cfg_generation():
    try:
        data = {
            "code": "def hello():\n    print('Hello World')",
            "language": "Python"
        }
        response = requests.post(f"{BASE_URL}/api/cfg/generate", json=data)
        print(f"CFG Generation: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"CFG nodes: {len(result.get('nodes', []))}")
            print(f"CFG edges: {len(result.get('edges', []))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"CFG generation test failed: {e}")

if __name__ == "__main__":
    print("Testing CFG Assistant API...")
    test_health()
    test_languages()
    test_models()
    test_cfg_generation()
    print("Testing complete!")