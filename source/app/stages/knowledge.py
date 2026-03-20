"""文件说明：知识采集阶段骨架。

这个模块负责“把原始漏洞资料变成结构化知识”。
它同时包含两类内容：
1. 阶段执行入口 `knowledge_node`
2. 阶段内部协调器 `KnowledgeStage`

设计目标：
- 对外暴露统一的阶段入口
- 对内保留明确的处理步骤骨架
- 不在这里堆积底层工具实现细节
"""

from app.schemas.knowledge import KnowledgeModel
from app.schemas.task import TaskModel


class KnowledgeStage:
    """知识阶段协调器。

    负责串联以下子步骤：
    - 收集参考资料
    - 清洗网页和文档内容
    - 组织提示词输入
    - 调用模型生成结构化知识
    - 持久化阶段产物
    """

    def build_context(self, task: TaskModel, workspace: str) -> dict:
        """构造知识阶段执行上下文。"""

        raise NotImplementedError

    def render_prompt(self, task: TaskModel, context: dict) -> str:
        """根据任务和上下文生成知识提取提示词。"""

        raise NotImplementedError

    def run(self, task: TaskModel, workspace: str) -> KnowledgeModel:
        """执行知识采集阶段并返回结构化知识结果。"""

        raise NotImplementedError


def knowledge_node(state):
    """LangGraph 节点：执行知识采集阶段并回写状态。"""

    task = state["task"]
    workspace = state["workspace"]
    stage = KnowledgeStage()

    knowledge = stage.run(task=task, workspace=workspace)

    history = list(state.get("stage_history", []))
    history.append({"stage": "knowledge", "status": "success"})

    return {
        "knowledge": knowledge,
        "current_stage": "build",
        "stage_history": history,
        "last_error": None,
    }
