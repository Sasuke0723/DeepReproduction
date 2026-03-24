"""Reference extraction and normalization utilities."""

from __future__ import annotations

from typing import Iterable, List
from urllib.parse import urlsplit, urlunsplit

from app.schemas.task import TaskModel


class ReferenceExtractor:
    """Collect and normalize reference URLs for the knowledge agent."""

    _BLOCKED_DOMAINS = {
        "facebook.com",
        "twitter.com",
        "x.com",
        "linkedin.com",
        "youtube.com",
        "youtu.be",
        "instagram.com",
    }

    def collect_from_task(self, task: TaskModel) -> List[str]:
        """Collect task references plus the primary CVE URL."""

        references = list(task.references)
        if task.cve_url:
            references.insert(0, task.cve_url)
        return self.normalize(references)

    def normalize(self, references: Iterable[str]) -> List[str]:
        """Normalize URLs and keep deterministic order."""

        normalized: list[str] = []
        seen: set[str] = set()

        for reference in references:
            if not reference:
                continue
            cleaned = reference.strip()
            parts = urlsplit(cleaned)
            if parts.scheme not in {"http", "https"}:
                continue
            normalized_url = urlunsplit((parts.scheme, parts.netloc.lower(), parts.path, parts.query, ""))
            if normalized_url in seen:
                continue
            seen.add(normalized_url)
            normalized.append(normalized_url)

        return normalized

    def filter_relevant(self, references: Iterable[str]) -> List[str]:
        """Drop obviously irrelevant or noisy domains."""

        kept: list[str] = []
        for reference in references:
            hostname = urlsplit(reference).netloc.lower()
            if any(hostname.endswith(domain) for domain in self._BLOCKED_DOMAINS):
                continue
            kept.append(reference)
        return kept
