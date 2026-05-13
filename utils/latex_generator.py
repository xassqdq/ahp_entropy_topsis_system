# ============================================================================
# LaTeX表格生成工具库
# 功能：用于生成竞赛论文可用的LaTeX三线表代码
# ============================================================================

"""
LaTeX表格生成工具库
用于生成竞赛论文可用的LaTeX三线表代码
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(name)


class LaTeXGenerator:
    """LaTeX表格生成工具类"""

    @staticmethod
    def escape_latex(text: str) -> str:
        """
        转义LaTeX特殊字符

        Args:
            text: 输入文本

        Returns:
            转义后的文本
        """
        special_chars = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
        }

        for char, escaped in special_chars.items():
            text = text.replace(char, escaped)

        return text

    @staticmethod
    def format_number(value: float, precision: int = 4) -> str:
        """
        格式化数字为LaTeX格式

        Args:
            value: 数值
            precision: 小数位数

        Returns:
            格式化后的字符串
        """
        if isinstance(value, (int, np.integer)):
            return str(value)

        format_str = f"{{:.{precision}f}}"
        return format_str.format(float(value))

    @staticmethod
    def generate_simple_table(headers: List[str],
                              data: List[List],
                              caption: str = "Table",
                              label: str = "tab:table",
                              precision: int = 4,
                              alignment: str = "c") -> str:
        """
        生成简单的LaTeX三线表

        Args:
            headers: 表头列表
            data: 数据列表（二维）
            caption: 表格标题
            label: 表格标签
            precision: 数字精度
            alignment: 列对齐方式 ('c'=居中, 'l'=左对齐, 'r'=右对齐)

        Returns:
            LaTeX表格代码
        """
        lines = []

        # 表格开始
        lines.append(r"\begin{table}[htbp]")
        lines.append(r"\centering")
        lines.append(f"\\caption{{{LaTeXGenerator.escape_latex(caption)}}}")

        # 列数
        num_cols = len(headers)
        col_format = alignment * num_cols

        # 表格环境
        lines.append(f"\\begin{{tabular}}{{{col_format}}}")
        lines.append(r"\toprule")

        # 表头
        header_row = " & ".join([LaTeXGenerator.escape_latex(str(h)) for h in headers])
        lines.append(f"{header_row} \\\\")
        lines.append(r"\midrule")

        # 数据行
        for row in data:
            formatted_row = []
            for cell in row:
                if isinstance(cell, (int, np.integer)):
                    formatted_row.append(str(cell))
                elif isinstance(cell, (float, np.floating)):
                    formatted_row.append(LaTeXGenerator.format_number(cell, precision))
                else:
                    formatted_row.append(LaTeXGenerator.escape_latex(str(cell)))

            lines.append(" & ".join(formatted_row) + " \\\\")

        lines.append(r"\bottomrule")
        lines.append(r"\end{tabular}")
        lines.append(f"\\label{{{label}}}")
        lines.append(r"\end{table}")

        return "\n".join(lines)

    @staticmethod
    def generate_weights_table(indicators: List[str],
                               ahp_weights: Optional[List[float]] = None,
                               entropy_weights: Optional[List[float]] = None,
                               combined_weights: Optional[List[float]] = None,
                               caption: str = "各指标权重汇总表",
                               precision: int = 4) -> str:
        """
        生成权重汇总表

        Args:
            indicators: 指标名称列表
            ahp_weights: AHP权重列表
            entropy_weights: 熵权权重列表
            combined_weights: 组合权重列表
            caption: 表格标题
            precision: 数字精度

        Returns:
            LaTeX表格代码
        """
        lines = []

        lines.append(r"\begin{table}[htbp]")
        lines.append(r"\centering")
        lines.append(f"\\caption{{{LaTeXGenerator.escape_latex(caption)}}}")

        # 确定列数
        headers = ["指标"]
        if ahp_weights is not None:
            headers.append("AHP权重")
        if entropy_weights is not None:
            headers.append("熵权权重")
        if combined_weights is not None:
            headers.append("组合权重")
            headers.append("占比(\%)")

        num_cols = len(headers)

        lines.append(f"\\begin{{tabular}}{{{'c' * num_cols}}}")
        lines.append(r"\toprule")

        # 表头
        header_row = " & ".join(headers)
        lines.append(f"{header_row} \\\\")
        lines.append(r"\midrule")

        # 数据行
        for i, indicator in enumerate(indicators):
            row = [LaTeXGenerator.escape_latex(str(indicator))]

            if ahp_weights is not None:
                row.append(LaTeXGenerator.format_number(ahp_weights[i], precision))

            if entropy_weights is not None:
                row.append(LaTeXGenerator.format_number(entropy_weights[i], precision))

            if combined_weights is not None:
                row.append(LaTeXGenerator.format_number(combined_weights[i], precision))
                percentage = combined_weights[i] * 100
                row.append(LaTeXGenerator.format_number(percentage, precision - 2) + "\%")

            lines.append(" & ".join(row) + " \\\\")

        lines.append(r"\bottomrule")
        lines.append(r"\end{tabular}")
        lines.append(r"\end{table}")

        return "\n".join(lines)

    @staticmethod
    def generate_topsis_ranking_table(objects: List[str],
                                      scores: List[float],
                                      rankings: Optional[List[int]] = None,
                                      evaluations: Optional[List[str]] = None,
                                      caption: str = "TOPSIS综合评价排名表",
                                      precision: int = 4) -> str:
        """
        生成TOPSIS排名表

        Args:
            objects: 评价对象名称列表
            scores: TOPSIS贴近度列表
            rankings: 排名列表（可选，若不提供则自动计算）
            evaluations: 定性评价列表（可选）
            caption: 表格标题
            precision: 数字精度

        Returns:
            LaTeX表格代码
        """
        # 自动计算排名
        if rankings is None:
            sorted_indices = np.argsort(scores)[::-1]
            rankings = [0] * len(scores)
            for rank, idx in enumerate(sorted_indices, 1):
                rankings[idx] = rank

        lines = []

        lines.append(r"\begin{table}[htbp]")
        lines.append(r"\centering")
        lines.append(f"\\caption{{{LaTeXGenerator.escape_latex(caption)}}}")

        # 确定列数
        headers = ["排名", "评价对象", "贴近度", "得分"]
        if evaluations is not None:
            headers.append("评价")

        num_cols = len(headers)

        lines.append(f"\\begin{{tabular}}{{{'c' * num_cols}}}")
        lines.append(r"\toprule")

        # 表头
        header_row = " & ".join(headers)
        lines.append(f"{header_row} \\\\")
        lines.append(r"\midrule")

        # 按排名排序
        sorted_indices = np.argsort(rankings)

        for idx in sorted_indices:
            rank = rankings[idx]
            obj_name = LaTeXGenerator.escape_latex(str(objects[idx]))
            score = scores[idx]
            score_100 = score * 100

            row = [
                str(rank),
                obj_name,
                LaTeXGenerator.format_number(score, precision),
                LaTeXGenerator.format_number(score_100, precision)
            ]

            if evaluations is not None:
                row.append(LaTeXGenerator.escape_latex(str(evaluations[idx])))

            lines.append(" & ".join(row) + " \\\\")

        lines.append(r"\bottomrule")
        lines.append(r"\end{tabular}")
        lines.append(r"\end{table}")

        return "\n".join(lines)

    @staticmethod
    def generate_consistency_table(matrix_order: int,
                                   max_eigenvalue: float,
                                   ci: float,
                                   ri: float,
                                   cr: float,
                                   passed: bool,
                                   caption: str = "AHP一致性检验结果表",
                                   precision: int = 6) -> str:
        """
        生成一致性检验结果表

        Args:
            matrix_order: 矩阵阶数
            max_eigenvalue: 最大特征值
            ci: 一致性指数
            ri: 随机一致性指数
            cr: 一致性比率
            passed: 是否通过检验
            caption: 表格标题
            precision: 数字精度

        Returns:
            LaTeX表格代码
        """
        lines = []

        lines.append(r"\begin{table}[htbp]")
        lines.append(r"\centering")
        lines.append(f"\\caption{{{LaTeXGenerator.escape_latex(caption)}}}")

        lines.append(r"\begin{tabular}{cc}")
        lines.append(r"\toprule")
        lines.append(r"指标 & 数值 \\")
        lines.append(r"\midrule")

        lines.append(f"矩阵阶数 & {matrix_order} \\\\")
        lines.append(
            f"最大特征值 $\\lambda_{{\\max}}$ & {LaTeXGenerator.format_number(max_eigenvalue, precision)} \\\\")
        lines.append(f"一致性指数 $CI$ & {LaTeXGenerator.format_number(ci, precision)} \\\\")
        lines.append(f"随机一致性指数 $RI$ & {LaTeXGenerator.format_number(ri, precision)} \\\\")
        lines.append(f"一致性比率 $CR$ & {LaTeXGenerator.format_number(cr, precision)} \\\\")

        status = "通过" if passed else "未通过"
        lines.append(f"检验结论 & {status} \\\\")

        lines.append(r"\bottomrule")
        lines.append(r"\end{tabular}")
        lines.append(r"\end{table}")

        return "\n".join(lines)

    @staticmethod
    def generate_standardized_matrix_table(matrix: np.ndarray,
                                           row_labels: Optional[List[str]] = None,
                                           col_labels: Optional[List[str]] = None,
                                           caption: str = "标准化矩阵",
                                           precision: int = 4) -> str:
        """
        生成标准化矩阵表

        Args:
            matrix: 矩阵数据
            row_labels: 行标签
            col_labels: 列标签
            caption: 表格标题
            precision: 数字精度

        Returns:
            LaTeX表格代码
        """
        matrix = np.array(matrix, dtype=float)
        m, n = matrix.shape

        lines = []

        lines.append(r"\begin{table}[htbp]")
        lines.append(r"\centering")
        lines.append(f"\\caption{{{LaTeXGenerator.escape_latex(caption)}}}")

        # 列格式
        if row_labels is not None:
            col_format = "c" + "c" * n
        else:
            col_format = "c" * n

        lines.append(f"\\begin{{tabular}}{{{col_format}}}")
        lines.append(r"\toprule")

        # 表头
        if col_labels is not None:
            header = ""
            if row_labels is not None:
                header = " & "
            header += " & ".join([LaTeXGenerator.escape_latex(str(label)) for label in col_labels])
            lines.append(header + " \\\\")
            lines.append(r"\midrule")

        # 数据行
        for i in range(m):
            row = []

            if row_labels is not None:
                row.append(LaTeXGenerator.escape_latex(str(row_labels[i])))

            for j in range(n):
                row.append(LaTeXGenerator.format_number(matrix[i, j], precision))

            lines.append(" & ".join(row) + " \\\\")

        lines.append(r"\bottomrule")
        lines.append(r"\end{tabular}")
        lines.append(r"\end{table}")

        return "\n".join(lines)

    @staticmethod
    def generate_comparison_matrix_table(matrix: np.ndarray,
                                         criteria: Optional[List[str]] = None,
                                         caption: str = "AHP判断矩阵",
                                         precision: int = 4) -> str:
        """
        生成AHP判断矩阵表

        Args:
            matrix: 判断矩阵
            criteria: 准则名称列表
            caption: 表格标题
            precision: 数字精度

        Returns:
            LaTeX表格代码
        """
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]

        lines = []

        lines.append(r"\begin{table}[htbp]")
        lines.append(r"\centering")
        lines.append(f"\\caption{{{LaTeXGenerator.escape_latex(caption)}}}")

        # 列格式
        col_format = "c" * (n + 1)

        lines.append(f"\\begin{{tabular}}{{{col_format}}}")
        lines.append(r"\toprule")

        # 表头
        header = "准则"
        if criteria is not None:
            header += " & " + " & ".join([LaTeXGenerator.escape_latex(str(c)) for c in criteria])
        else:
            header += " & " + " & ".join([f"$C_{i + 1}$" for i in range(n)])

        lines.append(header + " \\\\")
        lines.append(r"\midrule")

        # 数据行
        for i in range(n):
            row = []

            if criteria is not None:
                row.append(LaTeXGenerator.escape_latex(str(criteria[i])))
            else:
                row.append(f"$C_{i + 1}$")

            for j in range(n):
                value = matrix[i, j]
                if abs(value - round(value)) < 1e-10:
                    # 整数
                    row.append(str(int(round(value))))
                else:
                    # 分数形式
                    row.append(LaTeXGenerator.format_number(value, precision))

            lines.append(" & ".join(row) + " \\\\")

        lines.append(r"\bottomrule")
        lines.append(r"\end{tabular}")
        lines.append(r"\end{table}")

        return "\n".join(lines)

    @staticmethod
    def generate_document_header(title: str = "数学建模竞赛报告",
                                 author: str = "Team Name",
                                 date: str = r"\today") -> str:
        """
        生成LaTeX文档头

        Args:
            title: 文档标题
            author: 作者
            date: 日期

        Returns:
            LaTeX文档头代码
        """
        lines = []

        lines.append(r"\documentclass[12pt,a4paper]{article}")
        lines.append(r"\usepackage[utf-8]{inputenc}")
        lines.append(r"\usepackage[chinese]{babel}")
        lines.append(r"\usepackage{amsmath}")
        lines.append(r"\usepackage{amssymb}")
        lines.append(r"\usepackage{booktabs}")
        lines.append(r"\usepackage{graphicx}")
        lines.append(r"\usepackage{float}")
        lines.append(r"\usepackage{hyperref}")
        lines.append(r"\usepackage{geometry}")
        lines.append(r"\geometry{margin=1in}")
        lines.append("")
        lines.append(f"\\title{{{LaTeXGenerator.escape_latex(title)}}}")
        lines.append(f"\\author{{{LaTeXGenerator.escape_latex(author)}}}")
        lines.append(f"\\date{{{date}}}")
        lines.append("")
        lines.append(r"\begin{document}")
        lines.append(r"\maketitle")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def generate_document_footer() -> str:
        """
        生成LaTeX文档尾

        Returns:
            LaTeX文档尾代码
        """
        return r"\end{document}"

    @staticmethod
    def generate_section(title: str, content: str = "", level: int = 1) -> str:
        """
        生成LaTeX章节

        Args:
            title: 章节标题
            content: 章节内容
            level: 章节级别（1=section, 2=subsection, 3=subsubsection）

        Returns:
            LaTeX章节代码
        """
        section_commands = {
            1: r"\section",
            2: r"\subsection",
            3: r"\subsubsection"
        }

        command = section_commands.get(level, r"\section")

        lines = []
        lines.append(f"{command}{{{LaTeXGenerator.escape_latex(title)}}}")
        lines.append("")

        if content:
            lines.append(content)
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def generate_figure(image_path: str,
                        caption: str = "Figure",
                        label: str = "fig:figure",
                        width: str = "0.8\\textwidth") -> str:
        """
        生成LaTeX图片环境

        Args:
            image_path: 图片路径
            caption: 图片标题
            label: 图片标签
            width: 图片宽度

        Returns:
            LaTeX图片代码
        """
        lines = []

        lines.append(r"\begin{figure}[H]")
        lines.append(r"\centering")
        lines.append(f"\\includegraphics[width={width}]{{{image_path}}}")
        lines.append(f"\\caption{{{LaTeXGenerator.escape_latex(caption)}}}")
        lines.append(f"\\label{{{label}}}")
        lines.append(r"\end{figure}")

        return "\n".join(lines)

    @staticmethod
    def generate_equation(equation: str,
                          label: str = "eq:equation") -> str:
        """
        生成LaTeX公式环境

        Args:
            equation: 公式内容
            label: 公式标签

        Returns:
            LaTeX公式代码
        """
        lines = []

        lines.append(r"\begin{equation}")
        lines.append(equation)
        lines.append(f"\\label{{{label}}}")
        lines.append(r"\end{equation}")

        return "\n".join(lines)

    @staticmethod
    def generate_itemize(items: List[str]) -> str:
        """
        生成LaTeX列表

        Args:
            items: 列表项

        Returns:
            LaTeX列表代码
        """
        lines = []

        lines.append(r"\begin{itemize}")
        for item in items:
            lines.append(f"\\item {LaTeXGenerator.escape_latex(str(item))}")
        lines.append(r"\end{itemize}")

        return "\n".join(lines)

    @staticmethod
    def generate_enumerate(items: List[str]) -> str:
        """
        生成LaTeX编号列表

        Args:
            items: 列表项

        Returns:
            LaTeX编号列表代码
        """
        lines = []

        lines.append(r"\begin{enumerate}")
        for item in items:
            lines.append(f"\\item {LaTeXGenerator.escape_latex(str(item))}")
        lines.append(r"\end{enumerate}")

        return "\n".join(lines)

    @staticmethod
    def generate_complete_document(title: str,
                                   author: str,
                                   sections: Dict[str, str]) -> str:
        """
        生成完整的LaTeX文档

        Args:
            title: 文档标题
            author: 作者
            sections: 章节字典 {章节标题: 章节内容}

        Returns:
            完整的LaTeX文档代码
        """
        lines = []

        # 文档头
        lines.append(LaTeXGenerator.generate_document_header(title, author))

        # 章节
        for section_title, section_content in sections.items():
            lines.append(LaTeXGenerator.generate_section(section_title, section_content))

        # 文档尾
        lines.append(LaTeXGenerator.generate_document_footer())

        return "\n".join(lines)

    @staticmethod
    def save_latex_code(latex_code: str, output_path: str):
        """
        保存LaTeX代码到文件

        Args:
            latex_code: LaTeX代码
            output_path: 输出文件路径
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(latex_code)
            logger.info(f"LaTeX代码已保存到: {output_path}")
        except Exception as e:
            logger.error(f"保存LaTeX代码失败: {e}")

    @staticmethod
    def generate_summary_report(weights_table: str,
                                ranking_table: str,
                                consistency_table: Optional[str] = None) -> str:
        """
        生成综合总结报告

        Args:
            weights_table: 权重表LaTeX代码
            ranking_table: 排名表LaTeX代码
            consistency_table: 一致性检验表LaTeX代码（可选）

        Returns:
            综合报告LaTeX代码
        """
        lines = []

        lines.append(r"\section{结果汇总}")
        lines.append("")

        lines.append(r"\subsection{权重分析}")
        lines.append(weights_table)
        lines.append("")

        if consistency_table is not None:
            lines.append(r"\subsection{一致性检验}")
            lines.append(consistency_table)
            lines.append("")

        lines.append(r"\subsection{综合排名}")
        lines.append(ranking_table)
        lines.append("")

        return "\n".join(lines)