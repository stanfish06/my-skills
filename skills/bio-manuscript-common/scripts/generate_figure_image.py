#!/usr/bin/env python3
"""
Figure 图文生成器

调用 Gemini API 生成 Figure 1 Panel b-c-d-e 的图文。
"""

import os
from typing import Optional, Dict, List


class FigureImageGenerator:
    """Figure 图文生成器"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化
        
        Args:
            api_key: Gemini API key（也可从环境变量获取）
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            print("Warning: No Gemini API key provided. Image generation will be simulated.")
    
    def generate_panel_image(self,
                            panel_type: str,
                            content: str,
                            description: str,
                            output_path: str) -> Dict:
        """
        生成 Panel 图文
        
        Args:
            panel_type: Panel 类型（data/task/metric/analysis）
            content: 内容描述
            description: 简短描述
            output_path: 输出路径
            
        Returns:
            生成结果
        """
        prompt = self._build_prompt(panel_type, content, description)
        
        # 调用 Gemini API（简化版）
        result = self._call_gemini(prompt, output_path)
        
        return result
    
    def _build_prompt(self, panel_type: str, content: str, description: str) -> str:
        """构建 prompt"""
        
        panel_descriptions = {
            "data": "数据类型介绍",
            "task": "任务层级介绍",
            "metric": "评价指标介绍",
            "analysis": "分析方法介绍"
        }
        
        prompt = f"""
生成一个简洁的科学论文插图，用于 Nature Methods 论文 Figure 1。

Panel 类型：{panel_descriptions.get(panel_type, panel_type)}

内容：{content}

简短描述：{description}

要求：
1. 风格：Nature Methods 论文插图，简洁清晰，配色专业
2. 布局：包含标题标签 + 示意图 + 简短描述文字
3. 颜色：专业科学论文配色，避免过于鲜艳
4. 尺寸：适合 Figure 1 Panel（约 60mm × 30mm 每个项目）
5. 格式：矢量图或高分辨率位图

请生成一个框框样式的设计，框框内包含：
- 内容名称（如 "Proteomics"）
- 简洁的示意图
- 一句话描述
"""
        return prompt
    
    def _call_gemini(self, prompt: str, output_path: str) -> Dict:
        """调用 Gemini API"""
        
        if not self.api_key:
            # 模拟生成
            return {
                "success": False,
                "message": "No API key provided. This is a simulation.",
                "prompt": prompt,
                "output_path": output_path,
                "note": "Please provide GEMINI_API_KEY to enable actual image generation."
            }
        
        try:
            # 实际调用 Gemini API
            # import google.generativeai as genai
            # genai.configure(api_key=self.api_key)
            # 'gemini-pro-vision' was retired; use the current image-capable
            # model id from https://ai.google.dev/gemini-api/docs/models
            # model = genai.GenerativeModel(GEMINI_IMAGE_MODEL)
            # response = model.generate_content(prompt)
            # ... 保存图片
            
            # NOTE: the actual Gemini call and image-saving code above are not
            # implemented yet, so no image file is written. Report failure rather
            # than claiming success, otherwise callers assume a panel exists.
            return {
                "success": False,
                "prompt": prompt,
                "output_path": output_path,
                "message": "Gemini image generation is not implemented; no image was written.",
                "note": "Implement the google.generativeai call above and save the image before marking success."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "prompt": prompt
            }
    
    def generate_figure1_panel_b(self, data_types: List[Dict]) -> Dict:
        """
        生成 Figure 1 Panel b（数据介绍）
        
        Args:
            data_types: 数据类型列表
                [{"name": "Proteomics", "description": "蛋白质表达测量"}, ...]
                
        Returns:
            生成结果
        """
        results = []
        
        for data_type in data_types:
            result = self.generate_panel_image(
                panel_type="data",
                content=data_type["name"],
                description=data_type["description"],
                output_path=f"figure1_panel_b_{data_type['name'].lower()}.png"
            )
            results.append(result)
        
        return {
            "panel": "Figure 1 Panel b",
            "results": results
        }
    
    def generate_figure1_panel_c(self, tasks: List[Dict]) -> Dict:
        """
        生成 Figure 1 Panel c（任务介绍）
        
        Args:
            tasks: 任务列表
                [{"name": "Vertical Integration", "description": "同细胞多模态"}, ...]
                
        Returns:
            生成结果
        """
        results = []
        
        for task in tasks:
            result = self.generate_panel_image(
                panel_type="task",
                content=task["name"],
                description=task["description"],
                output_path=f"figure1_panel_c_{task['name'].lower().replace(' ', '_')}.png"
            )
            results.append(result)
        
        return {
            "panel": "Figure 1 Panel c",
            "results": results
        }
    
    def generate_figure1_panel_d(self, metrics: List[Dict]) -> Dict:
        """
        生成 Figure 1 Panel d（指标介绍）
        
        Args:
            metrics: 指标列表
                [{"name": "ARI", "description": "聚类一致性评估"}, ...]
                
        Returns:
            生成结果
        """
        results = []
        
        for metric in metrics:
            result = self.generate_panel_image(
                panel_type="metric",
                content=metric["name"],
                description=metric["description"],
                output_path=f"figure1_panel_d_{metric['name'].lower()}.png"
            )
            results.append(result)
        
        return {
            "panel": "Figure 1 Panel d",
            "results": results
        }
    
    def generate_figure1_panel_e(self, analyses: List[Dict]) -> Dict:
        """
        生成 Figure 1 Panel e（分析介绍）
        
        Args:
            analyses: 分析列表
                [{"name": "Clustering", "description": "Leiden聚类"}, ...]
                
        Returns:
            生成结果
        """
        results = []
        
        for analysis in analyses:
            result = self.generate_panel_image(
                panel_type="analysis",
                content=analysis["name"],
                description=analysis["description"],
                output_path=f"figure1_panel_e_{analysis['name'].lower()}.png"
            )
            results.append(result)
        
        return {
            "panel": "Figure 1 Panel e",
            "results": results
        }


def main():
    """主函数"""
    generator = FigureImageGenerator()
    
    # 示例：生成 Panel b（数据介绍）
    data_types = [
        {"name": "Proteomics", "description": "蛋白质表达测量，提供细胞功能信息"},
        {"name": "Transcriptomics", "description": "全转录组表达，揭示基因调控"},
        {"name": "Epigenomics", "description": "表观遗传修饰，反映染色质状态"},
    ]
    
    result = generator.generate_figure1_panel_b(data_types)
    
    print(f"Panel: {result['panel']}")
    print(f"Generated {len(result['results'])} items")
    
    for r in result['results']:
        print(f"  - {r.get('output_path', 'N/A')}: {r.get('message', r.get('error', 'Unknown'))}")


if __name__ == "__main__":
    main()