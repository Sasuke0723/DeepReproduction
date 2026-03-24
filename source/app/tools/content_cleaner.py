"""Content cleaning utilities for the knowledge agent."""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser

from pydantic import BaseModel, Field


class CleanedContent(BaseModel):
    """Normalized cleaned content."""

    title: str = Field(default="", description="Title retained after cleaning.")
    cleaned_text: str = Field(default="", description="Cleaned plain text.")
    summary_hint: str = Field(default="", description="Short hint for downstream synthesis.")


class _TextExtractor(HTMLParser):
    """Small HTML to text extractor without external dependencies."""

    def __init__(self) -> None:
        super().__init__()
        self._title_chunks: list[str] = []
        self._text_chunks: list[str] = []
        self._inside_title = False

    @property
    def title(self) -> str:
        return " ".join(chunk.strip() for chunk in self._title_chunks if chunk.strip())

    @property
    def text(self) -> str:
        return "\n".join(chunk.strip() for chunk in self._text_chunks if chunk.strip())

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        if tag == "title":
            self._inside_title = True
        if tag in {"p", "div", "section", "article", "li", "pre", "code", "h1", "h2", "h3", "br"}:
            self._text_chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        if tag == "title":
            self._inside_title = False
        if tag in {"p", "div", "section", "article", "li", "pre", "code"}:
            self._text_chunks.append("\n")

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if not data.strip():
            return
        if self._inside_title:
            self._title_chunks.append(data)
        self._text_chunks.append(data)


class ContentCleaner:
    """Rule-based cleaner used before any LLM-based summarization."""

    _SCRIPT_STYLE_RE = re.compile(r"<(script|style|noscript).*?>.*?</\1>", re.IGNORECASE | re.DOTALL)
    _COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
    _URL_RE = re.compile(r"https?://\S+")

    def clean_html(self, html_text: str, source_url: str = "") -> CleanedContent:
        """Clean an HTML page into stable text."""

        stripped = self._COMMENT_RE.sub(" ", html_text)
        stripped = self._SCRIPT_STYLE_RE.sub(" ", stripped)

        parser = _TextExtractor()
        parser.feed(stripped)

        title = self._normalize_text(parser.title)
        cleaned_text = self._normalize_text(parser.text)
        cleaned_text = self._drop_noise_lines(cleaned_text)

        return CleanedContent(
            title=title,
            cleaned_text=cleaned_text,
            summary_hint=f"Cleaned from HTML source: {source_url}".strip(),
        )

    def clean_markdown(self, markdown_text: str, source_url: str = "") -> CleanedContent:
        """Clean markdown or plain text into stable text."""

        cleaned_text = self._normalize_text(markdown_text)
        cleaned_text = self._drop_noise_lines(cleaned_text)
        title = cleaned_text.splitlines()[0][:200] if cleaned_text else ""

        return CleanedContent(
            title=title,
            cleaned_text=cleaned_text,
            summary_hint=f"Cleaned from text source: {source_url}".strip(),
        )

    def trim_for_prompt(self, cleaned: CleanedContent, max_chars: int) -> CleanedContent:
        """Trim cleaned content to a prompt-safe size."""

        if len(cleaned.cleaned_text) <= max_chars:
            return cleaned

        trimmed = cleaned.cleaned_text[:max_chars].rsplit("\n", 1)[0].strip()
        return CleanedContent(
            title=cleaned.title,
            cleaned_text=trimmed,
            summary_hint=cleaned.summary_hint,
        )

    def _normalize_text(self, text: str) -> str:
        text = html.unescape(text)
        text = text.replace("\r", "\n")
        text = self._URL_RE.sub(lambda match: match.group(0).strip(), text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _drop_noise_lines(self, text: str) -> str:
        noise_prefixes = (
            "cookie",
            "privacy policy",
            "terms of service",
            "sign in",
            "log in",
            "skip to content",
            "table of contents",
        )
        kept_lines: list[str] = []
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                kept_lines.append("")
                continue
            lowered = line.lower()
            if any(lowered.startswith(prefix) for prefix in noise_prefixes):
                continue
            if len(line) <= 2:
                continue
            kept_lines.append(line)
        return re.sub(r"\n{3,}", "\n\n", "\n".join(kept_lines)).strip()
