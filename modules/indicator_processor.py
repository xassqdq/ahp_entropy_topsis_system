"""
指标同趋化处理模块
功能：成本型→效益型转换、适度型指标处理
"""

import numpy as np
from typing import Dict, Tuple, List


class IndicatorProcessor:
    """指标同趋化处理类"""

    def __init__(self, data_matrix: np.ndarray,
                 indicators: List[str],
                 indicators_config: Dict):
        """
        初始化指标处理器

        Args:
            data_matrix: 原始评价矩阵
            indicators: 指标名称列表
            indicators_config: 指标配置字典
        """
        self.data_matrix = data_matrix.copy()
        self.indicators = indicators
        self.indicators_config = indicators_config
        self.processed_matrix = None
        self.indicator_types = {}

    def process(self) -> np.ndarray:
        """
        执行指标同趋化处理

        Returns:
            处理后的矩阵（所有指标转为效益型）
        """
        self.processed_matrix = self.data_matrix.copy()

        print("\n【指标同趋化处理】")

        for idx, indicator in enumerate(self.indicators):
            config = self.indicators_config.get(
                indicator,
                {'type': 'benefit'}
            )
            ind_type = config.get('type', 'benefit')
            self.indicator_types[indicator] = ind_type

            if ind_type == 'cost':
                # 成本型：取倒数转换
                self.processed_matrix[:, idx] = self._cost_to_benefit(
                    self.processed_matrix[:, idx]
                )
                print(f"  ✓ {indicator}: 成本型 → 倒数转换")

            elif ind_type == 'moderate':
                # 适度型：转为正向指标
                ideal_value = config.get('ideal_value')
                if ideal_value is None:
                    raise ValueError(f"适度型指标 {indicator} 缺少 ideal_value 配置")

                self.processed_matrix[:, idx] = self._moderate_to_benefit(
                    self.processed_matrix[:, idx],
                    ideal_value
                )
                print(f"  ✓ {indicator}: 适度型 → 正向转换 (理想值={ideal_value})")

            else:
                # 效益型：保持不变
                print(f"  ✓ {indicator}: 效益型 (保持不变)")

        return self.processed_matrix

    @staticmethod
    def _cost_to_benefit(col: np.ndarray) -> np.ndarray:
        """
        成本型指标转效益型：取倒数

        Args:
            col: 指标列向量

        Returns:
            转换后的向量
        """
        # 避免除以零
        col = np.where(col == 0, 1e-10, col)
        return 1.0 / col

    @staticmethod
    def _moderate_to_benefit(col: np.ndarray, ideal_value: float) -> np.ndarray:
        """
        适度型指标转效益型：1 - |x - ideal| / max|xi - ideal|

        Args:
            col: 指标列向量
            ideal_value: 理想值

        Returns:
            转换后的向量
        """
        deviations = np.abs(col - ideal_value)
        max_deviation = np.max(deviations)

        if max_deviation == 0:
            return np.ones_like(col)

        return 1.0 - deviations / max_deviation

    def get_indicator_types(self) -> Dict[str, str]:
        """获取指标类型映射"""
        return self.indicator_types