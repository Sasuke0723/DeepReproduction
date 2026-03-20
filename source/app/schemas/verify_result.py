"""文件说明：验证阶段结果模型。

该模型是整个主流程的最终判定输出。
它描述的不是“PoC 是否运行了”，而是“漏洞是否按预期被触发和修复”。
"""

from typing import List

from pydantic import BaseModel, Field


class VerifyResult(BaseModel):
    """验证阶段标准输出。"""

    pre_patch_triggered: bool = Field(..., description="补丁前是否成功触发漏洞")
    post_patch_clean: bool = Field(..., description="补丁后是否不再触发漏洞")
    matched_error_patterns: List[str] = Field(default_factory=list, description="命中的错误模式")
    matched_stack_keywords: List[str] = Field(default_factory=list, description="命中的栈关键词")
    verdict: str = Field(..., description="最终结论，例如 success 或 failed")
    reason: str = Field(..., description="最终结论说明")
