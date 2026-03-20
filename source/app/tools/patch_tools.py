"""文件说明：补丁分析工具接口。

这个模块负责从 diff 或 patch 中提取出对漏洞复现有价值的信息，
例如受影响文件、关键修改位置、修复语义线索等。

它的主要消费者是 knowledge 阶段。
"""

from typing import List

from pydantic import BaseModel, Field


class PatchSummary(BaseModel):
    """补丁摘要结果。"""

    affected_files: List[str] = Field(default_factory=list, description="受影响文件列表")
    changed_functions: List[str] = Field(default_factory=list, description="涉及的函数或符号")
    summary: str = Field(default="", description="补丁语义摘要")


class PatchTool:
    """补丁分析接口。"""

    def parse_diff(self, diff_text: str) -> PatchSummary:
        """解析 diff 内容并输出结构化摘要。"""

        raise NotImplementedError

    def extract_hunks(self, diff_text: str) -> List[str]:
        """提取关键变更块。"""

        raise NotImplementedError
