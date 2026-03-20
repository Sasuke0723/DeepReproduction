"""文件说明：项目主入口。

这个文件只负责三件事：
1. 从外部任务文件加载最小输入。
2. 组装 LangGraph 所需的初始状态。
3. 调用主流程图并返回最终结果。

这里不承载任何阶段实现细节，也不直接处理 Docker、Git、日志或模型调用。
它的目标是让调用链保持单一入口，便于后续接入 CLI、批处理或服务化接口。
"""

import yaml

from app.orchestrator.graph import build_app_graph
from app.schemas.task import TaskModel


def load_task(task_path: str) -> TaskModel:
    """加载任务文件并转换为统一任务模型。

    输入：
    - `task_path`：任务 YAML 文件路径。

    输出：
    - `TaskModel`：后续所有阶段共享的标准任务输入。
    """

    with open(task_path, "r", encoding="utf-8") as file:
        task_data = yaml.safe_load(file)

    return TaskModel(**task_data)


def build_initial_state(task: TaskModel) -> dict:
    """基于任务对象构造主流程初始状态。

    初始状态只包含流程启动所需的公共信息，不提前写入阶段产物。
    后续阶段产物由各阶段节点逐步回填。
    """

    return {
        "task": task,
        "workspace": f"workspaces/{task.task_id}",
        "retry_count": {},
        "stage_history": [],
        "current_stage": "knowledge",
        "final_status": "running",
        "last_error": None,
    }


def main():
    """启动漏洞复现主流程。

    当前只保留最小骨架：
    - 加载任务
    - 创建流程图
    - 执行流程
    - 输出最终状态
    """

    task = load_task("data/tasks/demo.yaml")
    app_graph = build_app_graph()
    initial_state = build_initial_state(task)
    result = app_graph.invoke(initial_state)
    print(result)


if __name__ == "__main__":
    main()
