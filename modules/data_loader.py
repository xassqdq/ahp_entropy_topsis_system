"""
数据读取与预处理模块
功能：读取CSV数据、缺失值处理、数据验证
"""

import pandas as pd
import numpy as np
import json
import os
from typing import Tuple, Dict, List

class DataLoader:
    """数据加载与预处理类"""

    def __init__(self, data_path: str, indicators_path: str = None):
        """
        初始化数据加载器

        Args:
            data_path: CSV数据文件路径
            indicators_path: 指标配置JSON文件路径
        """
        self.data_path = data_path
        self.indicators_path = indicators_path
        self.raw_data = None
        self.indicators_config = None
        self.objects = None
        self.indicators = None
        self.data_matrix = None

    def load_data(self) -> Tuple[np.ndarray, List[str], List[str]]:
        """
        加载原始数据矩阵

        Returns:
            data_matrix: 评价矩阵 (n_objects, n_indicators)
            objects: 评价对象名称列表
            indicators: 指标名称列表
        """
        # 读取CSV文件
        self.raw_data = pd.read_csv(self.data_path, index_col=0)
        self.objects = list(self.raw_data.index)
        self.indicators = list(self.raw_data.columns)

        print(f"✓ 数据加载成功")
        print(f"  评价对象数: {len(self.objects)}")
        print(f"  指标数: {len(self.indicators)}")
        print(f"  缺失值数: {self.raw_data.isnull().sum().sum()}")

        # 缺失值处理：均值填充
        self.raw_data = self._handle_missing_values()

        self.data_matrix = self.raw_data.values.astype(float)
        return self.data_matrix, self.objects, self.indicators

    def _handle_missing_values(self) -> pd.DataFrame:
        """
        缺失值处理：按列均值填充

        Returns:
            处理后的DataFrame
        """
        missing_count = self.raw_data.isnull().sum().sum()
        if missing_count > 0:
            print(f"⚠ 检测到 {missing_count} 个缺失值，执行均值填充...")
            self.raw_data = self.raw_data.fillna(self.raw_data.mean())
            print(f"✓ 缺失值处理完成")
        return self.raw_data

    def load_indicators_config(self) -> Dict:
        """
        加载指标配置文件

        Returns:
            指标配置字典
            格式: {
                'indicator_name': {
                    'type': 'benefit'|'cost'|'moderate',
                    'ideal_value': float (仅moderate类型需要)
                }
            }
        """
        if self.indicators_path and os.path.exists(self.indicators_path):
            with open(self.indicators_path, 'r', encoding='utf-8') as f:
                self.indicators_config = json.load(f)
            print(f"✓ 指标配置加载成功")
        else:
            # 默认配置：所有指标为效益型
            self.indicators_config = {
                ind: {'type': 'benefit'}
                for ind in self.indicators
            }
            print(f"⚠ 未找到指标配置文件，默认所有指标为效益型")

        return self.indicators_config

    def validate_data(self) -> bool:
        """
        数据有效性验证

        Returns:
            数据是否有效
        """
        # 检查数据维度
        if self.data_matrix is None:
            print("✗ 数据矩阵为空")
            return False

        if self.data_matrix.shape[0] < 2:
            print("✗ 评价对象数不足2个")
            return False

        if self.data_matrix.shape[1] < 2:
            print("✗ 指标数不足2个")
            return False

        # 检查数据类型
        if not np.issubdtype(self.data_matrix.dtype, np.number):
            print("✗ 数据包含非数值类型")
            return False

        # 检查是否存在无穷大或NaN
        if np.any(np.isnan(self.data_matrix)) or np.any(np.isinf(self.data_matrix)):
            print("✗ 数据包含NaN或无穷大")
            return False

        print("✓ 数据验证通过")
        return True

    def get_summary(self) -> Dict:
        """
        获取数据摘要统计

        Returns:
            统计信息字典
        """
        summary = {
            'n_objects': self.data_matrix.shape[0],
            'n_indicators': self.data_matrix.shape[1],
            'objects': self.objects,
            'indicators': self.indicators,
            'data_min': np.min(self.data_matrix),
            'data_max': np.max(self.data_matrix),
            'data_mean': np.mean(self.data_matrix),
            'data_std': np.std(self.data_matrix)
        }
        return summary