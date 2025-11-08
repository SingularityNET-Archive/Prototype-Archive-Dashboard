"""Utility functions for extracting topics from meetings."""

from typing import List, Set
from src.models.meeting import Meeting
from src.utils.text_normalizer import normalize_topic


def extract_all_topics(meetings: List[Meeting]) -> List[str]:
    """Extract all unique topics from meetings.

    Args:
        meetings: List of Meeting objects

    Returns:
        List of unique topic names (preserving original case for display)
    """
    topics_set: Set[str] = set()

    for meeting in meetings:
        if meeting.topics_covered:
            topics_set.update(meeting.topics_covered)

    # Return sorted list for consistent ordering
    return sorted(list(topics_set))


def extract_topics_normalized(meetings: List[Meeting]) -> Set[str]:
    """Extract all unique normalized topics from meetings (for matching).

    Args:
        meetings: List of Meeting objects

    Returns:
        Set of normalized topic names (lowercase, for matching)
    """
    topics_set: Set[str] = set()

    for meeting in meetings:
        if meeting.topics_covered:
            normalized = [normalize_topic(topic) for topic in meeting.topics_covered]
            topics_set.update(normalized)

    return topics_set

