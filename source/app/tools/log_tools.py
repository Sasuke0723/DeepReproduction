"""文件说明：日志处理工具接口。

这个模块负责对构建日志、运行日志、崩溃报告做标准化处理，
为 PoC 阶段和验证阶段提供统一输入。

它应该输出结构化结果，而不是让上层阶段自行解析原始大文本。
"""

from typing import List

from pydantic import BaseModel, Field


class LogSummary(BaseModel):
    """日志摘要结果。"""

    matched_errors: List[str] = Field(default_factory=list, description="命中的错误模式")
    matched_keywords: List[str] = Field(default_factory=list, description="命中的关键词")
    excerpt: str = Field(default="", description="关键日志摘录")


class LogTool:
    """日志处理接口。"""

    def summarize(self, log_text: str) -> LogSummary:
        """生成日志摘要。"""

        raise NotImplementedError

    def extract_crash_report(self, log_text: str) -> str:
        """从完整日志中提取崩溃报告片段。"""

        raise NotImplementedError

    def match_patterns(self, log_text: str, patterns: List[str]) -> List[str]:
        """匹配预定义错误模式。"""

        raise NotImplementedError
