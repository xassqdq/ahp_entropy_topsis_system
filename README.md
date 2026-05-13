# AHP + 熵权法 + TOPSIS 完整自动化工作流

**Mathematical Modeling Competition Standard Implementation**

一套严格按照数学建模竞赛规范设计的完整自动化工作流脚本，集成层次分析法(AHP)、熵权法、TOPSIS三大算法，支持一键运行、自动化处理、论文级输出。

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)

---

## 📋 目录

- [功能特性](#功能特性)
- [系统要求](#系统要求)
- [快速安装](#快速安装)
- [快速开始](#快速开始)
- [详细使用](#详细使用)
- [文件格式](#文件格式)
- [运行模式](#运行模式)
- [输出说明](#输出说明)
- [常见问题](#常见问题)
- [竞赛应用指南](#竞赛应用指南)
- [项目结构](#项目结构)

---

## ✨ 功能特性

### 核心算法
- ✅ **AHP (层次分析法)** - 特征向量法权重计算 + CR一致性检验
- ✅ **熵权法** - 基于信息熵的客观权重计算
- ✅ **TOPSIS** - 逼近理想解排序法
- ✅ **权重组合** - 乘法归一化(短板惩罚) + 线性加权

### 自动化处理
- ✅ 缺失值自动均值填充
- ✅ 指标同趋化自动处理
  - 成本型指标自动取倒数转换
  - 适度型指标自动转为正向指标
- ✅ 双轨标准化系统
  - 向量归一化(用于AHP+TOPSIS)
  - 极差标准化(用于熵权法)

### 竞赛规范
- ✅ 一致性检验不通过时仅警告，不自动修正
- ✅ 详细的一致性指标输出(λmax, CI, RI, CR)
- ✅ 人工优化建议提示
- ✅ 完整的中英文注释

### 输出功能
- ✅ 结构化结果表格(CSV格式)
- ✅ 权重汇总表
- ✅ 可视化图表(权重分布、排名柱状图、雷达图)
- ✅ LaTeX三线表代码(可直接插入论文)
- ✅ 一致性检验详细报告

### 灵活的运行模式
- ✅ **full模式** - 完整工作流(AHP + 熵权 + TOPSIS)
- ✅ **fast模式** - 快速模式(熵权 + TOPSIS，纯数据驱动)
- ✅ **expert模式** - 专家模式(仅AHP权重排序)

---

## 🖥️ 系统要求

### Python版本
- Python 3.8 或更高版本

### 依赖包
- numpy>=1.19.0
- pandas>=1.1.0
- matplotlib>=3.3.0
- scipy>=1.5.0


---

## 📦 快速安装

### 方法1：使用pip安装依赖

```bash
# 克隆或下载项目
git clone https://github.com/xassqdq/ahp_entropy_topsis_system.git
cd ahp-entropy-topsis

# 安装依赖
pip install -r requirements.txt

```
### 方法2：手动安装依赖
```bash
pip install numpy pandas matplotlib scipy
```
### 验证安装
```bash
python -c "import numpy, pandas, matplotlib; print('✓ 依赖安装成功')"
```

## 🚀 快速开始
### 最简单的使用方式
#### 1. 准备数据文件

- 在 data/ 文件夹中放置：

-  **data.csv** - 原始评价矩阵

- **ahp_matrix.json** - AHP判断矩阵(可选)

- **indicators.json** - 指标配置(可选)


#### 2. 运行脚本
```bash
# 完整模式(推荐用于竞赛)
python main.py --mode full --data data/data.csv --ahp data/ahp_matrix.json

# 快速模式(仅有数据)
python main.py --mode fast --data data/data.csv

# 专家模式(仅有AHP判断矩阵)
python main.py --mode expert --ahp data/ahp_matrix.json
```

#### 3. 查看结果

- 所有结果自动保存到 results/ 文件夹：
```aiignore
results/
├── results_summary.csv          # 排序结果表
├── weights_table.csv            # 权重汇总表
├── ahp_consistency.txt          # 一致性检验结果
├── latex_tables.txt             # LaTeX代码
└── figures/
    ├── weights_distribution.png # 权重分布图
    ├── topsis_ranking.png       # 排名柱状图
    └── radar_chart.png          # 雷达图
```

## 📖 详细使用
### 命令行参数
```bash
python main.py [OPTIONS]
```

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| --mode | 运行模式 (full/fast/expert) | full | --mode fast |
| --data | 原始数据CSV路径 | data/data.csv | --data mydata.csv |
| --indicators | 指标配置JSON路径 | data/indicators.json | --indicators config.json |
| --ahp | AHP判断矩阵JSON路径 | data/ahp_matrix.json | --ahp matrix.json |
| --output | 结果输出目录 | results | --output my_results |
| --combination | 权重组合方法 | multiplicative | --combination linear |
| --alpha | 线性组合系数(0~1) | 0.5 | --alpha 0.6 |

### 常用命令示例
```bash
# 示例1: 完整模式，默认参数
python main.py --mode full --data data/data.csv --ahp data/ahp_matrix.json

# 示例2: 快速模式，自定义输出目录
python main.py --mode fast --data data/data.csv --output my_results

# 示例3: 完整模式，使用线性组合权重(AHP权重占60%)
python main.py --mode full \
    --data data/data.csv \
    --ahp data/ahp_matrix.json \
    --combination linear \
    --alpha 0.6

# 示例4: 专家模式，仅计算AHP权重
python main.py --mode expert --ahp data/ahp_matrix.json --output ahp_results

# 示例5: 完整模式，自定义指标配置
python main.py --mode full \
    --data data/data.csv \
    --ahp data/ahp_matrix.json \
    --indicators my_indicators.json
```

## 📄 文件格式
### 1. 原始数据矩阵 (data.csv)
格式: 行=评价对象，列=评价指标

```csv
,指标1,指标2,指标3,指标4
方案A,85,92,78,88
方案B,90,85,82,91
方案C,78,88,95,85
方案D,92,80,88,89
```
说明：
- 第一列为对象名称（自动作为索引）
- 支持缺失值(NaN)，脚本自动均值填充
- 所有数据必须为数值类型

### 2. 指标配置文件 (indicators.json)
格式: 指标类型配置
```json
{
  "指标1": {
    "type": "benefit"
  },
  "指标2": {
    "type": "cost"
  },
  "指标3": {
    "type": "moderate",
    "ideal_value": 50
  },
  "指标4": {
    "type": "benefit"
  }
}
```
指标类型说明：
- benefit - 效益型(越大越好)，保持不变
- cost - 成本型(越小越好)，自动取倒数转换
- moderate - 适度型(有最优值)，自动转为正向指标

如果不提供此文件：脚本默认所有指标为效益型

### 3. AHP判断矩阵 (ahp_matrix.json)
格式: n×n的判断矩阵
```json
[
  [1, 2, 3, 4],
  [0.5, 1, 2, 3],
  [0.333, 0.5, 1, 2],
  [0.25, 0.333, 0.5, 1]
]
```
说明：
- 必须是方阵(n×n)
- 必须满足倒数关系: \(a_{ij} \times a_{ji} = 1\)
- 对角线元素必须为1

**1-9标度法：**
- 1：同等重要
- 3：一方略重要
- 5：一方明显重要
- 7：一方强烈重要
- 9：一方极端重要
- 2,4,6,8：中间值


快速生成AHP判断矩阵
```python
from utils.ahp_builder import build_ahp_matrix

comparisons = {
    (0, 1): 2,
    (0, 2): 3,
    (1, 2): 1.5
}

matrix = build_ahp_matrix(4, comparisons)
```

# 🎯 运行模式
## 模式1: full (完整模式) ⭐ 推荐用于竞赛
适用场景: 有数据 + 有专家判断

输入：
- ✅ data.csv
- ✅ ahp_matrix.json
- ⚠️ indicators.json（可选）

流程：
数据加载 → 指标同趋化 → 标准化处理 
→ AHP权重计算 + 一致性检验 
→ 熵权法权重计算 
→ 权重组合赋权(乘法归一化) 
→ TOPSIS排序 
→ 输出

命令：
```bash
python main.py --mode full --data data/data.csv --ahp data/ahp_matrix.json
```

## 模式2: fast (快速模式)
适用场景: 只有数据

输入：
- ✅ data.csv

流程：
数据加载 → 指标同趋化 → 标准化 
→ 熵权法 → TOPSIS

命令：
```bash
python main.py --mode fast --data data/data.csv
```
## 模式3: expert (专家模式)
适用场景: 无数据，仅专家判断

输入：
- ✅ ahp_matrix.json

命令：
```bash
python main.py --mode expert --ahp data/ahp_matrix.json
```


# 📊 输出说明
## 1. 排序结果表 (results_summary.csv)
```csv
Rank,Object,Closeness Degree,Score
1,方案B,0.654321,65.43
2,方案A,0.612345,61.23
3,方案D,0.587654,58.77
4,方案C,0.523456,52.35
```
## 2. 权重汇总表 (weights_table.csv)
```csv
Indicator,AHP Weight,Entropy Weight,Combined Weight
指标1,0.250000,0.280000,0.264575
指标2,0.350000,0.320000,0.335410
指标3,0.200000,0.240000,0.219089
指标4,0.200000,0.160000,0.180926
```
## 3. 一致性检验结果 (ahp_consistency.txt)
```txt
AHP Consistency Check Results
==================================================

lambda_max: 4.123456
ci: 0.041152
ri: 0.900000
cr: 0.045725
pass: True
 ```
# ❓ 常见问题
## Q1: 一致性未通过怎么办？
- 检查逻辑矛盾（如 A>B, B>C, 但 C>A）
- 调整判断矩阵
- 使用中间值（2,4,6,8）
- 保留原始矩阵并说明调整过程


## Q2: 缺失值处理
默认：
缺失值 → 均值填充

可修改：
`_handle_missing_values()`
## Q3: 指标类型处理
```json
{
  "成本指标": {"type": "cost"},
  "适度指标": {"type": "moderate", "ideal_value": 50}
}
```
## Q4: 权重组合方法
| 方法 | 公式 | 特点 |
| ---- | ---- | ---- |
| 乘法归一化 | $\sqrt{w_{ahp} \times w_{entropy}}$ | ⭐ 竞赛推荐 |
| 线性加权 | $\alpha \times w_{ahp} + (1-\alpha) \times w_{entropy}$ | 系数可调 |


## Q5: α参数
```bash
python main.py --mode full \
    --data data/data.csv \
    --ahp data/ahp_matrix.json \
    --combination linear \
    --alpha 0.6
```
# 论文结构
评价指标体系
→ 权重确定(AHP + 熵权)
→ 权重组合
→ TOPSIS排序
→ 结果分析
# 答辩要点
- 说明模式选择理由
- 解释AHP判断矩阵来源
- 强调一致性检验意义
- 分析AHP与熵权权重差异
- 解释最终方案排序合理性
# 项目结构
```aiignore
ahp_entropy_topsis_workflow/
│
├── main.py
├── config.py
├── data/
│   ├── data.csv
│   ├── indicators.json
│   └── ahp_matrix.json
│
├── modules/
│   ├── data_loader.py
│   ├── indicator_processor.py
│   ├── standardizer.py
│   ├── ahp_engine.py
│   ├── entropy_engine.py
│   ├── weight_combiner.py
│   ├── topsis_engine.py
│   └── visualizer.py
│
├── utils/
│   ├── matrix_utils.py
│   ├── consistency_checker.py
│   ├── latex_generator.py
│   └── ahp_builder.py
│
├── results/
```
