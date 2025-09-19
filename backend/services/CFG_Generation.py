import subprocess
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

from util.LLM_util import LLM_util
# from soupsieve.util import lower    #将字符串变为小写 - 注释掉未使用的导入

class CFG:
    def __init__(self, language, client_name, model_name):
        self.language = language
        self.llm = LLM_util(model_name, client_name)
        pass

    # 读文件
    def read_file(self,path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    # 写文件
    def write_file(self, path, content):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    # 解套 目前只针对Python代码执行这一步骤
    def unwrap_code(self,code):
        """
        :param code_path: 代码文件地址
        :param language:代码语言
        :return: -
        """
        prompt = self.read_file('prompt/'+'Python/unwrap_prompt.txt')    #提示词
        prompt = prompt.replace('{input_code}', code)
        # message = [{"role": "user", "content": prompt.replace('{input_code}', code)}]    #消息内容  将提示词中的占位符换成代码
        unwrap_python_code = self.llm.call_LLM(prompt).strip('\n')
        return unwrap_python_code

    # 获得代码结构并写入文件
    def get_structure(self, code):
        """
        :param code_path: 代码文件地址
        :param language:代码语言
        :return: -
        """
        prompt = self.read_file('./prompt/' + self.language + '/structure_prompt.txt')  # 提示词
        prompt = prompt.replace('{input_code}', code)
        # message = [{"role": "user", "content": prompt.replace('{input_code}', code)}]  # 消息内容  将提示词中的占位符换成代码
        structure_content = self.llm.call_LLM(prompt).strip('@Output{').strip('}').strip('\n').strip('[').strip(']').strip(
            '\n')  # 调用大模型 去除返回内容的包裹符号和头尾的空行
        return structure_content

    def get_nested(self,code, code_structure):
        """
        :param code_path: 代码文件地址
        :param structure_path: 代码结构文件地址
        :param language:代码语言
        :return:
        """
        prompt = self.read_file('./prompt/' + self.language + '/nested_prompt.txt')  # 提示词
        # message = [{"role": "user", "content": prompt.replace('{input_code}', code).replace('{input_structure}',
        #                                                                                     code_structure)}]  # 消息内容  将提示词中的代码占位符换成代码 代码结构占位符换成代码结构
        prompt = prompt.replace('{input_code}', code).replace('{input_structure}',code_structure)

        nested_content = self.llm.call_LLM(prompt).strip('@Output{').strip('}').strip('\n').strip('[').strip(']').strip(
            '\n')  # 调用大模型 去除返回内容的包裹符号和头尾的空行
        return nested_content

    def get_subgraph(self, code, nested_blocks):
        """
        :param code_path: 代码文件地址
        :param nested_path: 代码块文件地址
        :param language:代码语言
        :return: -
        """
        prompt = self.read_file('prompt/' + self.language + '/subgraph_prompt.txt')  # 提示词
        # message = [{"role": "user", "content": prompt.replace('{input_code}', code).replace('{input_nested}',
        #                                                                                     nested)}]
        prompt = prompt.replace('{input_code}', code).replace('{input_nested}',nested_blocks)

        subgraph_content = self.llm.call_LLM(prompt).strip('@Output{').strip('}').strip('\n').strip('[').strip(']').strip(
            '\n')  # 调用大模型 去除返回内容的包裹符号和头尾的空行
        return subgraph_content

    def fusion_subgraph(self, code, subgraph):
        """
        :param code_path: 代码文件地址
        :param subgraph_path: 子图文件地址
        :param language:代码语言
        :return: -
        """
        prompt = self.read_file('prompt/' + self.language + '/fusion_prompt.txt')  # 提示词
  # 消息内容  将提示词中的代码占位符换成代码 子图占位符换成子图
        prompt = prompt.replace('{input_code}',code).replace('{input_subgraph}', subgraph)
        fusion_content = self.llm.call_LLM(prompt).strip('@Output{').strip('}').strip('\n').strip('[').strip(']').strip(
            '\n')  # 调用大模型 去除返回内容的包裹符号和头尾的空行
        fusion_code = "from graphviz import Digraph\ndot = Digraph()\ndot.attr('node', fontname='SimSun')\n" + fusion_content + "\ndot.render('graph', format='png', view=False)"

        self.write_file("./graph_code.py", fusion_code)  # 写入文件到指定地址
        return fusion_code

    # 生成graphviz流程图
    def generation(self,create_graph_code):
        """
        :param create_graph_code: 完整的graphviz生成流程图的代码文件地址
        :param language:代码语言
        :return: -
        """
        subprocess.run(['python', "./graph_code.py"])  # 执行生成流程图的代码文件
        # print('graph:成功生成流程图!')

    def unit_chain(self, code):
        if self.language == 'Python':
             code = self.unwrap_code(code)
        code_structure = self.get_structure(code)
        nested_blocks = self.get_nested(code,code_structure)
        subgraphs = self.get_subgraph(code, nested_blocks)
        fusion_code = self.fusion_subgraph(code, subgraphs)
        self.generation(fusion_code)

if __name__ == '__main__':
    code = '''\
public static void heapsort(int[] a) {
    for (int i = 0; i < a.length; i++) {
        for (int j = i * 3 + 1; j < i * 3 + 4; j++) {
            if (j < a.length) {
                if (a[j] < a[i]) {
                    switchPos(a, i, j);
                    heapsort(a);
                }
            }
        }
    }
}
'''
    cfg = CFG('Java', 'openai', 'gpt-4-0613')
    cfg.unit_chain(code)
