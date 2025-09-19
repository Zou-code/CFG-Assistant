import os
import sys
import time
import uuid
import subprocess
from typing import Dict, Any, Optional
import tempfile
import shutil

# 添加项目根目录到Python路径以导入现有的CFG模块
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

try:
    from services.CFG_Generation import CFG
except ImportError:
    try:
        # 尝试从backend目录导入
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        sys.path.insert(0, backend_dir)
        from services.CFG_Generation import CFG
    except ImportError:
        # 如果导入失败，创建一个简单的模拟类
        class CFG:
            def __init__(self, language, client_name, model_name):
                self.language = language
                self.client_name = client_name
                self.model_name = model_name
                self.llm = type('LLM', (), {'temperature': 0.0})()
            
            def unit_chain(self, code):
                # 简单的模拟实现
                return 'digraph G { A -> B; B -> C; }'
from models.schemas import CFGGenerationRequest, LanguageEnum, ModelEnum, ClientEnum

class CFGService:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def __del__(self):
        # 清理临时目录
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def generate_cfg(self, request: CFGGenerationRequest) -> Dict[str, Any]:
        """
        生成控制流图
        """
        start_time = time.time()
        
        # 添加特殊标识确认这个方法被调用
        print(f"[CRITICAL] CFGService.generate_cfg 方法被调用！")
        
        try:
            print(f"[DEBUG] 开始CFG生成，语言: {request.language.value}, 模型: {request.model_name.value}")
            
            # 创建CFG实例
            cfg = CFG(
                language=request.language.value,
                client_name=request.client_name.value,
                model_name=request.model_name.value
            )
            print(f"[DEBUG] CFG实例创建成功")
            print(f"[DEBUG] CFG类型: {type(cfg)}")
            print(f"[DEBUG] CFG模块: {cfg.__class__.__module__}")
            print(f"[DEBUG] CFG是否有read_file方法: {hasattr(cfg, 'read_file')}")
            
            # 如果提供了自定义API密钥，更新配置
            if request.api_key:
                self._update_api_key(cfg, request.client_name, request.api_key)
            
            # 设置温度参数
            if hasattr(cfg.llm, 'temperature'):
                cfg.llm.temperature = request.temperature
            
            # 生成唯一的工作目录
            work_dir = os.path.join(self.temp_dir, str(uuid.uuid4()))
            os.makedirs(work_dir, exist_ok=True)
            print(f"[DEBUG] 工作目录创建: {work_dir}")
            
            # 保存原始工作目录
            original_cwd = os.getcwd()
            
            try:
                # 切换到工作目录
                os.chdir(work_dir)
                print(f"[DEBUG] 切换到工作目录: {work_dir}")
                
                # 复制必要的文件
                self._copy_required_files(work_dir)
                print(f"[DEBUG] 必要文件复制完成")
                
                # 执行CFG生成 - 使用unit_chain方法
                print(f"[DEBUG] 开始执行CFG生成...")
                cfg.unit_chain(request.code)
                print(f"[DEBUG] CFG生成执行完成")
                
                # 检查是否生成了图片文件和代码文件
                graph_path = os.path.join(work_dir, "graph.png")
                graph_code_path = os.path.join(work_dir, "graph_code.py")
                
                print(f"[DEBUG] 检查生成的文件:")
                print(f"[DEBUG] - graph.png 存在: {os.path.exists(graph_path)}")
                print(f"[DEBUG] - graph_code.py 存在: {os.path.exists(graph_code_path)}")
                
                # 列出工作目录中的所有文件
                files_in_workdir = os.listdir(work_dir)
                print(f"[DEBUG] 工作目录中的文件: {files_in_workdir}")
                
                result = {
                    "success": True,
                    "message": "CFG生成成功",
                    "processing_time": time.time() - start_time
                }
                
                # 读取生成的图形代码
                fusion_code = ""
                if os.path.exists(graph_code_path):
                    with open(graph_code_path, 'r', encoding='utf-8') as f:
                        fusion_code = f.read()
                    result["graph_code"] = fusion_code
                    
                    # 解析图形数据
                    result["graph_data"] = self._parse_graph_data(fusion_code)
                
                # 如果生成了图片，复制到静态文件目录
                if os.path.exists(graph_path):
                    static_dir = os.path.join(original_cwd, "static")
                    os.makedirs(static_dir, exist_ok=True)
                    
                    image_filename = f"cfg_{uuid.uuid4().hex}.png"
                    static_path = os.path.join(static_dir, image_filename)
                    shutil.copy2(graph_path, static_path)
                    
                    result["image_url"] = f"/static/{image_filename}"
                else:
                    # 检查工作目录中是否有其他png文件
                    import glob
                    png_files = glob.glob(os.path.join(work_dir, "*.png"))
                    print(f"[DEBUG] 工作目录中的PNG文件: {png_files}")
                    if png_files:
                        # 使用找到的第一个png文件
                        graph_path = png_files[0]
                        static_dir = os.path.join(original_cwd, "static")
                        os.makedirs(static_dir, exist_ok=True)
                        
                        image_filename = f"cfg_{uuid.uuid4().hex}.png"
                        static_path = os.path.join(static_dir, image_filename)
                        shutil.copy2(graph_path, static_path)
                        
                        result["image_url"] = f"/static/{image_filename}"
                        print(f"[DEBUG] 使用备用PNG文件，已复制到静态目录: {static_path}")
                    # 如果没有生成图片，但有图形代码，尝试手动生成
                    if fusion_code and "dot.render" in fusion_code:
                        try:
                            print(f"[DEBUG] 尝试手动生成图片...")
                            # 执行图形代码生成图片
                            exec(fusion_code, {'__file__': os.path.join(work_dir, 'graph_code.py')})
                            
                            # 重新检查图片是否生成
                            if os.path.exists(graph_path):
                                print(f"[DEBUG] 手动生成图片成功: {graph_path}")
                                static_dir = os.path.join(original_cwd, "static")
                                os.makedirs(static_dir, exist_ok=True)
                                
                                image_filename = f"cfg_{uuid.uuid4().hex}.png"
                                static_path = os.path.join(static_dir, image_filename)
                                shutil.copy2(graph_path, static_path)
                                
                                result["image_url"] = f"/static/{image_filename}"
                                print(f"[DEBUG] 图片已复制到静态目录: {static_path}")
                            else:
                                print(f"[DEBUG] 手动生成图片失败，文件不存在: {graph_path}")
                                # 检查工作目录中的所有文件
                                all_files = []
                                for root, dirs, files in os.walk(work_dir):
                                    for file in files:
                                        if file.endswith('.png'):
                                            full_path = os.path.join(root, file)
                                            all_files.append(full_path)
                                print(f"[DEBUG] 找到的图片文件: {all_files}")
                        except Exception as e:
                            print(f"[DEBUG] 手动生成图片异常: {str(e)}")
                            result["warning"] = f"图片生成失败: {str(e)}"
                
                return result
                
            finally:
                # 恢复原始工作目录
                os.chdir(original_cwd)
                
        except Exception as e:
            return {
                "success": False,
                "message": f"CFG生成失败: {str(e)}",
                "processing_time": time.time() - start_time
            }
    
    def _update_api_key(self, cfg: CFG, client_name: ClientEnum, api_key: str):
        """更新API密钥"""
        if client_name == ClientEnum.OPENAI:
            cfg.llm.client.api_key = api_key
        elif client_name == ClientEnum.DEEPSEEK:
            if hasattr(cfg.llm, 'client_deepseek'):
                cfg.llm.client_deepseek.api_key = api_key
    
    def _copy_required_files(self, work_dir: str):
        """复制必要的文件到工作目录"""
        # 获取项目根目录
        project_root = os.path.join(os.path.dirname(__file__), '../../')
        
        # 复制prompt目录
        prompt_src = os.path.join(project_root, 'prompt')
        prompt_dst = os.path.join(work_dir, 'prompt')
        if os.path.exists(prompt_src):
            shutil.copytree(prompt_src, prompt_dst)
        
        # 复制config.yaml
        config_src = os.path.join(project_root, 'config.yaml')
        config_dst = os.path.join(work_dir, 'config.yaml')
        if os.path.exists(config_src):
            shutil.copy2(config_src, config_dst)
        
        # 复制util目录
        util_src = os.path.join(project_root, 'util')
        util_dst = os.path.join(work_dir, 'util')
        if os.path.exists(util_src):
            shutil.copytree(util_src, util_dst)
    
    def _parse_graph_data(self, graph_code: str) -> Dict[str, Any]:
        """解析图形代码，提取节点和边的信息"""
        try:
            nodes = []
            edges = []
            node_ids = set()
            
            lines = graph_code.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('dot.node('):
                    # 解析节点
                    node_info = self._parse_node_line(line)
                    if node_info:
                        nodes.append(node_info)
                        node_ids.add(node_info["id"])
                elif line.startswith('dot.edge('):
                    # 解析边
                    edge_info = self._parse_edge_line(line)
                    if edge_info:
                        edges.append(edge_info)
            
            # 如果没有显式的节点定义，从边中推断节点
            if not nodes:
                for edge in edges:
                    for node_id in [edge.get("source"), edge.get("target")]:
                        if node_id and node_id not in node_ids:
                            nodes.append({
                                "id": node_id,
                                "label": node_id
                            })
                            node_ids.add(node_id)
            
            # 确保边的格式正确（同时支持source/target和from/to）
            formatted_edges = []
            for edge in edges:
                formatted_edge = {
                    "source": edge.get("source", edge.get("from")),
                    "target": edge.get("target", edge.get("to")),
                    "from": edge.get("source", edge.get("from")),
                    "to": edge.get("target", edge.get("to"))
                }
                formatted_edges.append(formatted_edge)
            
            return {
                "nodes": nodes,
                "edges": formatted_edges,
                "type": "directed_graph"
            }
        except Exception as e:
            return {
                "error": f"解析图形数据失败: {str(e)}",
                "nodes": [],
                "edges": []
            }
    
    def _parse_node_line(self, line: str) -> Optional[Dict[str, str]]:
        """解析节点行"""
        try:
            import re
            # 支持多种节点定义格式
            patterns = [
                r"dot\.node\('([^']+)',\s*'([^']+)'",  # dot.node('id', 'label')
                r"dot\.node\('([^']+)'\)",              # dot.node('id')
                r"dot\.node\(\"([^\"]+)\",\s*\"([^\"]+)\"",  # 双引号版本
                r"dot\.node\(\"([^\"]+)\"\)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    node_id = match.group(1)
                    label = match.group(2) if match.lastindex >= 2 else node_id
                    return {
                        "id": node_id,
                        "label": label
                    }
        except Exception:
            pass
        return None
    
    def _parse_edge_line(self, line: str) -> Optional[Dict[str, str]]:
        """解析边行"""
        try:
            import re
            # 支持多种边定义格式
            patterns = [
                r"dot\.edge\('([^']+)',\s*'([^']+)'",  # dot.edge('from', 'to')
                r"dot\.edge\(\"([^\"]+)\",\s*\"([^\"]+)\"",  # 双引号版本
            ]
            
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    return {
                        "source": match.group(1),
                        "target": match.group(2),
                        "from": match.group(1),
                        "to": match.group(2)
                    }
        except Exception:
            pass
        return None

# 创建全局服务实例
cfg_service = CFGService()