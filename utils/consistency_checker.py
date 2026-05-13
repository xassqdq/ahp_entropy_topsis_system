"""
AHP一致性检验工具库
用于检验判断矩阵的一致性
"""

import numpy as np
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class ConsistencyChecker:
    """AHP一致性检验工具类"""

    # 随机一致性指数表（Saaty提供）
    RI_TABLE = {
        1: 0.00,
        2: 0.00,
        3: 0.58,
        4: 0.90,
        5: 1.12,
        6: 1.24,
        7: 1.32,
        8: 1.41,
        9: 1.45,
        10: 1.49,
        11: 1.51,
        12: 1.48,
        13: 1.56,
        14: 1.57,
        15: 1.59
    }

    @staticmethod
    def get_ri_value(n: int) -> float:
        """
        获取随机一致性指数RI

        Args:
            n: 矩阵阶数

        Returns:
            RI值
        """
        if n in ConsistencyChecker.RI_TABLE:
            return ConsistencyChecker.RI_TABLE[n]
        else:
            logger.warning(f"矩阵阶数{n}超出RI表范围，使用线性插值")
            # 对于超出范围的阶数，使用线性插值
            if n > 15:
                return 1.59 + (n - 15) * 0.01
            else:
                return 0.0

    @staticmethod
    def calculate_max_eigenvalue(matrix: np.ndarray) -> float:
        """
        计算矩阵的最大特征值

        Args:
            matrix: 判断矩阵

        Returns:
            最大特征值
        """
        matrix = np.array(matrix, dtype=float)
        eigenvalues = np.linalg.eigvals(matrix)
        # 取实部，因为可能有复数特征值
        eigenvalues = np.real(eigenvalues)
        return float(np.max(eigenvalues))

    @staticmethod
    def calculate_consistency_index(matrix: np.ndarray) -> float:
        """
        计算一致性指数CI

        公式：CI = (λmax - n) / (n - 1)

        Args:
            matrix: 判断矩阵

        Returns:
            一致性指数CI
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        if n == 1:
            return 0.0

        lambda_max = ConsistencyChecker.calculate_max_eigenvalue(matrix)
        ci = (lambda_max - n) / (n - 1)

        return float(ci)

    @staticmethod
    def calculate_consistency_ratio(matrix: np.ndarray) -> float:
        """
        计算一致性比率CR

        公式：CR = CI / RI

        Args:
            matrix: 判断矩阵

        Returns:
            一致性比率CR
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        if n == 1:
            return 0.0

        ci = ConsistencyChecker.calculate_consistency_index(matrix)
        ri = ConsistencyChecker.get_ri_value(n)

        if ri == 0:
            return 0.0

        cr = ci / ri

        return float(cr)

    @staticmethod
    def check_consistency(matrix: np.ndarray, cr_threshold: float = 0.1) -> Tuple[bool, Dict]:
        """
        检验矩阵的一致性

        Args:
            matrix: 判断矩阵
            cr_threshold: 一致性检验阈值（默认0.1）

        Returns:
            (是否通过, 详细信息字典)
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        # 计算各项指标
        lambda_max = ConsistencyChecker.calculate_max_eigenvalue(matrix)
        ci = ConsistencyChecker.calculate_consistency_index(matrix)
        ri = ConsistencyChecker.get_ri_value(n)
        cr = ConsistencyChecker.calculate_consistency_ratio(matrix)

        # 判定是否通过
        passed = cr < cr_threshold if n > 2 else True

        result = {
            'matrix_order': n,
            'max_eigenvalue': lambda_max,
            'consistency_index': ci,
            'random_index': ri,
            'consistency_ratio': cr,
            'threshold': cr_threshold,
            'passed': passed,
            'message': f"一致性检验{'通过' if passed else '未通过'} (CR = {cr:.4f} {'<' if passed else '≥'} {cr_threshold})"
        }

        return passed, result

    @staticmethod
    def generate_consistency_report(matrix: np.ndarray,
                                    weights: np.ndarray = None,
                                    cr_threshold: float = 0.1) -> str:
        """
        生成一致性检验报告

        Args:
            matrix: 判断矩阵
            weights: 权重向量（可选）
            cr_threshold: 一致性检验阈值

        Returns:
            报告文本
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        passed, result = ConsistencyChecker.check_consistency(matrix, cr_threshold)

        report = []
        report.append("=" * 60)
        report.append("AHP一致性检验报告")
        report.append("=" * 60)
        report.append("")

        # 基本信息
        report.append(f"判断矩阵阶数: {n}")
        report.append("")

        # 判断矩阵
        report.append("判断矩阵:")
        for i in range(n):
            row_str = "  " + "  ".join([f"{matrix[i, j]:8.4f}" for j in range(n)])
            report.append(row_str)
        report.append("")

        # 特征值和特征向量
        if weights is not None:
            report.append("权重向量:")
            for i, w in enumerate(weights):
                report.append(f"  w{i + 1} = {w:.4f}")
            report.append("")

        # 一致性指标
        report.append("一致性指标:")
        report.append(f"  最大特征值 (λmax): {result['max_eigenvalue']:.6f}")
        report.append(f"  一致性指数 (CI):  {result['consistency_index']:.6f}")
        report.append(f"  随机一致性指数 (RI): {result['random_index']:.6f}")
        report.append(f"  一致性比率 (CR):  {result['consistency_ratio']:.6f}")
        report.append("")

        # 检验结论
        report.append("检验结论:")
        if passed:
            report.append(f"✓ 一致性检验通过 (CR = {result['consistency_ratio']:.4f} < {cr_threshold})")
            report.append("  判断矩阵具有满意的一致性，可直接使用。")
        else:
            report.append(f"✗ 一致性检验未通过 (CR = {result['consistency_ratio']:.4f} ≥ {cr_threshold})")
            report.append("  建议调整判断矩阵中的某些元素以提高一致性。")
        report.append("")

        # 调整建议
        if not passed:
            report.append("调整建议:")
            report.append("  1. 检查判断矩阵中数值最大和最小的元素")
            report.append("  2. 重新审视这些元素对应的比较关系")
            report.append("  3. 根据实际情况调整判断矩阵")
            report.append("  4. 重新计算权重并检验一致性")
            report.append("")

        report.append("=" * 60)

        return "\n".join(report)

    @staticmethod
    def find_inconsistent_pairs(matrix: np.ndarray,
                                tolerance: float = 0.1) -> list:
        """
        找出矩阵中不一致的元素对

        Args:
            matrix: 判断矩阵
            tolerance: 容差值

        Returns:
            不一致的元素对列表
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        inconsistent_pairs = []

        # 检查互反性
        for i in range(n):
            for j in range(i + 1, n):
                product = matrix[i, j] * matrix[j, i]
                if abs(product - 1.0) > tolerance:
                    inconsistent_pairs.append({
                        'position': (i, j),
                        'value_ij': matrix[i, j],
                        'value_ji': matrix[j, i],
                        'product': product,
                        'error': abs(product - 1.0)
                    })

        return inconsistent_pairs

    @staticmethod
    def suggest_matrix_adjustment(matrix: np.ndarray,
                                  cr_threshold: float = 0.1) -> Dict:
        """
        建议矩阵调整方案

        Args:
            matrix: 判断矩阵
            cr_threshold: 一致性检验阈值

        Returns:
            调整建议字典
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        passed, result = ConsistencyChecker.check_consistency(matrix, cr_threshold)

        suggestions = {
            'passed': passed,
            'cr': result['consistency_ratio'],
            'threshold': cr_threshold,
            'inconsistent_pairs': ConsistencyChecker.find_inconsistent_pairs(matrix),
            'adjustment_steps': []
        }

        if not passed:
            cr_excess = result['consistency_ratio'] - cr_threshold
            suggestions['adjustment_steps'].append(
                f"当前CR超过阈值 {cr_excess:.4f}，需要调整"
            )

            # 找出最不一致的元素对
            if suggestions['inconsistent_pairs']:
                worst_pair = max(suggestions['inconsistent_pairs'],
                                 key=lambda x: x['error'])
                i, j = worst_pair['position']
                suggestions['adjustment_steps'].append(
                    f"优先调整位置({i},{j})的元素，当前值为{worst_pair['value_ij']:.4f}"
                )

        return suggestions