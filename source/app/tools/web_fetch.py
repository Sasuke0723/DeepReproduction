"""Web fetching utilities for the knowledge agent."""

from __future__ import annotations

import mimetypes
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from app.schemas.fetched_page import FetchedPage


class _LinkExtractor(HTMLParser):
    """Simple hyperlink extractor for recursive crawling."""

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if not href:
            return
        self.links.append(urljoin(self.base_url, href))


class WebFetchTool:
    """Fetch web pages or downloadable resources."""

    _USER_AGENT = "DeepReproductionKnowledgeAgent/1.0"

    def fetch_one(self, url: str, download_dir: Optional[str] = None, timeout: int = 20) -> FetchedPage:
        """Fetch a single URL and return normalized metadata."""

        request = Request(url, headers={"User-Agent": self._USER_AGENT})
        with urlopen(request, timeout=timeout) as response:
            raw_bytes = response.read()
            status_code = getattr(response, "status", 200)
            content_type = response.headers.get_content_type()
            charset = response.headers.get_content_charset() or "utf-8"

        local_path: Optional[str] = None
        html_text = ""
        links: list[str] = []
        title = ""

        if content_type.startswith("text/") or content_type in {"application/json", "application/xml"}:
            html_text = raw_bytes.decode(charset, errors="replace")
            if content_type == "text/html":
                title = self._extract_title(html_text)
                links = self._extract_links(html_text, base_url=url)
            else:
                title = Path(urlparse(url).path).name or url
        else:
            if download_dir:
                local_path = self._save_binary(url=url, payload=raw_bytes, download_dir=download_dir, content_type=content_type)
            title = Path(urlparse(url).path).name or url

        return FetchedPage(
            url=url,
            title=title,
            html=html_text,
            cleaned_text="",
            status_code=status_code,
            content_type=content_type,
            local_path=local_path,
            links=links,
        )

    def fetch_many(self, urls: List[str], download_dir: Optional[str] = None, timeout: int = 20) -> List[FetchedPage]:
        """Fetch many URLs sequentially."""

        pages: list[FetchedPage] = []
        for url in urls:
            try:
                pages.append(self.fetch_one(url=url, download_dir=download_dir, timeout=timeout))
            except Exception:
                continue
        return pages

    def _extract_title(self, html_text: str) -> str:
        match = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.IGNORECASE | re.DOTALL)
        return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""

    def _extract_links(self, html_text: str, base_url: str) -> List[str]:
        extractor = _LinkExtractor(base_url=base_url)
        extractor.feed(html_text)
        return extractor.links

    def _save_binary(self, url: str, payload: bytes, download_dir: str, content_type: str) -> str:
        directory = Path(download_dir)
        directory.mkdir(parents=True, exist_ok=True)

        parsed = urlparse(url)
        filename = Path(parsed.path).name or "downloaded_attachment"
        if "." not in filename:
            extension = mimetypes.guess_extension(content_type) or ".bin"
            filename = f"{filename}{extension}"

        target = directory / filename
        target.write_bytes(payload)
        return str(target)
