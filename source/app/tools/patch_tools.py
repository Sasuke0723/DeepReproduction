"""Patch parsing utilities for the knowledge agent."""

from __future__ import annotations

import re
from typing import List

from pydantic import BaseModel, Field


class PatchSummary(BaseModel):
    """Structured summary extracted from a patch."""

    affected_files: List[str] = Field(default_factory=list, description="Affected file list.")
    changed_functions: List[str] = Field(default_factory=list, description="Function or symbol hints.")
    summary: str = Field(default="", description="Short patch summary.")


class PatchTool:
    """Parse unified diff text into structured hints."""

    _FILE_RE = re.compile(r"^\+\+\+\s+b/(.+)$", re.MULTILINE)
    _FUNCTION_RE = re.compile(r"@@.*?@@\s*(.+)$", re.MULTILINE)

    def parse_diff(self, diff_text: str) -> PatchSummary:
        """Parse diff content and extract lightweight metadata."""

        affected_files = sorted(set(self._FILE_RE.findall(diff_text)))
        changed_functions = [item.strip() for item in self._FUNCTION_RE.findall(diff_text) if item.strip()]
        summary = f"Patch touches {len(affected_files)} file(s)." if affected_files else "Patch metadata unavailable."

        return PatchSummary(
            affected_files=affected_files,
            changed_functions=changed_functions[:20],
            summary=summary,
        )

    def extract_hunks(self, diff_text: str) -> List[str]:
        """Return diff hunks split by hunk header."""

        chunks = re.split(r"(?=^@@)", diff_text, flags=re.MULTILINE)
        return [chunk.strip() for chunk in chunks if chunk.strip().startswith("@@")]
