"""文件说明：流程共享状态定义。

`AppState` 是 LangGraph 在各阶段之间传递信息的唯一共享容器。
它描述的是“流程运行时需要知道什么”，而不是“某个阶段如何实现”。

状态内容分三类：
1. 固定输入：任务信息、工作区路径。
2. 阶段产物：knowledge、build、poc、verify。
3. 过程控制：当前阶段、重试计数、阶段历史、错误信息、最终状态。
"""

from typing import Dict, List, Optional, TypedDict

from app.schemas.build_artifact import BuildArtifact
from app.schemas.knowledge import KnowledgeModel
from app.schemas.poc_artifact import PoCArtifact
from app.schemas.task import TaskModel
from app.schemas.verify_result import VerifyResult


class AppState(TypedDict, total=False):
    """LangGraph 主流程共享状态。

    说明：
    - 这个结构只描述字段，不定义字段如何被更新。
    - 字段更新逻辑由各阶段节点负责。
    - 字段是否可为空，由流程当前所处阶段决定。
    """

    task: TaskModel
    workspace: str

    knowledge: KnowledgeModel
    build: BuildArtifact
    poc: PoCArtifact
    verify: VerifyResult

    current_stage: str
    retry_count: Dict[str, int]
    stage_history: List[dict]
    last_error: Optional[str]
    final_status: str
