"""文件说明：PoC 生成与执行阶段骨架。

这个模块负责“把漏洞知识和构建结果转成最小复现载荷，并执行它”。
它的职责边界是：
- 生成 PoC 方案
- 组织 PoC 文件与运行脚本
- 执行 PoC
- 收集执行输出和崩溃信息
"""

from app.schemas.build_artifact import BuildArtifact
from app.schemas.knowledge import KnowledgeModel
from app.schemas.poc_artifact import PoCArtifact


class PocStage:
    """PoC 阶段协调器。"""

    def build_plan(self, knowledge: KnowledgeModel, build: BuildArtifact, workspace: str) -> dict:
        """生成 PoC 阶段计划。"""

        raise NotImplementedError

    def render_prompt(self, knowledge: KnowledgeModel, build: BuildArtifact, plan: dict) -> str:
        """生成 PoC 阶段提示词。"""

        raise NotImplementedError

    def run(self, knowledge: KnowledgeModel, build: BuildArtifact, workspace: str) -> PoCArtifact:
        """执行 PoC 阶段并返回 PoC 产物。"""

        raise NotImplementedError


def poc_node(state):
    """LangGraph 节点：执行 PoC 生成与执行阶段。"""

    knowledge = state["knowledge"]
    build = state["build"]
    workspace = state["workspace"]
    retry_count = dict(state.get("retry_count", {}))
    history = list(state.get("stage_history", []))
    stage = PocStage()

    try:
        poc = stage.run(knowledge=knowledge, build=build, workspace=workspace)
        history.append({"stage": "poc", "status": "success"})
        return {
            "poc": poc,
            "current_stage": "verify",
            "stage_history": history,
            "last_error": None,
        }
    except Exception as error:
        retry_count["poc"] = retry_count.get("poc", 0) + 1
        history.append({"stage": "poc", "status": "failed", "error": str(error)})
        return {
            "retry_count": retry_count,
            "stage_history": history,
            "last_error": str(error),
        }
