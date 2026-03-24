"""Fetched page schema used by the knowledge agent."""

from typing import List, Optional

from pydantic import BaseModel, Field


class FetchedPage(BaseModel):
    """Normalized representation of a fetched web resource."""

    url: str = Field(..., description="Fetched URL.")
    title: str = Field(default="", description="Best-effort page title.")
    html: str = Field(default="", description="Raw HTML or decoded text content.")
    cleaned_text: str = Field(default="", description="Rule-cleaned text content.")
    status_code: int = Field(default=0, description="HTTP status code.")
    content_type: str = Field(default="", description="HTTP content type.")
    local_path: Optional[str] = Field(default=None, description="Local file path for downloaded content.")
    links: List[str] = Field(default_factory=list, description="Extracted child links.")
