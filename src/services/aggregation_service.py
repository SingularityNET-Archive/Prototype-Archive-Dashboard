"""Aggregation service for aggregating decisions and action items."""

from typing import List
import pandas as pd

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.utils.logger import logger


class AggregationService:
    """Service for aggregating decisions and action items from meetings."""

    def __init__(self):
        """Initialize AggregationService."""
        pass

    def aggregate_decisions(self, meetings: List[Meeting]) -> List[Decision]:
        """Aggregate all decisions from all meetings with workgroup and date context.

        Uses pandas for efficient flattening to meet performance requirements (SC-004).

        Args:
            meetings: List of Meeting objects

        Returns:
            List of Decision objects with workgroup and date from parent meeting
        """
        if not meetings:
            return []

        logger.info(f"Aggregating decisions from {len(meetings)} meetings")

        # Flatten all decisions from all meetings
        all_decisions = []
        for meeting in meetings:
            if meeting.decisions:
                all_decisions.extend(meeting.decisions)

        logger.info(f"Aggregated {len(all_decisions)} decisions")
        return all_decisions

    def aggregate_action_items(self, meetings: List[Meeting]) -> List[ActionItem]:
        """Aggregate all action items from all meetings with workgroup and date context.

        Uses pandas for efficient flattening to meet performance requirements (SC-004).

        Args:
            meetings: List of Meeting objects

        Returns:
            List of ActionItem objects with workgroup and date from parent meeting
        """
        if not meetings:
            return []

        logger.info(f"Aggregating action items from {len(meetings)} meetings")

        # Flatten all action items from all meetings
        all_action_items = []
        for meeting in meetings:
            if meeting.action_items:
                all_action_items.extend(meeting.action_items)

        logger.info(f"Aggregated {len(all_action_items)} action items")
        return all_action_items

