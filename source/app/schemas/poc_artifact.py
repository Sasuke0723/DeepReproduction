"""文件说明：PoC 阶段产物模型。

该模型用于表达“PoC 阶段产出了什么，以及执行结果如何”。
它连接了生成过程和执行过程，是验证阶段最直接的输入之一。
"""

from typing import List

from pydantic import BaseModel, Field


class PoCArtifact(BaseModel):
    """PoC 阶段标准输出。"""

    root_cause_analysis: str = Field(default="", description="漏洞根因分析")
    payload_generation_strategy: str = Field(default="", description="载荷构造策略")
    poc_filename: str = Field(..., description="PoC 主文件名")
    poc_content: str = Field(..., description="PoC 主文件内容")
    run_script_content: str = Field(..., description="运行脚本内容")
    input_files: List[str] = Field(default_factory=list, description="附属输入文件列表")
    expected_error_patterns: List[str] = Field(default_factory=list, description="预期错误模式")
    crash_report_content: str = Field(default="", description="崩溃报告内容")
    execution_success: bool = Field(default=False, description="PoC 执行是否成功")
    execution_logs: str = Field(default="", description="PoC 执行日志")
