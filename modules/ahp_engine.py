"""
AHP权重计算与一致性检验模块
功能：特征向量法、CR一致性检验、判断矩阵构建
"""

import numpy as np
import json
import os
from typing import Dict, Tuple, Optional


class AHPEngine:
    """AHP权重计算引擎"""

    # 随机一致性指数表
    RI_TABLE = {
        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
        6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
        11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59
    }

    def __init__(self, n_indicators: int,
                 ahp_matrix_path: Optional[str] = None):
        """
        初始化AHP引擎

        Args:
            n_indicators: 指标数量
            ahp_matrix_path: AHP判断矩阵JSON文件路径
        """
        self.n = n_indicators
        self.ahp_matrix_path = ahp_matrix_path
        self.judgment_matrix = None
        self.weights = None
        self.cr = None
        self.ci = None
        self.ri = None
        self.consistency_pass = False

    def load_judgment_matrix(self) -> np.ndarray:
        """
        加载AHP判断矩阵

        Returns:
            判断矩阵
        """
        if self.ahp_matrix_path and os.path.exists(self.ahp_matrix_path):
            with open(self.ahp_matrix_path, 'r', encoding='utf-8') as f:
                matrix_list = json.load(f)
            self.judgment_matrix = np.array(matrix_list, dtype=float)
            print(f"✓ AHP判断矩阵加载成功 ({self.n}×{self.n})")
        else:
            print("⚠ 未找到AHP判断矩阵文件，使用默认单位矩阵")
            self.judgment_matrix = np.eye(self.n)

        return self.judgment_matrix

    def calculate_weights(self) -> np.ndarray:
        """
        特征向量法计算权重

        Returns:
            权重向量
        """
        print("\n【AHP权重计算】")

        if self.judgment_matrix is None:
            self.load_judgment_matrix()

        # 特征向量法：逐行相乘再开n次方
        row_products = np.prod(self.judgment_matrix, axis=1)

        # 避免负数开方
        row_products = np.abs(row_products)

        # 开n次方
        eigenvector = np.power(row_products, 1.0 / self.n)

        # 归一化
        self.weights = eigenvector / np.sum(eigenvector)

        print(f"✓ 特征向量法计算完成")
        print(f"  权重向量: {np.round(self.weights, 4)}")

        return self.weights

    def check_consistency(self) -> Tuple[float, bool, Dict]:
        """
        一致性检验（CR检验）

        Returns:
            (CR值, 是否通过, 详细信息字典)
        """
        print("\n【AHP一致性检验】")

        if self.weights is None:
            self.calculate_weights()

        # 计算加权和向量
        weighted_sum = np.dot(self.judgment_matrix, self.weights)

        # 计算λmax
        lambda_max = np.mean(weighted_sum / self.weights)

        # 计算CI
        self.ci = (lambda_max - self.n) / (self.n - 1)

        # 获取RI
        self.ri = self.RI_TABLE.get(self.n, 0)

        # 计算CR
        if self.ri == 0:
            self.cr = 0
        else:
            self.cr = self.ci / self.ri

        # 判断是否通过（CR < 0.1）
        self.consistency_pass = self.cr < 0.1

        status = "✓ 通过" if self.consistency_pass else "✗ 未通过"
        print(f"  λmax = {lambda_max:.6f}")
        print(f"  CI = {self.ci:.6f}")
        print(f"  RI = {self.ri:.6f}")
        print(f"  CR = {self.cr:.6f} {status}")

        if not self.consistency_pass:
            print(f"\n⚠ 一致性检验未通过 (CR={self.cr:.4f} > 0.1)")
            print(f"  建议：调整判断矩阵，使相邻元素比值更加一致")
            print(f"  或检查是否存在逻辑矛盾的比较关系")

        details = {
            'lambda_max': lambda_max,
            'ci': self.ci,
            'ri': self.ri,
            'cr': self.cr,
            'pass': self.consistency_pass
        }

        return self.cr, self.consistency_pass, details

    def get_weights(self) -> np.ndarray:
        """获取AHP权重"""
        if self.weights is None:
            self.calculate_weights()
        return self.weights