"""文件说明：网页抓取结果模型。用于保存原始页面内容、清洗文本和基础元数据。"""

from pydantic import BaseModel


class FetchedPage(BaseModel):
    url: str
    title: str
    html: str
    cleaned_text: str
