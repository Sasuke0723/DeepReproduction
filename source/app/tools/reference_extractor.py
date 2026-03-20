"""文件说明：参考资料提取工具接口。

这个模块负责从任务输入和页面内容中整理真正值得抓取的参考链接。
它是 knowledge 阶段的前置工具，用来减少后续抓取噪声。
"""

from typing import List

from app.schemas.task import TaskModel


class ReferenceExtractor:
    """参考资料提取接口。"""

    def collect_from_task(self, task: TaskModel) -> List[str]:
        """从任务模型中提取候选参考链接。"""

        raise NotImplementedError

    def normalize(self, references: List[str]) -> List[str]:
        """去重并标准化参考链接。"""

        raise NotImplementedError

    def filter_relevant(self, references: List[str]) -> List[str]:
        """过滤与漏洞复现无关的参考链接。"""

        raise NotImplementedError
