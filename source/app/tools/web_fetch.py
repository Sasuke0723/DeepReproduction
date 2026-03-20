"""文件说明：网页抓取工具接口。

这个模块负责下载参考页面、公告、补丁说明等外部文本资源，
并将抓取结果转成统一结构，供知识阶段后续清洗和抽取。

这里不处理清洗逻辑，只处理“获取内容”和“保存基础元信息”。
"""

from typing import List

from app.schemas.fetched_page import FetchedPage


class WebFetchTool:
    """网页抓取接口。"""

    def fetch_one(self, url: str) -> FetchedPage:
        """抓取单个页面并返回结构化结果。"""

        raise NotImplementedError

    def fetch_many(self, urls: List[str]) -> List[FetchedPage]:
        """批量抓取多个页面。"""

        raise NotImplementedError
