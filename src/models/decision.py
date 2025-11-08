"""Decision data model."""

from datetime import datetime
from typing import Optional


class Decision:
    """Represents a decision made in a meeting."""

    def __init__(
        self,
        id: str,
        meeting_id: str,
        workgroup: str,
        date: datetime,
        decision_text: str,
        effect: str,
        rationale: Optional[str] = None,
        opposing: Optional[str] = None,
    ):
        """Initialize a Decision object.

        Args:
            id: Unique identifier for the decision
            meeting_id: Reference to parent meeting
            workgroup: Workgroup name (from parent meeting)
            date: Meeting date (from parent meeting)
            decision_text: The decision text
            effect: Effect scope - "affectsOnlyThisWorkgroup" or "mayAffectOtherPeople"
            rationale: Rationale for the decision (optional)
            opposing: Opposing views or "none" (optional)
        """
        self.id = id
        self.meeting_id = meeting_id
        self.workgroup = workgroup
        self.date = date
        self.decision_text = decision_text.strip() if decision_text else ""
        self.rationale = rationale.strip() if rationale else None
        self.opposing = opposing.strip() if opposing else None

        # Validate
        if not self.decision_text:
            raise ValueError("decision_text must be non-empty")
        
        # Normalize and validate effect (case-insensitive)
        effect_normalized = (effect or "affectsOnlyThisWorkgroup").lower()
        valid_effects = ["affectsonlythisworkgroup", "mayaffectotherpeople"]
        if effect_normalized not in valid_effects:
            raise ValueError(
                f"effect must be 'affectsOnlyThisWorkgroup' or 'mayAffectOtherPeople', got: {effect}"
            )
        
        # Store normalized effect for matching, but preserve original case for display
        if effect_normalized == "affectsonlythisworkgroup":
            self.effect = "affectsOnlyThisWorkgroup"
        else:
            self.effect = "mayAffectOtherPeople"

    def __repr__(self) -> str:
        """Return string representation of Decision."""
        return f"Decision(id={self.id}, workgroup={self.workgroup}, date={self.date})"

