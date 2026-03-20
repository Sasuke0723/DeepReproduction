"""文件说明：项目配置骨架。

这个文件用于集中声明项目级配置项，避免模型名称、路径、重试上限、
默认工作区策略等内容散落在不同模块中。

当前只保留配置结构，不写具体业务逻辑。后续可以继续拆成：
- 模型配置
- 路径配置
- 运行时配置
- 外部工具配置
"""

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """模型调用相关配置。"""

    provider: str = Field(default="openai", description="模型提供方标识")
    model_name: str = Field(default="gpt-4.1", description="默认使用的模型名称")


class RuntimeConfig(BaseModel):
    """流程运行相关配置。"""

    max_build_retry: int = Field(default=2, description="构建阶段最大重试次数")
    max_poc_retry: int = Field(default=2, description="PoC 阶段最大重试次数")
    workspace_root: str = Field(default="workspaces", description="工作区根目录")


class AppConfig(BaseModel):
    """项目总配置对象。

    统一作为应用启动时的配置入口，后续可以从 `.env`、YAML 或命令行注入。
    """

    model: ModelConfig = Field(default_factory=ModelConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
