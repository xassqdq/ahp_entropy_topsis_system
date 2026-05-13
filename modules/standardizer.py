"""
标准化模块（双轨制）
功能：向量归一化（AHP+TOPSIS用）、极差标准化（熵权法用）
"""

import numpy as np
from typing import Tuple


class Standardizer:
    """标准化处理类"""

    def __init__(self, data_matrix: np.ndarray):
        """
        初始化标准化器

        Args:
            data_matrix: 处理后的评价矩阵（已同趋化）
        """
        self.data_matrix = data_matrix.copy()
        self.vector_normalized = None  # 向量归一化矩阵
        self.range_normalized = None  # 极差标准化矩阵

    def standardize_vector(self) -> np.ndarray:
        """
        向量归一化（平方和开根号）
        用于：AHP权重计算、TOPSIS计算

        公式：x_ij' = x_ij / sqrt(sum(x_ij^2))

        Returns:
            向量标准化矩阵
        """
        # 计算每列的平方和
        col_sum_squares = np.sum(self.data_matrix ** 2, axis=0)

        # 避免除以零
        col_sum_squares = np.where(
            col_sum_squares == 0,
            1e-10,
            col_sum_squares
        )

        # 向量归一化
        self.vector_normalized = self.data_matrix / np.sqrt(col_sum_squares)

        print("✓ 向量归一化完成 (用于AHP+TOPSIS)")
        return self.vector_normalized

    def standardize_range(self) -> np.ndarray:
        """
        极差标准化（映射到0~1区间）
        用于：熵权法计算

        公式：x_ij' = (x_ij - min_j) / (max_j - min_j)

        Returns:
            极差标准化矩阵
        """
        col_min = np.min(self.data_matrix, axis=0)
        col_max = np.max(self.data_matrix, axis=0)

        col_range = col_max - col_min

        # 避免除以零（指标无差异）
        col_range = np.where(col_range == 0, 1e-10, col_range)

        # 极差标准化
        self.range_normalized = (
                (self.data_matrix - col_min) / col_range
        )

        print("✓ 极差标准化完成 (用于熵权法)")
        return self.range_normalized

    def standardize_all(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        同时执行两种标准化

        Returns:
            (向量标准化矩阵, 极差标准化矩阵)
        """
        print("\n【标准化处理】")
        vector_norm = self.standardize_vector()
        range_norm = self.standardize_range()
        return vector_norm, range_norm