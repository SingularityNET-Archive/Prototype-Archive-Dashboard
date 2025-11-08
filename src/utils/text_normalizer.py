"""Text normalization utilities."""

from typing import List, Optional


def parse_comma_separated_string(text: Optional[str]) -> List[str]:
    """Parse a comma-separated string into a list of strings.

    Args:
        text: Comma-separated string (e.g., "Alice, Bob, Charlie")

    Returns:
        List of trimmed strings (empty list if input is None/empty)
    """
    if not text:
        return []

    return [item.strip() for item in text.split(",") if item.strip()]


def normalize_name(name: str) -> str:
    """Normalize a person's name for consistent matching.

    Handles variations like brackets, aliases, and case variations.

    Args:
        name: Person's name (e.g., "Stephen [QADAO]")

    Returns:
        Normalized name string
    """
    if not name:
        return ""

    # Trim whitespace
    normalized = name.strip()

    # Handle bracket aliases - keep the main name and alias
    # "Stephen [QADAO]" -> "Stephen [QADAO]" (preserve for display)
    # Could be extended to extract just "Stephen" for matching if needed

    return normalized


def normalize_topic(topic: str) -> str:
    """Normalize a topic name for consistent matching.

    Trims whitespace and handles case variations.

    Args:
        topic: Topic name

    Returns:
        Normalized topic string (trimmed, lowercase for matching)
    """
    if not topic:
        return ""

    return topic.strip().lower()


def normalize_topics(topics: List[str]) -> List[str]:
    """Normalize a list of topic names.

    Args:
        topics: List of topic names

    Returns:
        List of normalized topic strings
    """
    return [normalize_topic(topic) for topic in topics if topic.strip()]

