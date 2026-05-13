"""
熵权法权重计算模块
功能：信息熵计算、差异系数、熵权权重
"""

import numpy as np
from typing import Tuple


class EntropyEngine:
    """熵权法权重计算引擎"""

    def __init__(self, range_normalized_matrix: np.ndarray):
        """
        初始化熵权法引擎

        Args:
            range_normalized_matrix: 极差标准化矩阵 (0~1区间)
        """
        self.normalized_matrix = range_normalized_matrix.copy()
        self.n_objects = range_normalized_matrix.shape[0]
        self.n_indicators = range_normalized_matrix.shape[1]
        self.entropy = None
        self.divergence = None
        self.weights = None

    def calculate_entropy(self) -> np.ndarray:
        """
        计算信息熵

        公式：e_j = -1/ln(m) * sum(p_ij * ln(p_ij))
        其中 p_ij = x_ij / sum(x_ij)

        Returns:
            各指标的信息熵向量
        """
        print("\n【熵权法权重计算】")

        # 计算概率矩阵 p_ij
        col_sums = np.sum(self.normalized_matrix, axis=0)

        # 避免除以零
        col_sums = np.where(col_sums == 0, 1e-10, col_sums)

        probability_matrix = self.normalized_matrix / col_sums

        # 计算信息熵
        # 处理 ln(0) 的情况
        with np.errstate(divide='ignore', invalid='ignore'):
            ln_p = np.log(probability_matrix)
            ln_p = np.where(np.isfinite(ln_p), ln_p, 0)

        self.entropy = -1.0 / np.log(self.n_objects) * np.sum(
            probability_matrix * ln_p,
            axis=0
        )

        print(f"✓ 信息熵计算完成")
        print(f"  熵值向量: {np.round(self.entropy, 4)}")

        return self.entropy

    def calculate_divergence(self) -> np.ndarray:
        """
        计算差异系数（冗余度）

        公式：d_j = 1 - e_j

        Returns:
            各指标的差异系数向量
        """
        if self.entropy is None:
            self.calculate_entropy()

        self.divergence = 1.0 - self.entropy

        print(f"✓ 差异系数计算完成")
        print(f"  差异系数向量: {np.round(self.divergence, 4)}")

        return self.divergence

    def calculate_weights(self) -> np.ndarray:
        """
        计算熵权

        公式：w_j = d_j / sum(d_j)

        Returns:
            熵权向量
        """
        if self.divergence is None:
            self.calculate_divergence()

        divergence_sum = np.sum(self.divergence)

        # 避免除以零
        if divergence_sum == 0:
            self.weights = np.ones(self.n_indicators) / self.n_indicators
        else:
            self.weights = self.divergence / divergence_sum

        print(f"✓ 熵权计算完成")
        print(f"  熵权向量: {np.round(self.weights, 4)}")

        return self.weights

    def get_weights(self) -> np.ndarray:
        """获取熵权"""
        if self.weights is None:
            self.calculate_weights()
        return self.weights