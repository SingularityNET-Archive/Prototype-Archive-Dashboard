"""Workgroup data model."""

from typing import List, Optional
from src.models.meeting import Meeting


class Workgroup:
    """Represents a community workgroup."""

    def __init__(
        self,
        id: str,
        name: str,
        meetings: Optional[List[Meeting]] = None,
    ):
        """Initialize a Workgroup object.

        Args:
            id: Unique workgroup identifier (UUID format)
            name: Workgroup name
            meetings: List of meetings for this workgroup (optional)
        """
        self.id = id
        self.name = name
        self.meetings = meetings or []

    @property
    def meeting_count(self) -> int:
        """Return the number of meetings for this workgroup."""
        return len(self.meetings)

    def __repr__(self) -> str:
        """Return string representation of Workgroup."""
        return f"Workgroup(id={self.id}, name={self.name}, meeting_count={self.meeting_count})"

