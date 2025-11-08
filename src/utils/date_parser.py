"""Date parsing utilities."""

from datetime import datetime
from typing import Optional
from dateutil import parser as dateutil_parser
import pandas as pd


def parse_date(date_str: str) -> datetime:
    """Parse a date string to a datetime object.

    Tries ISO format (YYYY-MM-DD) first, then falls back to dateutil.parser
    for flexible date format handling.

    Args:
        date_str: Date string in various formats

    Returns:
        datetime object

    Raises:
        ValueError: If date string cannot be parsed
    """
    if not date_str:
        raise ValueError("Date string cannot be empty")

    # Try pandas first (handles ISO format efficiently)
    try:
        return pd.to_datetime(date_str).to_pydatetime()
    except (ValueError, TypeError):
        pass

    # Fallback to dateutil.parser for flexible parsing
    try:
        return dateutil_parser.parse(date_str)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Unable to parse date string: {date_str}") from e


def parse_optional_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse an optional date string to a datetime object.

    Args:
        date_str: Optional date string

    Returns:
        datetime object or None if input is None/empty
    """
    if not date_str:
        return None
    return parse_date(date_str)

