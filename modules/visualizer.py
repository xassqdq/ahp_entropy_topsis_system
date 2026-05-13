"""
可视化与输出模块
功能：绘图、表格生成、LaTeX代码输出、结果归档
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, List, Tuple
import os
import json

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class Visualizer:
    """可视化与输出类"""

    def __init__(self, results_dir: str = 'results'):
        """
        初始化可视化器

        Args:
            results_dir: 结果输出目录
        """
        self.results_dir = results_dir
        self.figures_dir = os.path.join(results_dir, 'figures')

        # 创建输出目录
        os.makedirs(self.figures_dir, exist_ok=True)

    def plot_weights_distribution(self,
                                  indicators: List[str],
                                  ahp_weights: np.ndarray = None,
                                  entropy_weights: np.ndarray = None,
                                  combined_weights: np.ndarray = None) -> str:
        """
        绘制权重分布柱状图

        Args:
            indicators: 指标名称列表
            ahp_weights: AHP权重
            entropy_weights: 熵权
            combined_weights: 组合权重

        Returns:
            图片保存路径
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        fig.suptitle('Weight Distribution', fontsize=14, fontweight='bold')

        weights_data = [
            (ahp_weights, 'AHP Weights', axes[0]),
            (entropy_weights, 'Entropy Weights', axes[1]),
            (combined_weights, 'Combined Weights', axes[2])
        ]

        for weights, title, ax in weights_data:
            if weights is not None:
                colors = plt.cm.Set3(np.linspace(0, 1, len(indicators)))
                ax.bar(range(len(indicators)), weights, color=colors)
                ax.set_xlabel('Indicators', fontsize=10)
                ax.set_ylabel('Weight', fontsize=10)
                ax.set_title(title, fontsize=11)
                ax.set_xticks(range(len(indicators)))
                ax.set_xticklabels(indicators, rotation=45, ha='right')
                ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        save_path = os.path.join(self.figures_dir, 'weights_distribution.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 权重分布图已保存: {save_path}")
        return save_path

    def plot_topsis_ranking(self,
                            objects: List[str],
                            closeness: np.ndarray,
                            ranking: np.ndarray) -> str:
        """
        绘制TOPSIS排名柱状图

        Args:
            objects: 评价对象名称列表
            closeness: 相对贴近度向量
            ranking: 排名索引

        Returns:
            图片保存路径
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        ranked_objects = [objects[i] for i in ranking]
        ranked_closeness = closeness[ranking]

        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(objects)))
        bars = ax.barh(range(len(ranked_objects)), ranked_closeness, color=colors)

        ax.set_yticks(range(len(ranked_objects)))
        ax.set_yticklabels(ranked_objects)
        ax.set_xlabel('Closeness Degree', fontsize=11)
        ax.set_title('TOPSIS Ranking Results', fontsize=13, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        # 添加数值标签
        for i, (bar, value) in enumerate(zip(bars, ranked_closeness)):
            ax.text(value + 0.01, i, f'{value:.4f}',
                    va='center', fontsize=9)

        plt.tight_layout()

        save_path = os.path.join(self.figures_dir, 'topsis_ranking.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ TOPSIS排名图已保存: {save_path}")
        return save_path

    def plot_radar_chart(self,
                         objects: List[str],
                         indicators: List[str],
                         normalized_matrix: np.ndarray,
                         top_n: int = 3) -> str:
        """
        绘制雷达图（前N个对象）

        Args:
            objects: 评价对象名称列表
            indicators: 指标名称列表
            normalized_matrix: 标准化矩阵
            top_n: 显示前N个对象

        Returns:
            图片保存路径
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='polar')

        # 角度
        angles = np.linspace(0, 2 * np.pi, len(indicators), endpoint=False).tolist()
        angles += angles[:1]  # 闭合

        # 绘制前top_n个对象
        colors = plt.cm.Set2(np.linspace(0, 1, top_n))

        for idx in range(min(top_n, len(objects))):
            values = normalized_matrix[idx].tolist()
            values += values[:1]  # 闭合

            ax.plot(angles, values, 'o-', linewidth=2,
                    label=objects[idx], color=colors[idx])
            ax.fill(angles, values, alpha=0.15, color=colors[idx])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(indicators, fontsize=9)
        ax.set_ylim(0, 1)
        ax.set_title('Radar Chart (Top Objects)',
                     fontsize=13, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)

        plt.tight_layout()

        save_path = os.path.join(self.figures_dir, 'radar_chart.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 雷达图已保存: {save_path}")
        return save_path

    def generate_results_table(self,
                               objects: List[str],
                               closeness: np.ndarray,
                               ranking: np.ndarray) -> pd.DataFrame:
        """
        生成结果表格

        Args:
            objects: 评价对象名称列表
            closeness: 相对贴近度向量
            ranking: 排名索引

        Returns:
            结果DataFrame
        """
        ranked_objects = [objects[i] for i in ranking]
        ranked_closeness = closeness[ranking]

        df = pd.DataFrame({
            'Rank': range(1, len(ranked_objects) + 1),
            'Object': ranked_objects,
            'Closeness Degree': np.round(ranked_closeness, 6),
            'Score': np.round(ranked_closeness * 100, 2)
        })

        return df

    def generate_weights_table(self,
                               indicators: List[str],
                               ahp_weights: np.ndarray = None,
                               entropy_weights: np.ndarray = None,
                               combined_weights: np.ndarray = None) -> pd.DataFrame:
        """
        生成权重汇总表格

        Args:
            indicators: 指标名称列表
            ahp_weights: AHP权重
            entropy_weights: 熵权
            combined_weights: 组合权重

        Returns:
            权重DataFrame
        """
        data = {'Indicator': indicators}

        if ahp_weights is not None:
            data['AHP Weight'] = np.round(ahp_weights, 6)

        if entropy_weights is not None:
            data['Entropy Weight'] = np.round(entropy_weights, 6)

        if combined_weights is not None:
            data['Combined Weight'] = np.round(combined_weights, 6)

        df = pd.DataFrame(data)
        return df

    def generate_latex_table(self, df: pd.DataFrame,
                             caption: str = "Results Table") -> str:
        """
        生成LaTeX表格代码

        Args:
            df: 数据框
            caption: 表格标题

        Returns:
            LaTeX代码字符串
        """
        latex_code = df.to_latex(index=False, escape=False)

        # 包装为完整表格环境
        full_latex = f"""
\\begin{{table}}[htbp]
\\centering
\\caption{{{caption}}}
\\label{{tab:results}}
{latex_code}
\\end{{table}}
"""
        return full_latex

    def save_all_results(self,
                         results_summary: pd.DataFrame,
                         weights_table: pd.DataFrame,
                         ahp_consistency: Dict = None,
                         latex_tables: Dict = None):
        """
        保存所有结果到文件

        Args:
            results_summary: 结果汇总表
            weights_table: 权重表
            ahp_consistency: AHP一致性检验结果
            latex_tables: LaTeX表格代码字典
        """
        # 保存CSV表格
        results_summary.to_csv(
            os.path.join(self.results_dir, 'results_summary.csv'),
            index=False, encoding='utf-8-sig'
        )
        print(f"✓ 结果汇总表已保存")

        weights_table.to_csv(
            os.path.join(self.results_dir, 'weights_table.csv'),
            index=False, encoding='utf-8-sig'
        )
        print(f"✓ 权重汇总表已保存")

        # 保存AHP一致性检验结果
        if ahp_consistency:
            with open(os.path.join(self.results_dir, 'ahp_consistency.txt'),
                      'w', encoding='utf-8') as f:
                f.write("AHP Consistency Check Results\n")
                f.write("=" * 50 + "\n\n")
                for key, value in ahp_consistency.items():
                    f.write(f"{key}: {value}\n")
            print(f"✓ AHP一致性检验结果已保存")

        # 保存LaTeX代码
        if latex_tables:
            with open(os.path.join(self.results_dir, 'latex_tables.txt'),
                      'w', encoding='utf-8') as f:
                for name, code in latex_tables.items():
                    f.write(f"\n% {name}\n")
                    f.write(code)
                    f.write("\n" + "=" * 60 + "\n")
            print(f"✓ LaTeX表格代码已保存")

        print(f"\n✓ 所有结果已保存到: {self.results_dir}/")