"""文件说明：内容清洗工具接口。

这个模块负责把网页、公告、提交说明等原始文本整理为适合模型消费的干净内容。
它服务于知识阶段，但不关心漏洞知识如何抽取，只关心文本本身如何被标准化。

建议职责：
1. 去除 HTML 噪声和导航内容。
2. 过滤无关段落，保留漏洞相关文本。
3. 截断超长内容，生成适合提示词的片段。
4. 在需要时保留标题、段落结构和代码块边界。
"""

from pydantic import BaseModel, Field


class CleanedContent(BaseModel):
    """清洗后的文本结果。"""

    title: str = Field(default="", description="清洗后保留的标题")
    cleaned_text: str = Field(default="", description="清洗后的正文内容")
    summary_hint: str = Field(default="", description="可选的摘要提示")


class ContentCleaner:
    """内容清洗器接口。"""

    def clean_html(self, html: str, source_url: str = "") -> CleanedContent:
        """将 HTML 内容转换为可读文本。"""

        raise NotImplementedError

    def clean_markdown(self, markdown_text: str, source_url: str = "") -> CleanedContent:
        """将 Markdown 内容转换为标准清洗结果。"""

        raise NotImplementedError

    def trim_for_prompt(self, cleaned: CleanedContent, max_chars: int) -> CleanedContent:
        """按提示词预算裁剪文本内容。"""

        raise NotImplementedError
