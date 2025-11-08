"""Meeting data model."""

from datetime import datetime
from typing import List, Optional, Dict, Any


class Meeting:
    """Represents a single meeting record from the archive."""

    def __init__(
        self,
        id: str,
        workgroup: str,
        workgroup_id: str,
        date: datetime,
        type: str,
        no_summary_given: bool,
        canceled_summary: bool,
        host: Optional[str] = None,
        documenter: Optional[str] = None,
        people_present: Optional[List[str]] = None,
        purpose: Optional[str] = None,
        type_of_meeting: Optional[str] = None,
        meeting_video_link: Optional[str] = None,
        working_docs: Optional[List[Dict[str, str]]] = None,
        action_items: Optional[List[Any]] = None,  # Will be ActionItem objects
        decisions: Optional[List[Any]] = None,  # Will be Decision objects
        discussion_points: Optional[List[str]] = None,
        topics_covered: Optional[List[str]] = None,
        emotions: Optional[List[str]] = None,
    ):
        """Initialize a Meeting object.

        Args:
            id: Unique identifier for the meeting
            workgroup: Workgroup name
            workgroup_id: Unique workgroup identifier (UUID format)
            date: Meeting date (datetime object)
            type: Meeting type (e.g., "Custom")
            no_summary_given: Flag indicating if summary was provided
            canceled_summary: Flag indicating if summary was canceled
            host: Meeting host name (optional)
            documenter: Person who documented the meeting (optional)
            people_present: List of people present (optional)
            purpose: Meeting purpose/description (optional)
            type_of_meeting: Type of meeting (e.g., "Monthly", "Weekly") (optional)
            meeting_video_link: URL to meeting video (optional)
            working_docs: List of {title: str, link: str} objects (optional)
            action_items: List of action items from this meeting (optional)
            decisions: List of decisions from this meeting (optional)
            discussion_points: List of discussion points (optional)
            topics_covered: List of topics (optional)
            emotions: List of emotions (optional)
        """
        self.id = id
        self.workgroup = workgroup
        self.workgroup_id = workgroup_id
        self.date = date
        self.type = type
        self.no_summary_given = no_summary_given
        self.canceled_summary = canceled_summary
        self.host = host
        self.documenter = documenter
        self.people_present = people_present or []
        self.purpose = purpose
        self.type_of_meeting = type_of_meeting
        self.meeting_video_link = meeting_video_link
        self.working_docs = working_docs or []
        self.action_items = action_items or []
        self.decisions = decisions or []
        self.discussion_points = discussion_points or []
        self.topics_covered = topics_covered or []
        self.emotions = emotions or []

    def __repr__(self) -> str:
        """Return string representation of Meeting."""
        return f"Meeting(id={self.id}, workgroup={self.workgroup}, date={self.date})"

