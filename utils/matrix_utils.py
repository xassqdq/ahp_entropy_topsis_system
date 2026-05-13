"""
矩阵操作工具库
提供矩阵运算、验证、转换等基础功能
"""

import numpy as np
from typing import List, Tuple, Union
import logging

logger = logging.getLogger(__name__)


class MatrixUtils:
    """矩阵操作工具类"""

    @staticmethod
    def validate_reciprocal_matrix(matrix: np.ndarray, tolerance: float = 1e-10) -> Tuple[bool, str]:
        """
        验证矩阵是否为正互反矩阵

        Args:
            matrix: 待验证矩阵
            tolerance: 容差值

        Returns:
            (是否有效, 错误信息)
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        # 检查矩阵是否为方阵
        if matrix.shape[0] != matrix.shape[1]:
            return False, "矩阵必须是方阵"

        # 检查对角线元素是否为1
        for i in range(n):
            if abs(matrix[i, i] - 1.0) > tolerance:
                return False, f"对角线元素应为1，第({i},{i})位置为{matrix[i, i]}"

        # 检查互反性：aij * aji = 1
        for i in range(n):
            for j in range(i + 1, n):
                product = matrix[i, j] * matrix[j, i]
                if abs(product - 1.0) > tolerance:
                    return False, f"互反性检验失败：({i},{j})和({j},{i})位置的乘积为{product}，应为1"

        # 检查所有元素是否为正数
        if np.any(matrix <= 0):
            return False, "矩阵所有元素必须为正数"

        return True, "矩阵验证通过"

    @staticmethod
    def matrix_to_list(matrix: np.ndarray) -> List[List[float]]:
        """
        将numpy数组转换为列表

        Args:
            matrix: numpy数组

        Returns:
            列表形式的矩阵
        """
        return matrix.astype(float).tolist()

    @staticmethod
    def list_to_matrix(data: List[List[float]]) -> np.ndarray:
        """
        将列表转换为numpy数组

        Args:
            data: 列表形式的矩阵

        Returns:
            numpy数组
        """
        return np.array(data, dtype=float)

    @staticmethod
    def normalize_matrix_rows(matrix: np.ndarray) -> np.ndarray:
        """
        按行归一化矩阵（每行元素之和为1）

        Args:
            matrix: 输入矩阵

        Returns:
            行归一化后的矩阵
        """
        matrix = np.array(matrix, dtype=float)
        row_sums = matrix.sum(axis=1, keepdims=True)
        # 防止除以0
        row_sums[row_sums == 0] = 1
        return matrix / row_sums

    @staticmethod
    def normalize_matrix_cols(matrix: np.ndarray) -> np.ndarray:
        """
        按列归一化矩阵（每列元素之和为1）

        Args:
            matrix: 输入矩阵

        Returns:
            列归一化后的矩阵
        """
        matrix = np.array(matrix, dtype=float)
        col_sums = matrix.sum(axis=0, keepdims=True)
        # 防止除以0
        col_sums[col_sums == 0] = 1
        return matrix / col_sums

    @staticmethod
    def vector_normalize(matrix: np.ndarray) -> np.ndarray:
        """
        向量标准化（平方和开根号）
        用于TOPSIS算法

        Args:
            matrix: 输入矩阵

        Returns:
            向量标准化后的矩阵
        """
        matrix = np.array(matrix, dtype=float)
        # 计算每列的平方和
        col_sum_squares = np.sqrt((matrix ** 2).sum(axis=0))
        # 防止除以0
        col_sum_squares[col_sum_squares == 0] = 1
        return matrix / col_sum_squares

    @staticmethod
    def minmax_normalize(matrix: np.ndarray) -> np.ndarray:
        """
        极差标准化（最小-最大标准化）
        将数据映射到[0, 1]区间
        用于熵权法

        Args:
            matrix: 输入矩阵

        Returns:
            极差标准化后的矩阵
        """
        matrix = np.array(matrix, dtype=float)
        col_min = matrix.min(axis=0)
        col_max = matrix.max(axis=0)
        col_range = col_max - col_min

        # 防止除以0（当某列所有值相同时）
        col_range[col_range == 0] = 1

        return (matrix - col_min) / col_range

    @staticmethod
    def zscore_normalize(matrix: np.ndarray) -> np.ndarray:
        """
        Z-score标准化

        Args:
            matrix: 输入矩阵

        Returns:
            Z-score标准化后的矩阵
        """
        matrix = np.array(matrix, dtype=float)
        col_mean = matrix.mean(axis=0)
        col_std = matrix.std(axis=0)

        # 防止除以0
        col_std[col_std == 0] = 1

        return (matrix - col_mean) / col_std

    @staticmethod
    def calculate_eigenvalues_eigenvectors(matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算矩阵的特征值和特征向量

        Args:
            matrix: 输入矩阵

        Returns:
            (特征值, 特征向量)
        """
        matrix = np.array(matrix, dtype=float)
        eigenvalues, eigenvectors = np.linalg.eig(matrix)

        # 按特征值从大到小排序
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        return eigenvalues, eigenvectors

    @staticmethod
    def get_max_eigenvalue(matrix: np.ndarray) -> float:
        """
        获取矩阵的最大特征值

        Args:
            matrix: 输入矩阵

        Returns:
            最大特征值
        """
        eigenvalues, _ = MatrixUtils.calculate_eigenvalues_eigenvectors(matrix)
        return float(np.real(eigenvalues[0]))

    @staticmethod
    def get_principal_eigenvector(matrix: np.ndarray) -> np.ndarray:
        """
        获取对应最大特征值的特征向量（主特征向量）

        Args:
            matrix: 输入矩阵

        Returns:
            主特征向量（已归一化）
        """
        eigenvalues, eigenvectors = MatrixUtils.calculate_eigenvalues_eigenvectors(matrix)
        principal_eigenvector = np.real(eigenvectors[:, 0])

        # 归一化
        principal_eigenvector = principal_eigenvector / principal_eigenvector.sum()

        return principal_eigenvector

    @staticmethod
    def geometric_mean_method(matrix: np.ndarray) -> np.ndarray:
        """
        几何平均法计算权重

        Args:
            matrix: 判断矩阵

        Returns:
            权重向量
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        # 计算每行的几何平均数
        weights = np.zeros(n)
        for i in range(n):
            weights[i] = np.prod(matrix[i, :]) ** (1 / n)

        # 归一化
        weights = weights / weights.sum()

        return weights

    @staticmethod
    def arithmetic_mean_method(matrix: np.ndarray) -> np.ndarray:
        """
        算术平均法计算权重

        Args:
            matrix: 判断矩阵

        Returns:
            权重向量
        """
        matrix = np.array(matrix, dtype=float)

        # 列归一化
        normalized = MatrixUtils.normalize_matrix_cols(matrix)

        # 计算每行的平均值
        weights = normalized.mean(axis=1)

        return weights

    @staticmethod
    def power_method(matrix: np.ndarray, max_iterations: int = 100, tolerance: float = 1e-10) -> np.ndarray:
        """
        幂法计算主特征向量

        Args:
            matrix: 输入矩阵
            max_iterations: 最大迭代次数
            tolerance: 收敛容差

        Returns:
            主特征向量（已归一化）
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        # 初始向量
        x = np.ones(n) / n

        for _ in range(max_iterations):
            x_new = matrix @ x
            x_new = x_new / np.linalg.norm(x_new)

            # 检查收敛
            if np.linalg.norm(x_new - x) < tolerance:
                break

            x = x_new

        # 归一化
        x = x / x.sum()

        return x

    @staticmethod
    def matrix_multiply(matrix_a: np.ndarray, matrix_b: np.ndarray) -> np.ndarray:
        """
        矩阵乘法

        Args:
            matrix_a: 矩阵A
            matrix_b: 矩阵B

        Returns:
            A × B的结果
        """
        return np.dot(np.array(matrix_a, dtype=float), np.array(matrix_b, dtype=float))

    @staticmethod
    def matrix_inverse(matrix: np.ndarray) -> np.ndarray:
        """
        矩阵求逆

        Args:
            matrix: 输入矩阵

        Returns:
            逆矩阵
        """
        return np.linalg.inv(np.array(matrix, dtype=float))

    @staticmethod
    def matrix_transpose(matrix: np.ndarray) -> np.ndarray:
        """
        矩阵转置

        Args:
            matrix: 输入矩阵

        Returns:
            转置矩阵
        """
        return np.array(matrix, dtype=float).T

    @staticmethod
    def matrix_determinant(matrix: np.ndarray) -> float:
        """
        计算矩阵行列式

        Args:
            matrix: 输入矩阵

        Returns:
            行列式值
        """
        return float(np.linalg.det(np.array(matrix, dtype=float)))

    @staticmethod
    def matrix_rank(matrix: np.ndarray) -> int:
        """
        计算矩阵秩

        Args:
            matrix: 输入矩阵

        Returns:
            矩阵秩
        """
        return int(np.linalg.matrix_rank(np.array(matrix, dtype=float)))

    @staticmethod
    def matrix_trace(matrix: np.ndarray) -> float:
        """
        计算矩阵迹（对角线元素之和）

        Args:
            matrix: 输入矩阵

        Returns:
            矩阵迹
        """
        return float(np.trace(np.array(matrix, dtype=float)))

    @staticmethod
    def euclidean_distance(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        """
        计算两个向量的欧氏距离

        Args:
            vector_a: 向量A
            vector_b: 向量B

        Returns:
            欧氏距离
        """
        return float(np.linalg.norm(np.array(vector_a) - np.array(vector_b)))

    @staticmethod
    def manhattan_distance(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        """
        计算两个向量的曼哈顿距离

        Args:
            vector_a: 向量A
            vector_b: 向量B

        Returns:
            曼哈顿距离
        """
        return float(np.sum(np.abs(np.array(vector_a) - np.array(vector_b))))

    @staticmethod
    def cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        """
        计算两个向量的余弦相似度

        Args:
            vector_a: 向量A
            vector_b: 向量B

        Returns:
            余弦相似度（-1到1之间）
        """
        a = np.array(vector_a, dtype=float)
        b = np.array(vector_b, dtype=float)

        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(dot_product / (norm_a * norm_b))

    @staticmethod
    def correlation_matrix(data_matrix: np.ndarray) -> np.ndarray:
        """
        计算数据矩阵的相关系数矩阵

        Args:
            data_matrix: 数据矩阵（行=样本，列=特征）

        Returns:
            相关系数矩阵
        """
        return np.corrcoef(np.array(data_matrix, dtype=float).T)

    @staticmethod
    def covariance_matrix(data_matrix: np.ndarray) -> np.ndarray:
        """
        计算数据矩阵的协方差矩阵

        Args:
            data_matrix: 数据矩阵（行=样本，列=特征）

        Returns:
            协方差矩阵
        """
        return np.cov(np.array(data_matrix, dtype=float).T)

    @staticmethod
    def print_matrix(matrix: np.ndarray, name: str = "Matrix", precision: int = 4):
        """
        打印矩阵

        Args:
            matrix: 输入矩阵
            name: 矩阵名称
            precision: 小数精度
        """
        matrix = np.array(matrix, dtype=float)
        print(f"\n{name}:")
        print(f"Shape: {matrix.shape}")
        np.set_printoptions(precision=precision, suppress=True)
        print(matrix)