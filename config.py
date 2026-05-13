"""
全局配置管理模块
支持多模式切换、指标配置、算法参数统一管理
"""

import os
from pathlib import Path
from typing import Dict, List, Literal

# ============ 项目路径配置 ============
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
MODULES_DIR = PROJECT_ROOT / "modules"
UTILS_DIR = PROJECT_ROOT / "utils"

# 自动创建必要目录
for dir_path in [DATA_DIR, RESULTS_DIR, FIGURES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ============ 运行模式配置 ============
"""
mode 参数说明：
  'full'    - 完整模式：AHP + 熵权 + TOPSIS（需同时提供数据矩阵 + AHP判断矩阵）
  'fast'    - 快速模式：仅熵权 + TOPSIS（仅需原始数据，无需专家判断）
  'expert'  - 专家模式：仅AHP + TOPSIS（仅需AHP判断矩阵，适合小样本/定性指标）
"""
MODE: Literal['full', 'fast', 'expert'] = 'full'

# ============ 数据输入配置 ============
# 原始数据矩阵文件路径
DATA_FILE = DATA_DIR / "data.csv"

# 指标配置文件路径
INDICATORS_CONFIG_FILE = DATA_DIR / "indicators.json"

# AHP判断矩阵文件路径（mode='full' 或 'expert' 时需要）
AHP_MATRIX_FILE = DATA_DIR / "ahp_matrix.json"

# 缺失值处理策略
MISSING_VALUE_STRATEGY = 'mean'  # 'mean' | 'median' | 'forward_fill'

# ============ 指标配置示例（若无indicators.json则使用此配置） ============
DEFAULT_INDICATORS_CONFIG = {
    "indicators": [
        {
            "name": "指标1",
            "type": "benefit",  # benefit | cost | moderate
            "ideal_value": None  # moderate类型时需指定
        },
        {
            "name": "指标2",
            "type": "cost",
            "ideal_value": None
        },
        {
            "name": "指标3",
            "type": "moderate",
            "ideal_value": 50  # 适度型指标的最优值
        }
    ]
}

# ============ AHP算法参数 ============
class AHPConfig:
    # 一致性检验阈值
    CR_THRESHOLD = 0.1  # CR < 0.1 判定为通过

    # 随机一致性指数（RI）表
    RI_TABLE = {
        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
        6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
        11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59
    }

    # 判断矩阵标度定义（1-9标度法）
    SCALE_DEFINITION = {
        1: "同等重要",
        3: "弱重要",
        5: "明显重要",
        7: "强烈重要",
        9: "绝对重要",
        2: "介于1和3之间",
        4: "介于3和5之间",
        6: "介于5和7之间",
        8: "介于7和9之间"
    }

    # 特征向量计算方法
    EIGENVECTOR_METHOD = 'geometric_mean'  # 'geometric_mean' | 'arithmetic_mean' | 'power_method'

    # 一致性检验不通过时的处理策略
    CONSISTENCY_FAIL_STRATEGY = 'warn'  # 'warn' | 'auto_fix'（严禁自动修正，仅警告）

# ============ 熵权法算法参数 ============
class EntropyConfig:
    # 标准化方法（熵权法强制使用极差标准化）
    NORMALIZATION_METHOD = 'minmax'  # 极差标准化

    # 信息熵计算中的平滑参数（防止log(0)）
    EPSILON = 1e-10

    # 权重计算中的平滑参数
    WEIGHT_EPSILON = 1e-10

# ============ TOPSIS算法参数 ============
class TOPSISConfig:
    # 标准化方法（TOPSIS使用向量标准化）
    NORMALIZATION_METHOD = 'vector'  # 向量标准化

    # 距离计算方法
    DISTANCE_METRIC = 'euclidean'  # 'euclidean' | 'manhattan'

    # 贴近度计算中的平滑参数
    EPSILON = 1e-10

# ============ 权重组合配置 ============
class WeightCombinerConfig:
    # 组合赋权方法
    COMBINATION_METHOD = 'geometric'  # 'geometric' | 'linear'

    # 线性加权时的权重系数（仅当COMBINATION_METHOD='linear'时使用）
    ALPHA = 0.5  # α*AHP权重 + (1-α)*熵权权重

    # 组合权重中AHP和熵权的权重分配
    AHP_WEIGHT_RATIO = 0.5  # AHP权重占比
    ENTROPY_WEIGHT_RATIO = 0.5  # 熵权占比

# ============ 可视化配置 ============
class VisualizerConfig:
    # 图表风格
    STYLE = 'seaborn-v0_8-darkgrid'

    # 图表DPI（用于保存）
    DPI = 300

    # 图表尺寸
    FIGURE_SIZE = (12, 6)

    # 颜色方案
    COLOR_PALETTE = 'husl'

    # 字体配置
    FONT_SIZE = 12
    TITLE_SIZE = 14
    LABEL_SIZE = 11

    # 是否显示图表
    SHOW_PLOTS = False

    # 是否保存图表
    SAVE_PLOTS = True

# ============ 输出配置 ============
class OutputConfig:
    # 输出精度（小数位数）
    PRECISION = 4

    # 是否生成LaTeX表格代码
    GENERATE_LATEX = True

    # 是否生成详细报告
    GENERATE_REPORT = True

    # 输出文件编码
    ENCODING = 'utf-8-sig'  # 支持中文

    # 结果表格格式
    TABLE_FORMAT = 'csv'  # 'csv' | 'xlsx' | 'json'

# ============ 日志配置 ============
class LogConfig:
    # 日志级别
    LEVEL = 'INFO'  # 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR'

    # 日志文件路径
    LOG_FILE = RESULTS_DIR / "workflow.log"

    # 是否输出到控制台
    CONSOLE_OUTPUT = True

    # 是否输出到文件
    FILE_OUTPUT = True

# ============ 数据预处理配置 ============
class PreprocessConfig:
    # 是否自动检测并处理缺失值
    HANDLE_MISSING = True

    # 是否自动检测异常值
    DETECT_OUTLIERS = False

    # 异常值检测方法（仅当DETECT_OUTLIERS=True时使用）
    OUTLIER_METHOD = 'iqr'  # 'iqr' | 'zscore'

    # 异常值处理方法
    OUTLIER_STRATEGY = 'mean'  # 'mean' | 'median' | 'remove'

    # 是否进行数据标准化前的数据质量检查
    QUALITY_CHECK = True

# ============ 竞赛规范配置 ============
class CompetitionConfig:
    # 是否启用严格模式（符合竞赛评委审美）
    STRICT_MODE = True

    # 是否生成可答辩的详细过程文档
    GENERATE_DEFENSE_DOC = True

    # 是否生成论文可用的结果片段
    GENERATE_PAPER_SNIPPET = True

    # 论文语言
    PAPER_LANGUAGE = 'chinese'  # 'chinese' | 'english'

# ============ 全局参数汇总函数 ============
def get_config_summary() -> Dict:
    """获取当前配置摘要"""
    return {
        'mode': MODE,
        'data_file': str(DATA_FILE),
        'indicators_config': str(INDICATORS_CONFIG_FILE),
        'ahp_matrix_file': str(AHP_MATRIX_FILE),
        'results_dir': str(RESULTS_DIR),
        'cr_threshold': AHPConfig.CR_THRESHOLD,
        'combination_method': WeightCombinerConfig.COMBINATION_METHOD,
        'alpha': WeightCombinerConfig.ALPHA,
        'output_precision': OutputConfig.PRECISION,
        'strict_mode': CompetitionConfig.STRICT_MODE
    }

def print_config():
    """打印当前配置信息"""
    print("\n" + "="*60)
    print("【全局配置信息】")
    print("="*60)
    for key, value in get_config_summary().items():
        print(f"{key:.<30} {value}")
    print("="*60 + "\n")

if __name__ == '__main__':
    print_config()