"""Task schema used by the knowledge agent."""

from typing import List, Optional

from pydantic import BaseModel, Field


class TaskReference(BaseModel):
    """Structured reference entry preserved from OSV or task input."""

    url: str = Field(..., description="Reference URL.")
    type: Optional[str] = Field(default=None, description="Reference type such as FIX or EVIDENCE.")


class TaskModel(BaseModel):
    """Normalized task payload for a single CVE."""

    task_id: str = Field(..., description="Stable task identifier.")
    cve_id: str = Field(..., description="CVE identifier.")
    cve_url: Optional[str] = Field(default=None, description="Primary CVE or OSV URL.")
    repo_url: Optional[str] = Field(default=None, description="Source repository URL.")
    vulnerable_ref: Optional[str] = Field(default=None, description="Vulnerable revision.")
    fixed_ref: Optional[str] = Field(default=None, description="Fixed revision.")
    language: Optional[str] = Field(default=None, description="Primary project language.")
    references: List[str] = Field(default_factory=list, description="Candidate references.")
    reference_details: List[TaskReference] = Field(default_factory=list, description="Structured reference metadata.")
