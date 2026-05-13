"""
项目初始化与启动脚本
一键初始化项目结构、生成示例文件、启动完整工作流
"""

import json
import sys
from pathlib import Path
import logging
from datetime import datetime

# 导入配置
from config import (
    PROJECT_ROOT, DATA_DIR, RESULTS_DIR, FIGURES_DIR,
    MODE, DATA_FILE, INDICATORS_CONFIG_FILE, AHP_MATRIX_FILE,
    DEFAULT_INDICATORS_CONFIG, LogConfig, print_config
)


# ============ 日志配置 ============
def setup_logging():
    """配置日志系统"""
    log_file = LogConfig.LOG_FILE
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, LogConfig.LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ] if LogConfig.FILE_OUTPUT and LogConfig.CONSOLE_OUTPUT else
        [logging.FileHandler(log_file, encoding='utf-8')] if LogConfig.FILE_OUTPUT else
        [logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


# ============ 项目结构初始化 ============
def init_project_structure():
    """初始化项目目录结构"""
    logger.info("【初始化项目结构】")

    directories = [
        DATA_DIR,
        RESULTS_DIR,
        FIGURES_DIR,
        PROJECT_ROOT / "modules",
        PROJECT_ROOT / "utils"
    ]

    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ 创建目录: {dir_path}")

    logger.info("项目结构初始化完成\n")


# ============ 示例文件生成 ============
def generate_sample_data():
    """生成示例数据文件"""
    logger.info("【生成示例数据文件】")

    # 示例数据矩阵
    sample_data = """评价对象,指标1(效益型),指标2(成本型),指标3(适度型)
方案A,85,120,50
方案B,92,95,48
方案C,78,110,52
方案D,88,105,49
方案E,95,100,51"""

    data_file = DATA_DIR / "data_example.csv"
    data_file.write_text(sample_data, encoding='utf-8-sig')
    logger.info(f"✓ 生成示例数据: {data_file}")

    # 示例指标配置
    indicators_config = {
        "indicators": [
            {
                "name": "指标1",
                "type": "benefit",
                "description": "效益型指标，越大越好",
                "ideal_value": None
            },
            {
                "name": "指标2",
                "type": "cost",
                "description": "成本型指标，越小越好",
                "ideal_value": None
            },
            {
                "name": "指标3",
                "type": "moderate",
                "description": "适度型指标，接近最优值最好",
                "ideal_value": 50
            }
        ]
    }

    indicators_file = DATA_DIR / "indicators_example.json"
    indicators_file.write_text(
        json.dumps(indicators_config, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    logger.info(f"✓ 生成示例指标配置: {indicators_file}")

    # 示例AHP判断矩阵
    ahp_matrix = {
        "matrix": [
            [1, 2, 3],
            [0.5, 1, 2],
            [1 / 3, 0.5, 1]
        ],
        "criteria": ["指标1", "指标2", "指标3"],
        "description": "AHP判断矩阵示例（3×3）"
    }

    ahp_file = DATA_DIR / "ahp_matrix_example.json"
    ahp_file.write_text(
        json.dumps(ahp_matrix, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    logger.info(f"✓ 生成示例AHP判断矩阵: {ahp_file}")

    logger.info("示例文件生成完成\n")


# ============ 配置文件检查 ============
def check_required_files():
    """检查必要的输入文件"""
    logger.info("【检查输入文件】")

    if MODE == 'full':
        required_files = [DATA_FILE, AHP_MATRIX_FILE]
        file_names = ['数据矩阵', 'AHP判断矩阵']
    elif MODE == 'fast':
        required_files = [DATA_FILE]
        file_names = ['数据矩阵']
    elif MODE == 'expert':
        required_files = [AHP_MATRIX_FILE]
        file_names = ['AHP判断矩阵']
    else:
        logger.error(f"未知的运行模式: {MODE}")
        return False

    missing_files = []
    for file_path, file_name in zip(required_files, file_names):
        if file_path.exists():
            logger.info(f"✓ 找到 {file_name}: {file_path}")
        else:
            logger.warning(f"✗ 缺少 {file_name}: {file_path}")
            missing_files.append(file_name)

    if missing_files:
        logger.error(f"\n缺少必要文件: {', '.join(missing_files)}")
        logger.info(f"请参考 data/ 目录下的示例文件进行配置")
        return False

    logger.info("所有必要文件检查完成\n")
    return True


# ============ 配置验证 ============
def validate_config():
    """验证配置参数的合法性"""
    logger.info("【验证配置参数】")

    # 验证mode参数
    valid_modes = ['full', 'fast', 'expert']
    if MODE not in valid_modes:
        logger.error(f"无效的mode参数: {MODE}，应为 {valid_modes}")
        return False
    logger.info(f"✓ mode 参数有效: {MODE}")

    # 验证CR阈值
    from config import AHPConfig
    if not (0 < AHPConfig.CR_THRESHOLD < 1):
        logger.error(f"CR阈值应在0-1之间，当前值: {AHPConfig.CR_THRESHOLD}")
        return False
    logger.info(f"✓ CR阈值有效: {AHPConfig.CR_THRESHOLD}")

    # 验证权重组合参数
    from config import WeightCombinerConfig
    if WeightCombinerConfig.COMBINATION_METHOD not in ['geometric', 'linear']:
        logger.error(f"无效的权重组合方法: {WeightCombinerConfig.COMBINATION_METHOD}")
        return False
    logger.info(f"✓ 权重组合方法有效: {WeightCombinerConfig.COMBINATION_METHOD}")

    if not (0 <= WeightCombinerConfig.ALPHA <= 1):
        logger.error(f"线性加权系数α应在0-1之间，当前值: {WeightCombinerConfig.ALPHA}")
        return False
    logger.info(f"✓ 线性加权系数有效: {WeightCombinerConfig.ALPHA}")

    logger.info("配置参数验证完成\n")
    return True


# ============ 启动工作流 ============
def start_workflow():
    """启动完整工作流"""
    logger.info("=" * 70)
    logger.info("【AHP + 熵权法 + TOPSIS 自动化工作流】")
    logger.info("=" * 70)
    logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"运行模式: {MODE}")
    logger.info("=" * 70 + "\n")

    # 打印配置信息
    print_config()

    # 初始化项目结构
    init_project_structure()

    # 生成示例文件
    generate_sample_data()

    # 检查必要文件
    if not check_required_files():
        logger.error("\n【工作流启动失败】缺少必要的输入文件")
        return False

    # 验证配置
    if not validate_config():
        logger.error("\n【工作流启动失败】配置参数验证失败")
        return False

    logger.info("=" * 70)
    logger.info("【所有检查通过，准备启动主工作流】")
    logger.info("=" * 70 + "\n")

    # 导入并启动主程序
    try:
        from main import run_workflow
        logger.info("正在启动主工作流...\n")
        run_workflow()
        logger.info("\n" + "=" * 70)
        logger.info("【工作流执行完成】")
        logger.info(f"结果已保存至: {RESULTS_DIR}")
        logger.info("=" * 70)
        return True
    except ImportError as e:
        logger.error(f"无法导入主程序: {e}")
        logger.info("请确保 main.py 文件存在")
        return False
    except Exception as e:
        logger.error(f"工作流执行出错: {e}", exc_info=True)
        return False


# ============ 快速启动函数 ============
def quick_start():
    """快速启动（跳过初始化，直接运行）"""
    logger.info("【快速启动模式】")
    try:
        from main import run_workflow
        run_workflow()
        return True
    except Exception as e:
        logger.error(f"快速启动失败: {e}", exc_info=True)
        return False


# ============ 主入口 ============
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='AHP + 熵权法 + TOPSIS 自动化工作流启动脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python init_project.py                    # 完整初始化并启动
  python init_project.py --quick            # 快速启动（跳过初始化）
  python init_project.py --init-only        # 仅初始化，不启动工作流
  python init_project.py --check            # 仅检查配置和文件
        """
    )

    parser.add_argument(
        '--quick',
        action='store_true',
        help='快速启动模式（跳过初始化检查）'
    )
    parser.add_argument(
        '--init-only',
        action='store_true',
        help='仅执行初始化，不启动工作流'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='仅检查配置和文件，不启动工作流'
    )

    args = parser.parse_args()

    if args.quick:
        success = quick_start()
    elif args.init_only:
        init_project_structure()
        generate_sample_data()
        success = True
    elif args.check:
        init_project_structure()
        generate_sample_data()
        check_required_files()
        validate_config()
        success = True
    else:
        success = start_workflow()

    sys.exit(0 if success else 1)