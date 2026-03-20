"""文件说明：Docker 工具接口。

这个模块负责封装所有与容器构建和容器执行有关的动作，
供 build 阶段和 poc 阶段复用。

它只表达“需要哪些 Docker 能力”，不在这里绑定具体命令实现。
这样后续既可以接 Docker CLI，也可以接 SDK。
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DockerBuildRequest(BaseModel):
    """镜像构建请求。"""

    workspace: str = Field(..., description="构建上下文目录")
    dockerfile_path: str = Field(..., description="Dockerfile 路径")
    image_tag: str = Field(..., description="目标镜像标签")
    build_args: Dict[str, str] = Field(default_factory=dict, description="构建参数")


class DockerRunRequest(BaseModel):
    """容器运行请求。"""

    image_tag: str = Field(..., description="待运行镜像标签")
    command: List[str] = Field(default_factory=list, description="容器内执行命令")
    workspace: Optional[str] = Field(default=None, description="挂载工作区")
    environment: Dict[str, str] = Field(default_factory=dict, description="环境变量")


class DockerCommandResult(BaseModel):
    """Docker 命令执行结果。"""

    success: bool = Field(default=False, description="命令是否成功")
    exit_code: int = Field(default=1, description="进程退出码")
    stdout: str = Field(default="", description="标准输出")
    stderr: str = Field(default="", description="标准错误")


class DockerTool:
    """Docker 操作接口。"""

    def build_image(self, request: DockerBuildRequest) -> DockerCommandResult:
        """根据请求构建镜像。"""

        raise NotImplementedError

    def run_container(self, request: DockerRunRequest) -> DockerCommandResult:
        """运行容器并返回执行结果。"""

        raise NotImplementedError

    def remove_image(self, image_tag: str) -> None:
        """删除临时镜像。"""

        raise NotImplementedError
