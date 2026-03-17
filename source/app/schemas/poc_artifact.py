"""计划功能：定义 PoC 阶段产物结构，记录分析过程、复现代码、运行脚本、输入文件、崩溃报告与执行结果。"""
from pydantic import BaseModel, Field
from typing import List

class PoCArtifact(BaseModel):

    root_cause_analysis: str = Field(
        default="",
        description="漏洞根因分析，说明漏洞产生的原因"
    )

    payload_generation_strategy: str = Field(
        default="",
        description="Payload 生成策略，说明构造恶意输入的思路"
    )

    poc_filename: str

    poc_content: str

    run_script_content: str

    input_files: List[str] = Field(default_factory=list)

    expected_error_patterns: List[str] = Field(default_factory=list)
    
    crash_report_content: str = Field(
        default="",
        description="漏洞触发后的崩溃日志（如 ASan 报告），保存到独立文件"
    )

    execution_success: bool = False

    execution_logs: str = ""