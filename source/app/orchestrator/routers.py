"""文件说明：阶段路由规则。

这个文件负责回答一个问题：
“某个阶段执行完之后，流程下一步应该去哪里？”

这里不关心阶段内部细节，只依据共享状态中的结果字段做判断。
这样可以把“阶段实现”和“流程跳转”明确分开，方便后续单独调整重试策略。
"""

MAX_BUILD_RETRY = 2
MAX_POC_RETRY = 2


def route_after_build(state):
    """构建阶段后的路由规则。

    返回值语义：
    - `poc`：构建成功，进入 PoC 阶段。
    - `build`：构建失败但仍可重试。
    - `failed`：构建失败且达到重试上限，结束流程。
    """

    build = state.get("build")
    retry_count = state.get("retry_count", {})

    if build and build.build_success:
        return "poc"

    if retry_count.get("build", 0) < MAX_BUILD_RETRY:
        return "build"

    return "failed"


def route_after_poc(state):
    """PoC 阶段后的路由规则。"""

    poc = state.get("poc")
    retry_count = state.get("retry_count", {})

    if poc and poc.execution_success:
        return "verify"

    if retry_count.get("poc", 0) < MAX_POC_RETRY:
        return "poc"

    return "failed"


def route_after_verify(state):
    """验证阶段后的路由规则。"""

    verify = state.get("verify")
    if verify and verify.verdict == "success":
        return "success"
    return "failed"
