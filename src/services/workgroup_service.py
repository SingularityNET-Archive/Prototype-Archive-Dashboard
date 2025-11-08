"""Workgroup service for managing workgroups and their meetings."""

from typing import List, Optional
from collections import defaultdict

from src.models.meeting import Meeting
from src.models.workgroup import Workgroup


class WorkgroupService:
    """Service for managing workgroups and retrieving meetings by workgroup."""

    def __init__(self, meetings: List[Meeting]):
        """Initialize WorkgroupService with a list of meetings.

        Args:
            meetings: List of Meeting objects
        """
        self.meetings = meetings

    def get_all_workgroups(self) -> List[Workgroup]:
        """Extract unique workgroups from meetings.

        Returns:
            List of unique Workgroup objects
        """
        # Group meetings by workgroup
        workgroup_dict = defaultdict(list)
        for meeting in self.meetings:
            workgroup_dict[meeting.workgroup_id].append(meeting)

        # Create Workgroup objects
        workgroups = []
        for workgroup_id, meetings_list in workgroup_dict.items():
            # Get workgroup name from first meeting (all meetings in group have same name)
            workgroup_name = meetings_list[0].workgroup
            workgroup = Workgroup(
                id=workgroup_id,
                name=workgroup_name,
                meetings=meetings_list,
            )
            workgroups.append(workgroup)

        return workgroups

    def get_meetings_by_workgroup(
        self, workgroup_name: str, sort_order: str = "newest"
    ) -> List[Meeting]:
        """Get all meetings for a specific workgroup, sorted chronologically.

        Args:
            workgroup_name: Name of the workgroup
            sort_order: Sort order - "newest" (default) or "oldest"

        Returns:
            List of Meeting objects for the workgroup, sorted chronologically
        """
        workgroup_meetings = [
            meeting
            for meeting in self.meetings
            if meeting.workgroup == workgroup_name
        ]

        # Sort by date
        if sort_order == "oldest":
            workgroup_meetings.sort(key=lambda m: m.date)
        else:  # newest (default)
            workgroup_meetings.sort(key=lambda m: m.date, reverse=True)

        return workgroup_meetings

