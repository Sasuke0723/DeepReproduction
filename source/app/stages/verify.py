"""文件说明：结果验证阶段骨架。

这个模块负责“根据补丁前后结果判断漏洞是否成功复现、是否被修复”。
它是主流程的最终判定阶段，输出统一的验证结果模型。

验证方式后续可以有两类：
- 基于规则的匹配
- 基于模型的综合判断
"""

from app.schemas.knowledge import KnowledgeModel
from app.schemas.poc_artifact import PoCArtifact
from app.schemas.verify_result import VerifyResult


class VerifyStage:
    """验证阶段协调器。"""

    def build_context(self, knowledge: KnowledgeModel, poc: PoCArtifact, workspace: str) -> dict:
        """构造验证所需上下文，例如补丁前后日志、错误模式和比对信息。"""

        raise NotImplementedError

    def render_prompt(self, knowledge: KnowledgeModel, context: dict) -> str:
        """生成验证阶段提示词。"""

        raise NotImplementedError

    def run(self, knowledge: KnowledgeModel, poc: PoCArtifact, workspace: str) -> VerifyResult:
        """执行验证阶段并返回最终验证结果。"""

        raise NotImplementedError


def verify_node(state):
    """LangGraph 节点：执行验证阶段并回写最终流程状态。"""

    knowledge = state["knowledge"]
    poc = state["poc"]
    workspace = state["workspace"]
    stage = VerifyStage()

    verify = stage.run(knowledge=knowledge, poc=poc, workspace=workspace)

    history = list(state.get("stage_history", []))
    history.append({"stage": "verify", "status": verify.verdict})
    final_status = "success" if verify.verdict == "success" else "failed"

    return {
        "verify": verify,
        "final_status": final_status,
        "stage_history": history,
        "last_error": None if final_status == "success" else verify.reason,
    }
