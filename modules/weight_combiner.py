"""
权重组合赋权模块
功能：AHP权重与熵权组合、乘法归一化、线性加权
"""

import numpy as np
from typing import Tuple, Dict


class WeightCombiner:
    """权重组合赋权类"""

    def __init__(self, ahp_weights: np.ndarray = None,
                 entropy_weights: np.ndarray = None):
        """
        初始化权重组合器

        Args:
            ahp_weights: AHP权重向量
            entropy_weights: 熵权向量
        """
        self.ahp_weights = ahp_weights
        self.entropy_weights = entropy_weights
        self.combined_weights = None
        self.combination_method = None

    def combine_multiplicative(self) -> np.ndarray:
        """
        乘法归一化组合权重（默认方案）

        公式：w_j = sqrt(w_ahp_j * w_entropy_j) / sum(...)

        特点：短板惩罚，提升评价严谨性

        Returns:
            组合权重向量
        """
        if self.ahp_weights is None or self.entropy_weights is None:
            raise ValueError("AHP权重和熵权都不能为空")

        print("\n【权重组合赋权】")
        print("  方法：乘法归一化 (短板惩罚)")

        # 乘积
        product = self.ahp_weights * self.entropy_weights

        # 开平方
        geometric_mean = np.sqrt(product)

        # 归一化
        self.combined_weights = geometric_mean / np.sum(geometric_mean)

        self.combination_method = 'multiplicative'

        print(f"✓ 乘法组合权重计算完成")
        print(f"  组合权重: {np.round(self.combined_weights, 4)}")

        return self.combined_weights

    def combine_linear(self, alpha: float = 0.5) -> np.ndarray:
        """
        线性加权组合权重（备选方案）

        公式：w_j = α * w_ahp_j + (1-α) * w_entropy_j

        Args:
            alpha: AHP权重系数 (0~1)，默认0.5

        Returns:
            组合权重向量
        """
        if self.ahp_weights is None or self.entropy_weights is None:
            raise ValueError("AHP权重和熵权都不能为空")

        print("\n【权重组合赋权】")
        print(f"  方法：线性加权 (α={alpha})")

        self.combined_weights = (
                alpha * self.ahp_weights +
                (1 - alpha) * self.entropy_weights
        )

        self.combination_method = f'linear_α{alpha}'

        print(f"✓ 线性组合权重计算完成")
        print(f"  组合权重: {np.round(self.combined_weights, 4)}")

        return self.combined_weights

    def get_combined_weights(self) -> np.ndarray:
        """获取组合权重"""
        if self.combined_weights is None:
            self.combine_multiplicative()
        return self.combined_weights

    def get_weight_summary(self) -> Dict:
        """
        获取权重汇总信息

        Returns:
            权重对比字典
        """
        summary = {
            'ahp_weights': self.ahp_weights,
            'entropy_weights': self.entropy_weights,
            'combined_weights': self.combined_weights,
            'combination_method': self.combination_method
        }
        return summary