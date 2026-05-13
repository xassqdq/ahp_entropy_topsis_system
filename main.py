"""
AHP + 熵权法 + TOPSIS 完整自动化工作流主入口
数学建模竞赛一键运行脚本

使用方式：
    python main.py --mode full --data data/data.csv --ahp data/ahp_matrix.json
    python main.py --mode fast --data data/data.csv
    python main.py --mode expert --ahp data/ahp_matrix.json
"""

import sys
import os
import argparse
import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Tuple, Optional

# 导入所有模块
from modules.data_loader import DataLoader
from modules.indicator_processor import IndicatorProcessor
from modules.standardizer import Standardizer
from modules.ahp_engine import AHPEngine
from modules.entropy_engine import EntropyEngine
from modules.weight_combiner import WeightCombiner
from modules.topsis_engine import TOPSISEngine
from modules.visualizer import Visualizer


class AHPEntropyTOPSISWorkflow:
    """完整工作流主类"""

    def __init__(self, mode: str = 'full',
                 data_path: str = None,
                 indicators_path: str = None,
                 ahp_matrix_path: str = None,
                 results_dir: str = 'results',
                 combination_method: str = 'multiplicative',
                 alpha: float = 0.5):
        """
        初始化工作流

        Args:
            mode: 运行模式 ('full'|'fast'|'expert')
            data_path: 原始数据CSV路径
            indicators_path: 指标配置JSON路径
            ahp_matrix_path: AHP判断矩阵JSON路径
            results_dir: 结果输出目录
            combination_method: 权重组合方法 ('multiplicative'|'linear')
            alpha: 线性组合系数（仅linear模式）
        """
        self.mode = mode
        self.data_path = data_path
        self.indicators_path = indicators_path
        self.ahp_matrix_path = ahp_matrix_path
        self.results_dir = results_dir
        self.combination_method = combination_method
        self.alpha = alpha

        # 工作流组件
        self.data_loader = None
        self.indicator_processor = None
        self.standardizer = None
        self.ahp_engine = None
        self.entropy_engine = None
        self.weight_combiner = None
        self.topsis_engine = None
        self.visualizer = None

        # 中间结果
        self.raw_data = None
        self.objects = None
        self.indicators = None
        self.processed_data = None
        self.vector_normalized = None
        self.range_normalized = None
        self.ahp_weights = None
        self.entropy_weights = None
        self.combined_weights = None
        self.topsis_results = None
        self.ahp_consistency = None

        self._print_header()

    def _print_header(self):
        """打印工作流头部信息"""
        print("\n" + "=" * 70)
        print("  AHP + 熵权法 + TOPSIS 完整自动化工作流")
        print("  Mathematical Modeling Competition Standard Implementation")
        print("=" * 70)
        print(f"  运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  运行模式: {self.mode.upper()}")
        print("=" * 70 + "\n")

    def validate_inputs(self) -> bool:
        """
        验证输入参数

        Returns:
            输入是否有效
        """
        print("【输入参数验证】")

        if self.mode == 'full':
            if not self.data_path:
                print("✗ full模式需要提供 --data 参数")
                return False
            if not os.path.exists(self.data_path):
                print(f"✗ 数据文件不存在: {self.data_path}")
                return False
            if not self.ahp_matrix_path:
                print("✗ full模式需要提供 --ahp 参数")
                return False
            if not os.path.exists(self.ahp_matrix_path):
                print(f"✗ AHP判断矩阵文件不存在: {self.ahp_matrix_path}")
                return False
            print("✓ full模式参数验证通过")

        elif self.mode == 'fast':
            if not self.data_path:
                print("✗ fast模式需要提供 --data 参数")
                return False
            if not os.path.exists(self.data_path):
                print(f"✗ 数据文件不存在: {self.data_path}")
                return False
            print("✓ fast模式参数验证通过")

        elif self.mode == 'expert':
            if not self.ahp_matrix_path:
                print("✗ expert模式需要提供 --ahp 参数")
                return False
            if not os.path.exists(self.ahp_matrix_path):
                print(f"✗ AHP判断矩阵文件不存在: {self.ahp_matrix_path}")
                return False
            print("✓ expert模式参数验证通过")

        else:
            print(f"✗ 未知的运行模式: {self.mode}")
            return False

        return True

    def run_full_mode(self):
        """
        完整模式：AHP + 熵权 + TOPSIS
        需要：原始数据 + AHP判断矩阵
        """
        print("\n" + "=" * 70)
        print("【完整模式工作流】AHP + 熵权法 + TOPSIS")
        print("=" * 70)

        # 1. 数据加载
        print("\n[步骤1] 数据加载与预处理")
        self._load_data()

        # 2. 指标同趋化
        print("\n[步骤2] 指标同趋化处理")
        self._process_indicators()

        # 3. 标准化
        print("\n[步骤3] 标准化处理")
        self._standardize_data()

        # 4. AHP权重计算
        print("\n[步骤4] AHP权重计算与一致性检验")
        self._calculate_ahp_weights()

        # 5. 熵权计算
        print("\n[步骤5] 熵权法权重计算")
        self._calculate_entropy_weights()

        # 6. 权重组合
        print("\n[步骤6] 权重组合赋权")
        self._combine_weights()

        # 7. TOPSIS排序
        print("\n[步骤7] TOPSIS排序计算")
        self._calculate_topsis()

        # 8. 结果输出
        print("\n[步骤8] 结果可视化与输出")
        self._generate_outputs()

        print("\n" + "=" * 70)
        print("✓ 完整模式工作流执行完成")
        print("=" * 70)

    def run_fast_mode(self):
        """
        快速模式：熵权法 + TOPSIS
        仅需：原始数据（纯数据驱动）
        """
        print("\n" + "=" * 70)
        print("【快速模式工作流】熵权法 + TOPSIS (纯数据驱动)")
        print("=" * 70)

        # 1. 数据加载
        print("\n[步骤1] 数据加载与预处理")
        self._load_data()

        # 2. 指标同趋化
        print("\n[步骤2] 指标同趋化处理")
        self._process_indicators()

        # 3. 标准化
        print("\n[步骤3] 标准化处理")
        self._standardize_data()

        # 4. 熵权计算
        print("\n[步骤4] 熵权法权重计算")
        self._calculate_entropy_weights()

        # 5. TOPSIS排序（使用熵权）
        print("\n[步骤5] TOPSIS排序计算")
        self.combined_weights = self.entropy_weights
        self._calculate_topsis()

        # 6. 结果输出
        print("\n[步骤6] 结果可视化与输出")
        self._generate_outputs(skip_ahp=True)

        print("\n" + "=" * 70)
        print("✓ 快速模式工作流执行完成")
        print("=" * 70)

    def run_expert_mode(self):
        """
        专家模式：AHP权重排序
        仅需：AHP判断矩阵（定性量化）
        """
        print("\n" + "=" * 70)
        print("【专家模式工作流】AHP权重排序 (定性量化)")
        print("=" * 70)

        # 1. AHP权重计算
        print("\n[步骤1] AHP权重计算与一致性检验")
        self._calculate_ahp_weights_only()

        # 2. 结果输出
        print("\n[步骤2] 结果输出")
        self._generate_expert_outputs()

        print("\n" + "=" * 70)
        print("✓ 专家模式工作流执行完成")
        print("=" * 70)

    def _load_data(self):
        """加载数据"""
        self.data_loader = DataLoader(
            self.data_path,
            self.indicators_path
        )

        self.raw_data, self.objects, self.indicators = \
            self.data_loader.load_data()

        self.data_loader.load_indicators_config()

        if not self.data_loader.validate_data():
            raise ValueError("数据验证失败")

        summary = self.data_loader.get_summary()
        print(f"\n  数据摘要:")
        print(f"    评价对象: {summary['n_objects']}")
        print(f"    评价指标: {summary['n_indicators']}")
        print(f"    数据范围: [{summary['data_min']:.4f}, {summary['data_max']:.4f}]")

    def _process_indicators(self):
        """指标同趋化处理"""
        self.indicator_processor = IndicatorProcessor(
            self.raw_data,
            self.indicators,
            self.data_loader.indicators_config
        )

        self.processed_data = self.indicator_processor.process()

    def _standardize_data(self):
        """标准化处理"""
        self.standardizer = Standardizer(self.processed_data)
        self.vector_normalized, self.range_normalized = \
            self.standardizer.standardize_all()

    def _calculate_ahp_weights(self):
        """AHP权重计算与一致性检验"""
        self.ahp_engine = AHPEngine(
            len(self.indicators),
            self.ahp_matrix_path
        )

        self.ahp_engine.load_judgment_matrix()
        self.ahp_weights = self.ahp_engine.calculate_weights()

        cr, pass_flag, details = self.ahp_engine.check_consistency()
        self.ahp_consistency = details

    def _calculate_ahp_weights_only(self):
        """仅计算AHP权重（专家模式）"""
        # 从AHP判断矩阵推断指标数
        with open(self.ahp_matrix_path, 'r', encoding='utf-8') as f:
            matrix = json.load(f)

        n_indicators = len(matrix)

        self.ahp_engine = AHPEngine(
            n_indicators,
            self.ahp_matrix_path
        )

        self.ahp_engine.load_judgment_matrix()
        self.ahp_weights = self.ahp_engine.calculate_weights()

        cr, pass_flag, details = self.ahp_engine.check_consistency()
        self.ahp_consistency = details

    def _calculate_entropy_weights(self):
        """熵权法权重计算"""
        self.entropy_engine = EntropyEngine(self.range_normalized)

        self.entropy_engine.calculate_entropy()
        self.entropy_engine.calculate_divergence()
        self.entropy_weights = self.entropy_engine.calculate_weights()

    def _combine_weights(self):
        """权重组合赋权"""
        self.weight_combiner = WeightCombiner(
            self.ahp_weights,
            self.entropy_weights
        )

        if self.combination_method == 'multiplicative':
            self.combined_weights = self.weight_combiner.combine_multiplicative()
        else:
            self.combined_weights = self.weight_combiner.combine_linear(self.alpha)

    def _calculate_topsis(self):
        """TOPSIS排序计算"""
        self.topsis_engine = TOPSISEngine(
            self.vector_normalized,
            self.combined_weights
        )

        self.topsis_engine.calculate_weighted_matrix()
        self.topsis_engine.determine_ideal_solutions()
        self.topsis_engine.calculate_distances()
        self.topsis_engine.calculate_closeness()

        ranking, ranked_closeness = self.topsis_engine.get_ranking()

        self.topsis_results = self.topsis_engine.get_results_summary(
            self.objects
        )

    def _generate_outputs(self, skip_ahp: bool = False):
        """生成所有输出"""
        self.visualizer = Visualizer(self.results_dir)

        # 1. 生成结果表格
        results_df = self.visualizer.generate_results_table(
            self.objects,
            self.topsis_results['closeness'],
            self.topsis_results['ranking']
        )

        print("\n【TOPSIS排序结果】")
        print(results_df.to_string(index=False))

        # 2. 生成权重表格
        weights_df = self.visualizer.generate_weights_table(
            self.indicators,
            self.ahp_weights if not skip_ahp else None,
            self.entropy_weights,
            self.combined_weights
        )

        print("\n【权重汇总表】")
        print(weights_df.to_string(index=False))

        # 3. 生成一致性检验结果
        if not skip_ahp and self.ahp_consistency:
            print("\n【AHP一致性检验】")
            print(f"  λmax = {self.ahp_consistency['lambda_max']:.6f}")
            print(f"  CI = {self.ahp_consistency['ci']:.6f}")
            print(f"  RI = {self.ahp_consistency['ri']:.6f}")
            print(f"  CR = {self.ahp_consistency['cr']:.6f}")
            status = "✓ 通过" if self.ahp_consistency['pass'] else "✗ 未通过"
            print(f"  结论: {status}")

        # 4. 绘制图表
        print("\n【生成可视化图表】")

        if not skip_ahp:
            self.visualizer.plot_weights_distribution(
                self.indicators,
                self.ahp_weights,
                self.entropy_weights,
                self.combined_weights
            )
        else:
            self.visualizer.plot_weights_distribution(
                self.indicators,
                entropy_weights=self.entropy_weights,
                combined_weights=self.combined_weights
            )

        self.visualizer.plot_topsis_ranking(
            self.objects,
            self.topsis_results['closeness'],
            self.topsis_results['ranking']
        )

        self.visualizer.plot_radar_chart(
            self.objects,
            self.indicators,
            self.vector_normalized,
            top_n=3
        )

        # 5. 生成LaTeX代码
        latex_tables = {
            'Results Table': self.visualizer.generate_latex_table(
                results_df,
                'TOPSIS Ranking Results'
            ),
            'Weights Table': self.visualizer.generate_latex_table(
                weights_df,
                'Weight Summary'
            )
        }

        # 6. 保存所有结果
        self.visualizer.save_all_results(
            results_df,
            weights_df,
            self.ahp_consistency if not skip_ahp else None,
            latex_tables
        )

        print("\n✓ 所有输出已生成")

    def _generate_expert_outputs(self):
        """生成专家模式输出"""
        self.visualizer = Visualizer(self.results_dir)

        # 从AHP判断矩阵推断指标名称
        with open(self.ahp_matrix_path, 'r', encoding='utf-8') as f:
            matrix = json.load(f)

        n_indicators = len(matrix)
        indicators = [f'Indicator {i + 1}' for i in range(n_indicators)]

        # 生成权重表格
        weights_df = pd.DataFrame({
            'Indicator': indicators,
            'AHP Weight': np.round(self.ahp_weights, 6),
            'Ranking': np.argsort(-self.ahp_weights) + 1
        })

        print("\n【AHP权重排序结果】")
        print(weights_df.to_string(index=False))

        print("\n【AHP一致性检验】")
        print(f"  λmax = {self.ahp_consistency['lambda_max']:.6f}")
        print(f"  CI = {self.ahp_consistency['ci']:.6f}")
        print(f"  RI = {self.ahp_consistency['ri']:.6f}")
        print(f"  CR = {self.ahp_consistency['cr']:.6f}")
        status = "✓ 通过" if self.ahp_consistency['pass'] else "✗ 未通过"
        print(f"  结论: {status}")

        # 绘制权重分布图
        self.visualizer.plot_weights_distribution(
            indicators,
            ahp_weights=self.ahp_weights
        )

        # 保存结果
        weights_df.to_csv(
            os.path.join(self.results_dir, 'ahp_weights.csv'),
            index=False, encoding='utf-8-sig'
        )

        with open(os.path.join(self.results_dir, 'ahp_consistency.txt'),
                  'w', encoding='utf-8') as f:
            f.write("AHP Consistency Check Results\n")
            f.write("=" * 50 + "\n\n")
            for key, value in self.ahp_consistency.items():
                f.write(f"{key}: {value}\n")

        print("\n✓ 专家模式输出已生成")

    def run(self):
        """执行工作流"""
        try:
            if not self.validate_inputs():
                return False

            if self.mode == 'full':
                self.run_full_mode()
            elif self.mode == 'fast':
                self.run_fast_mode()
            elif self.mode == 'expert':
                self.run_expert_mode()

            print("\n" + "=" * 70)
            print("✓ 工作流执行成功")
            print(f"  结果已保存到: {os.path.abspath(self.results_dir)}/")
            print("=" * 70 + "\n")

            return True

        except Exception as e:
            print(f"\n✗ 工作流执行出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AHP + 熵权法 + TOPSIS 完整自动化工作流',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  # 完整模式（需要数据和AHP判断矩阵）
  python main.py --mode full --data data/data.csv --ahp data/ahp_matrix.json

  # 快速模式（仅需数据，纯数据驱动）
  python main.py --mode fast --data data/data.csv

  # 专家模式（仅需AHP判断矩阵）
  python main.py --mode expert --ahp data/ahp_matrix.json

  # 自定义权重组合方法
  python main.py --mode full --data data/data.csv --ahp data/ahp_matrix.json \\
                 --combination linear --alpha 0.6
        """
    )

    parser.add_argument(
        '--mode',
        type=str,
        default='full',
        choices=['full', 'fast', 'expert'],
        help='运行模式 (default: full)'
    )

    parser.add_argument(
        '--data',
        type=str,
        default='data/data.csv',
        help='原始数据CSV文件路径 (default: data/data.csv)'
    )

    parser.add_argument(
        '--indicators',
        type=str,
        default='data/indicators.json',
        help='指标配置JSON文件路径 (default: data/indicators.json)'
    )

    parser.add_argument(
        '--ahp',
        type=str,
        default='data/ahp_matrix.json',
        help='AHP判断矩阵JSON文件路径 (default: data/ahp_matrix.json)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='results',
        help='结果输出目录 (default: results)'
    )

    parser.add_argument(
        '--combination',
        type=str,
        default='multiplicative',
        choices=['multiplicative', 'linear'],
        help='权重组合方法 (default: multiplicative)'
    )

    parser.add_argument(
        '--alpha',
        type=float,
        default=0.5,
        help='线性组合系数 (default: 0.5, 仅在--combination linear时有效)'
    )

    args = parser.parse_args()

    # 创建工作流实例
    workflow = AHPEntropyTOPSISWorkflow(
        mode=args.mode,
        data_path=args.data,
        indicators_path=args.indicators,
        ahp_matrix_path=args.ahp,
        results_dir=args.output,
        combination_method=args.combination,
        alpha=args.alpha
    )

    # 执行工作流
    success = workflow.run()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()