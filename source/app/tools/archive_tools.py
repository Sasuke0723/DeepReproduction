"""Archive extraction utilities for the knowledge agent."""

from __future__ import annotations

import tarfile
import zipfile
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field


class ArchiveEntry(BaseModel):
    """Single archive member."""

    path: str = Field(..., description="Archive-relative path.")
    is_dir: bool = Field(default=False, description="Whether the member is a directory.")
    size: int = Field(default=0, description="Uncompressed size.")


class ArchiveExtractionResult(BaseModel):
    """Extraction result metadata."""

    archive_path: str = Field(..., description="Original archive path.")
    output_dir: str = Field(..., description="Directory where the archive was extracted.")
    extracted_files: List[str] = Field(default_factory=list, description="Extracted file paths.")


class ArchiveTool:
    """Extract archive files downloaded by the knowledge agent."""

    def is_supported_archive(self, file_path: str) -> bool:
        """Return whether the file extension is supported."""

        lowered = file_path.lower()
        return lowered.endswith(".zip") or lowered.endswith(".tar") or lowered.endswith(".tar.gz") or lowered.endswith(".tgz")

    def list_entries(self, file_path: str) -> List[ArchiveEntry]:
        """List members in the archive."""

        path = Path(file_path)
        if path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path) as archive:
                return [
                    ArchiveEntry(path=info.filename, is_dir=info.is_dir(), size=info.file_size)
                    for info in archive.infolist()
                ]

        with tarfile.open(path) as archive:
            return [
                ArchiveEntry(path=member.name, is_dir=member.isdir(), size=member.size)
                for member in archive.getmembers()
            ]

    def extract(self, file_path: str, output_dir: str) -> ArchiveExtractionResult:
        """Extract the archive into the target directory."""

        path = Path(file_path)
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        if path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path) as archive:
                archive.extractall(output)
        else:
            with tarfile.open(path) as archive:
                archive.extractall(output)

        extracted_files = [str(item) for item in output.rglob("*") if item.is_file()]
        return ArchiveExtractionResult(
            archive_path=str(path),
            output_dir=str(output),
            extracted_files=extracted_files,
        )
