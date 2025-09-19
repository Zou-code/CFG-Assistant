import time
from openai import OpenAI
import yaml
import os

class LLM_util:
    def __init__(self, model_name, client_name='openai', api_key=None):
        # 获取当前文件的绝对路径，再拼接config.yaml的路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "../config.yaml")
        # 规范化路径（处理..等相对路径符号）
        config_path = os.path.normpath(config_path)

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 如果提供了api_key，使用提供的，否则从配置文件读取
        openai_api_key = api_key if api_key and client_name == 'openai' else config["API Key"]["openai"]
        deepseek_api_key = api_key if api_key and client_name == 'deepseek' else config["API Key"]["deepseek"]

        self.model_name = model_name
        # 默认使用openai的模型
        self.client = OpenAI(api_key=openai_api_key)

        if client_name == "openai":
            self.client = OpenAI(api_key=openai_api_key)
        elif client_name == "deepseek":
            self.client_deepseek = OpenAI(api_key=deepseek_api_key)

    def call_LLM(self, prompt):
        message = [
            {"role": "user", "content": prompt}
        ]
        while True:
            try:
                # 根据模型名称选择合适的客户端
                if hasattr(self, 'client_deepseek') and self.model_name == "deepseek-chat":
                    client = self.client_deepseek
                else:
                    client = self.client
                
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=message,
                    temperature=0
                )
                return response.choices[0].message.content
            except Exception as e:
                print(e)
                time.sleep(1)

if __name__ == '__main__':
    # llm = LLM_util("deepseek-chat", "deepseek")
    llm = LLM_util("gpt-3.5-turbo")
    response = llm.call_LLM("hello, who are you?")
    print(response)



