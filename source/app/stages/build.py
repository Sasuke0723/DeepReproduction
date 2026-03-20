"""文件说明：环境构建阶段骨架。

这个模块负责“把漏洞知识转成可执行的构建环境和构建结果”。
它不直接实现 Docker 或 Git 的底层动作，而是保留明确的阶段接口。

该阶段通常包含：
- 构建策略生成
- Dockerfile / build.sh 产物生成
- 版本切换与编译执行
- 构建日志整理
"""

from app.schemas.build_artifact import BuildArtifact
from app.schemas.knowledge import KnowledgeModel


class BuildStage:
    """构建阶段协调器。"""

    def build_plan(self, knowledge: KnowledgeModel, workspace: str) -> dict:
        """生成构建阶段计划。

        计划中通常包含：
        - 仓库和版本信息
        - 依赖安装策略
        - 编译入口
        - 预期产物位置
        """

        raise NotImplementedError

    def render_prompt(self, knowledge: KnowledgeModel, plan: dict) -> str:
        """生成构建阶段提示词。"""

        raise NotImplementedError

    def run(self, knowledge: KnowledgeModel, workspace: str) -> BuildArtifact:
        """执行构建阶段并返回构建产物。"""

        raise NotImplementedError


def build_node(state):
    """LangGraph 节点：执行环境构建阶段。"""

    knowledge = state["knowledge"]
    workspace = state["workspace"]
    retry_count = dict(state.get("retry_count", {}))
    history = list(state.get("stage_history", []))
    stage = BuildStage()

    try:
        build = stage.run(knowledge=knowledge, workspace=workspace)
        history.append({"stage": "build", "status": "success"})
        return {
            "build": build,
            "current_stage": "poc",
            "stage_history": history,
            "last_error": None,
        }
    except Exception as error:
        retry_count["build"] = retry_count.get("build", 0) + 1
        history.append({"stage": "build", "status": "failed", "error": str(error)})
        return {
            "retry_count": retry_count,
            "stage_history": history,
            "last_error": str(error),
        }
