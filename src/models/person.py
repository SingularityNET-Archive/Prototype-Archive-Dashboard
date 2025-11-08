"""Person data model."""

from typing import Set, List, Dict


class Person:
    """Represents a community member."""

    def __init__(self, name: str):
        """Initialize a Person object.

        Args:
            name: Person's name (normalized)
        """
        if not name or not name.strip():
            raise ValueError("name must be non-empty string")

        self.name = name.strip()
        self.workgroups: Set[str] = set()  # Set of workgroup IDs
        self.meetings_attended: List[str] = []  # List of meeting IDs
        self.action_items_assigned: List[str] = []  # List of action item IDs
        self.roles: Dict[str, List[str]] = {}  # {workgroup_id: [host, documenter, participant]}

    def add_workgroup(self, workgroup_id: str, role: str = "participant"):
        """Add a workgroup to this person's workgroups with a role.

        Args:
            workgroup_id: Workgroup ID
            role: Role in the workgroup (host, documenter, or participant)
        """
        self.workgroups.add(workgroup_id)
        if workgroup_id not in self.roles:
            self.roles[workgroup_id] = []
        if role not in self.roles[workgroup_id]:
            self.roles[workgroup_id].append(role)

    def add_meeting(self, meeting_id: str):
        """Add a meeting to this person's attended meetings.

        Args:
            meeting_id: Meeting ID
        """
        if meeting_id not in self.meetings_attended:
            self.meetings_attended.append(meeting_id)

    def add_action_item(self, action_item_id: str):
        """Add an action item to this person's assigned action items.

        Args:
            action_item_id: Action item ID
        """
        if action_item_id not in self.action_items_assigned:
            self.action_items_assigned.append(action_item_id)

    def __repr__(self) -> str:
        """Return string representation of Person."""
        return f"Person(name={self.name}, workgroups={len(self.workgroups)}, meetings={len(self.meetings_attended)})"

    def __eq__(self, other):
        """Check equality based on name."""
        if not isinstance(other, Person):
            return False
        return self.name == other.name

    def __hash__(self):
        """Hash based on name."""
        return hash(self.name)

