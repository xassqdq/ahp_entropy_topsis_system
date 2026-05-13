"""
TOPSIS排序计算模块
功能：正负理想解确定、欧氏距离计算、相对贴近度求解
"""

import numpy as np
from typing import Tuple, Dict, List


class TOPSISEngine:
    """TOPSIS排序计算引擎"""

    def __init__(self, vector_normalized_matrix: np.ndarray,
                 weights: np.ndarray):
        """
        初始化TOPSIS引擎

        Args:
            vector_normalized_matrix: 向量标准化矩阵
            weights: 权重向量（组合权重）
        """
        self.normalized_matrix = vector_normalized_matrix.copy()
        self.weights = weights
        self.n_objects = vector_normalized_matrix.shape[0]
        self.n_indicators = vector_normalized_matrix.shape[1]

        self.weighted_matrix = None
        self.ideal_solution = None
        self.negative_ideal_solution = None
        self.distance_positive = None
        self.distance_negative = None
        self.closeness = None
        self.ranking = None

    def calculate_weighted_matrix(self) -> np.ndarray:
        """
        计算加权标准化矩阵

        公式：v_ij = w_j * x_ij

        Returns:
            加权标准化矩阵
        """
        print("\n【TOPSIS计算】")

        self.weighted_matrix = self.normalized_matrix * self.weights

        print(f"✓ 加权标准化矩阵计算完成")

        return self.weighted_matrix

    def determine_ideal_solutions(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        确定正负理想解

        正理想解：各指标最大值
        负理想解：各指标最小值

        Returns:
            (正理想解, 负理想解)
        """
        if self.weighted_matrix is None:
            self.calculate_weighted_matrix()

        # 正理想解：各列最大值
        self.ideal_solution = np.max(self.weighted_matrix, axis=0)

        # 负理想解：各列最小值
        self.negative_ideal_solution = np.min(self.weighted_matrix, axis=0)

        print(f"✓ 正负理想解确定完成")
        print(f"  正理想解: {np.round(self.ideal_solution, 4)}")
        print(f"  负理想解: {np.round(self.negative_ideal_solution, 4)}")

        return self.ideal_solution, self.negative_ideal_solution

    def calculate_distances(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算欧氏距离

        公式：
        D+ = sqrt(sum((v_ij - v_j+)^2))
        D- = sqrt(sum((v_ij - v_j-)^2))

        Returns:
            (到正理想解的距离, 到负理想解的距离)
        """
        if self.ideal_solution is None:
            self.determine_ideal_solutions()

        # 到正理想解的距离
        diff_positive = self.weighted_matrix - self.ideal_solution
        self.distance_positive = np.sqrt(
            np.sum(diff_positive ** 2, axis=1)
        )

        # 到负理想解的距离
        diff_negative = self.weighted_matrix - self.negative_ideal_solution
        self.distance_negative = np.sqrt(
            np.sum(diff_negative ** 2, axis=1)
        )

        print(f"✓ 欧氏距离计算完成")

        return self.distance_positive, self.distance_negative

    def calculate_closeness(self) -> np.ndarray:
        """
        计算相对贴近度

        公式：C_i = D_i- / (D_i+ + D_i-)

        Returns:
            相对贴近度向量
        """
        if self.distance_positive is None:
            self.calculate_distances()

        # 避免除以零
        denominator = self.distance_positive + self.distance_negative
        denominator = np.where(
            denominator == 0,
            1e-10,
            denominator
        )

        self.closeness = self.distance_negative / denominator

        print(f"✓ 相对贴近度计算完成")
        print(f"  贴近度向量: {np.round(self.closeness, 4)}")

        return self.closeness

    def get_ranking(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        获取排名

        Returns:
            (排名索引, 排名顺序的贴近度)
        """
        if self.closeness is None:
            self.calculate_closeness()

        # 按贴近度降序排序
        self.ranking = np.argsort(-self.closeness)

        print(f"✓ 排名计算完成")

        return self.ranking, self.closeness[self.ranking]

    def get_results_summary(self, objects: List[str]) -> Dict:
        """
        获取完整结果汇总

        Args:
            objects: 评价对象名称列表

        Returns:
            结果字典
        """
        if self.ranking is None:
            self.get_ranking()

        results = {
            'objects': objects,
            'closeness': self.closeness,
            'ranking': self.ranking,
            'ranked_objects': [objects[i] for i in self.ranking],
            'ranked_closeness': self.closeness[self.ranking],
            'distance_positive': self.distance_positive,
            'distance_negative': self.distance_negative
        }

        return results