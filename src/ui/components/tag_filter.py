"""Streamlit UI component for tag/topic filtering."""

import streamlit as st
from typing import List, Optional

from src.models.meeting import Meeting
from src.utils.topic_extractor import extract_all_topics


def render_tag_filter(meetings: List[Meeting]) -> Optional[List[str]]:
    """Render tag filter multiselect.

    Args:
        meetings: List of Meeting objects to extract topics from

    Returns:
        List of selected topic tags or None if none selected
    """
    st.subheader("Topics")

    # Extract all unique topics
    all_topics = extract_all_topics(meetings)

    if not all_topics:
        st.info("No topics available in meetings.")
        return None

    selected_tags = st.multiselect(
        "Select Topics",
        options=all_topics,
        default=None,
        help="Filter meetings by topics covered. Select one or more topics.",
    )

    if not selected_tags:
        return None

    return selected_tags

