"""文件说明：归档处理工具接口。

这个模块负责处理从网页、公告页或代码托管平台下载下来的压缩附件，
例如 `.zip`、`.tar.gz`、`.tgz` 等归档文件。

它的职责边界是：
1. 判断一个文件是否是可处理的归档文件。
2. 列出归档中的文件清单，便于上层阶段决定是否值得解压。
3. 将归档解压到指定目录。
4. 返回统一的解压结果，供知识阶段或构建阶段继续消费。

这个模块不负责“下载文件”，下载动作仍由 `web_fetch` 或其他下载工具负责。
"""

from typing import List

from pydantic import BaseModel, Field


class ArchiveEntry(BaseModel):
    """归档内单个文件条目。"""

    path: str = Field(..., description="归档内相对路径")
    is_dir: bool = Field(default=False, description="是否为目录")
    size: int = Field(default=0, description="文件大小")


class ArchiveExtractionResult(BaseModel):
    """归档解压结果。"""

    archive_path: str = Field(..., description="原始归档文件路径")
    output_dir: str = Field(..., description="解压输出目录")
    extracted_files: List[str] = Field(default_factory=list, description="解压出的文件列表")


class ArchiveTool:
    """归档处理接口。"""

    def is_supported_archive(self, file_path: str) -> bool:
        """判断当前文件是否是支持的归档格式。"""

        raise NotImplementedError

    def list_entries(self, file_path: str) -> List[ArchiveEntry]:
        """列出归档内的文件条目。"""

        raise NotImplementedError

    def extract(self, file_path: str, output_dir: str) -> ArchiveExtractionResult:
        """将归档文件解压到指定目录。"""

        raise NotImplementedError
