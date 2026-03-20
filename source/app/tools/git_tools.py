"""文件说明：Git 工具接口。

这个模块负责仓库获取、版本切换和补丁差异导出，
主要服务于 knowledge 阶段和 build 阶段。

设计上只保留框架真正需要的 Git 能力，避免把所有 Git 操作都堆进来。
"""

from pydantic import BaseModel, Field


class RepositorySnapshot(BaseModel):
    """仓库快照信息。"""

    repo_url: str = Field(..., description="仓库地址")
    local_path: str = Field(..., description="本地仓库路径")
    current_ref: str = Field(default="", description="当前版本引用")


class GitTool:
    """Git 操作接口。"""

    def clone_repo(self, repo_url: str, target_dir: str) -> RepositorySnapshot:
        """克隆仓库到指定目录。"""

        raise NotImplementedError

    def checkout_ref(self, repo_path: str, ref: str) -> RepositorySnapshot:
        """切换到指定 commit、tag 或分支。"""

        raise NotImplementedError

    def export_diff(self, repo_path: str, old_ref: str, new_ref: str) -> str:
        """导出两个版本之间的补丁差异。"""

        raise NotImplementedError
