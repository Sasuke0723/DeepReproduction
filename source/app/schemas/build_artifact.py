"""文件说明：构建阶段产物模型。

该模型用于表达“环境构建阶段最终产生了什么”。
它既包含静态产物，例如 Dockerfile 和构建脚本，
也包含动态结果，例如构建是否成功、日志输出和预期二进制位置。
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class BuildArtifact(BaseModel):
    """构建阶段标准输出。"""

    dockerfile_content: str = Field(..., description="生成的 Dockerfile 内容")
    build_script_content: str = Field(..., description="生成的构建脚本内容")
    install_packages: List[str] = Field(default_factory=list, description="需要安装的依赖")
    build_commands: List[str] = Field(default_factory=list, description="核心构建命令")
    expected_binary_path: Optional[str] = Field(default=None, description="预期产物路径")
    sanitizer_enabled: bool = Field(default=False, description="是否启用 sanitizer")
    build_success: bool = Field(default=False, description="构建是否成功")
    build_logs: str = Field(default="", description="构建日志")
