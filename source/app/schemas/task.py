"""文件说明：任务输入模型。

该模型描述一个漏洞复现任务在进入系统时必须具备的最小信息。
它属于“流程入口模型”，不关心中间产物，只描述任务本身。

设计原则：
- 尽量贴近原始任务数据
- 尽量稳定，不随阶段实现频繁变化
- 能覆盖仓库、版本、参考资料等基础输入
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    """单个漏洞复现任务的标准输入结构。"""

    task_id: str = Field(..., description="唯一任务标识")
    cve_id: str = Field(..., description="漏洞编号")
    cve_url: Optional[str] = Field(default=None, description="CVE 官方或聚合详情页")
    repo_url: Optional[str] = Field(default=None, description="漏洞对应源码仓库地址")
    vulnerable_ref: Optional[str] = Field(default=None, description="漏洞版本引用")
    fixed_ref: Optional[str] = Field(default=None, description="修复版本引用")
    language: Optional[str] = Field(default=None, description="目标项目主要语言")
    references: List[str] = Field(default_factory=list, description="补充参考链接列表")
