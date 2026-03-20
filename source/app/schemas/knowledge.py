"""文件说明：漏洞知识模型。

该模型是知识阶段的标准输出，也是后续 build / poc / verify 三个阶段的公共输入。
它的职责不是保存所有原始资料，而是保存“经过提炼后真正对复现有价值的信息”。
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class KnowledgeModel(BaseModel):
    """漏洞知识的结构化表达。"""

    cve_id: str = Field(..., description="漏洞编号")
    summary: str = Field(..., description="漏洞摘要")
    vulnerability_type: str = Field(..., description="漏洞类型")
    repo_url: Optional[str] = Field(default=None, description="源码仓库地址")
    vulnerable_ref: Optional[str] = Field(default=None, description="漏洞版本引用")
    fixed_ref: Optional[str] = Field(default=None, description="修复版本引用")
    affected_files: List[str] = Field(default_factory=list, description="可能受影响的文件")
    reproduction_hints: List[str] = Field(default_factory=list, description="复现提示信息")
    expected_error_patterns: List[str] = Field(default_factory=list, description="预期报错模式")
    expected_stack_keywords: List[str] = Field(default_factory=list, description="预期栈关键词")
    references: List[str] = Field(default_factory=list, description="知识阶段保留的参考资料")
