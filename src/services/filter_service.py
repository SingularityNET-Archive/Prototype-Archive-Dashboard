"""Filter service for filtering meetings, decisions, and action items."""

from typing import List, Optional
from datetime import datetime
import pandas as pd

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.utils.text_normalizer import normalize_topic
from src.utils.logger import logger


class FilterService:
    """Service for filtering meetings and other entities by various criteria."""

    def __init__(self):
        """Initialize FilterService."""
        pass

    def filter_meetings(
        self,
        meetings: List[Meeting],
        workgroup: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Meeting]:
        """Filter meetings by workgroup, date range, and/or tags.

        Uses pandas DataFrame for efficient filtering to meet performance requirements.

        Args:
            meetings: List of Meeting objects to filter
            workgroup: Workgroup name to filter by (optional)
            start_date: Start date for date range filter (optional)
            end_date: End date for date range filter (optional)
            tags: List of topic tags to filter by (optional)

        Returns:
            Filtered list of Meeting objects matching all criteria
        """
        if not meetings:
            return []

        # Convert to DataFrame for efficient filtering
        df = pd.DataFrame(
            [
                {
                    "meeting": m,
                    "workgroup": m.workgroup,
                    "date": m.date,
                    "topics_covered": m.topics_covered,
                }
                for m in meetings
            ]
        )

        # Apply filters with AND logic
        mask = pd.Series([True] * len(df))

        # Workgroup filter
        if workgroup:
            mask = mask & (df["workgroup"] == workgroup)

        # Date range filter
        if start_date:
            mask = mask & (df["date"] >= start_date)
        if end_date:
            mask = mask & (df["date"] <= end_date)

        # Tag filter (check if any tag in tags list appears in meeting.topics_covered)
        if tags:
            # Normalize tags for case-insensitive matching
            normalized_tags = [normalize_topic(tag) for tag in tags]

            def has_matching_tag(topics_list):
                """Check if any normalized tag matches any topic in the list."""
                if not topics_list:
                    return False
                normalized_topics = [normalize_topic(topic) for topic in topics_list]
                return any(nt in normalized_topics for nt in normalized_tags)

            tag_mask = df["topics_covered"].apply(has_matching_tag)
            mask = mask & tag_mask

        # Filter DataFrame and extract Meeting objects
        filtered_df = df[mask]
        filtered_meetings = filtered_df["meeting"].tolist()

        logger.info(
            f"Filtered {len(meetings)} meetings to {len(filtered_meetings)} "
            f"(workgroup={workgroup}, date_range={start_date} to {end_date}, tags={len(tags) if tags else 0})"
        )

        return filtered_meetings

    def filter_decisions(
        self,
        decisions: List[Decision],
        workgroup: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Decision]:
        """Filter decisions by workgroup and/or date range.

        Args:
            decisions: List of Decision objects to filter
            workgroup: Workgroup name to filter by (optional)
            start_date: Start date for date range filter (optional)
            end_date: End date for date range filter (optional)

        Returns:
            Filtered list of Decision objects matching all criteria
        """
        if not decisions:
            return []

        filtered = decisions

        # Filter by workgroup
        if workgroup:
            filtered = [d for d in filtered if d.workgroup == workgroup]

        # Filter by date range
        if start_date:
            filtered = [d for d in filtered if d.date >= start_date]
        if end_date:
            filtered = [d for d in filtered if d.date <= end_date]

        logger.info(
            f"Filtered {len(decisions)} decisions to {len(filtered)} "
            f"(workgroup={workgroup}, date_range={start_date} to {end_date})"
        )

        return filtered

    def filter_action_items(
        self,
        action_items: List[ActionItem],
        workgroup: Optional[str] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[ActionItem]:
        """Filter action items by workgroup, assignee, status, and/or date range.

        Args:
            action_items: List of ActionItem objects to filter
            workgroup: Workgroup name to filter by (optional)
            assignee: Assignee name to filter by (optional)
            status: Status to filter by - "todo", "in progress", "done", "cancelled" (optional)
            start_date: Start date for date range filter (optional)
            end_date: End date for date range filter (optional)

        Returns:
            Filtered list of ActionItem objects matching all criteria
        """
        if not action_items:
            return []

        # Apply filters with AND logic
        filtered = action_items

        # Filter by workgroup
        if workgroup:
            filtered = [a for a in filtered if a.workgroup == workgroup]

        if assignee:
            filtered = [a for a in filtered if a.assignee == assignee]

        if status:
            filtered = [a for a in filtered if a.status == status]

        if start_date:
            filtered = [a for a in filtered if a.date >= start_date]

        if end_date:
            filtered = [a for a in filtered if a.date <= end_date]

        logger.info(
            f"Filtered {len(action_items)} action items to {len(filtered)} "
            f"(workgroup={workgroup}, assignee={assignee}, status={status}, date_range={start_date} to {end_date})"
        )

        return filtered

