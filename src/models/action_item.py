"""Action item data model."""

from datetime import datetime
from typing import Optional


class ActionItem:
    """Represents a task or action item from a meeting."""

    def __init__(
        self,
        id: str,
        meeting_id: str,
        workgroup: str,
        date: datetime,
        text: str,
        status: str,
        assignee: Optional[str] = None,
        due_date: Optional[str] = None,
    ):
        """Initialize an ActionItem object.

        Args:
            id: Unique identifier for the action item
            meeting_id: Reference to parent meeting
            workgroup: Workgroup name (from parent meeting)
            date: Meeting date (from parent meeting)
            text: Action item description
            status: Status - "todo", "in progress", "done", or "cancelled"
            assignee: Person assigned to the action (optional)
            due_date: Due date (may be in various formats, e.g., "15 January 2025") (optional)
        """
        self.id = id
        self.meeting_id = meeting_id
        self.workgroup = workgroup
        self.date = date
        self.text = text.strip() if text else ""
        self.status = self._normalize_status(status)
        self.assignee = assignee.strip() if assignee else None
        self.due_date = due_date.strip() if due_date else None

        # Validate
        if not self.text:
            raise ValueError("text must be non-empty")
        valid_statuses = ["todo", "in progress", "done", "cancelled"]
        if self.status not in valid_statuses:
            raise ValueError(
                f"status must be one of {valid_statuses}, got: {status}"
            )

    def _normalize_status(self, status: str) -> str:
        """Normalize status value (case-insensitive matching, handle variations).

        Args:
            status: Status string to normalize

        Returns:
            Normalized status string
        """
        if not status:
            return "todo"  # Default

        status_lower = status.lower().strip()

        # Handle variations
        if status_lower in ["todo", "to do", "to-do"]:
            return "todo"
        elif status_lower in ["in progress", "in-progress", "inprogress", "in_progress"]:
            return "in progress"
        elif status_lower in ["done", "completed", "complete"]:
            return "done"
        elif status_lower in ["cancelled", "canceled", "cancelled"]:
            return "cancelled"
        else:
            # Default to todo if unrecognized
            return "todo"

    def __repr__(self) -> str:
        """Return string representation of ActionItem."""
        return f"ActionItem(id={self.id}, workgroup={self.workgroup}, assignee={self.assignee}, status={self.status})"

