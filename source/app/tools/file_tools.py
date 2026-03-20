"""文件说明：文件工具接口。

这个模块负责工作区文件和阶段产物的统一读写。
它的目标不是提供所有文件系统能力，而是为框架约定一套稳定的落盘接口。

适用场景：
- 写入 Dockerfile、build.sh、run.sh
- 保存知识阶段中间产物
- 读取日志和报告文件
- 创建和准备工作区目录
"""

from typing import Any


class FileTool:
    """文件系统操作接口。"""

    def ensure_dir(self, path: str) -> None:
        """确保目录存在。"""

        raise NotImplementedError

    def write_text(self, path: str, content: str) -> None:
        """写入文本文件。"""

        raise NotImplementedError

    def read_text(self, path: str) -> str:
        """读取文本文件。"""

        raise NotImplementedError

    def write_json(self, path: str, payload: Any) -> None:
        """写入 JSON 文件。"""

        raise NotImplementedError

    def exists(self, path: str) -> bool:
        """判断路径是否存在。"""

        raise NotImplementedError
