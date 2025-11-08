"""Topic data model."""

from typing import List, Set, Dict


class Topic:
    """Represents a subject or theme discussed in meetings."""

    def __init__(
        self,
        name: str,
        meetings: List[str] = None,
        workgroups: Set[str] = None,
        co_occurrences: Dict[str, int] = None,
    ):
        """Initialize a Topic object.

        Args:
            name: Topic name (normalized)
            meetings: List of meeting IDs where this topic was discussed
            workgroups: Set of workgroup IDs that discussed this topic
            co_occurrences: Dictionary of topics that co-occur: {topic_name: count}
        """
        self.name = name
        self.meetings = meetings or []
        self.workgroups = workgroups or set()
        self.co_occurrences = co_occurrences or {}

    def __repr__(self) -> str:
        """Return string representation of Topic."""
        return f"Topic(name={self.name}, meetings={len(self.meetings)}, workgroups={len(self.workgroups)})"

