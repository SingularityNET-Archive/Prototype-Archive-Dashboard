"""Streamlit UI component for date range filtering."""

import streamlit as st
from datetime import datetime, date
from typing import Optional, Tuple


def render_date_filter() -> Tuple[Optional[date], Optional[date]]:
    """Render date range filter inputs.

    Returns:
        Tuple of (start_date, end_date) or (None, None) if not set
    """
    st.subheader("Date Range")

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=None,
            key="date_filter_start",
            help="Filter meetings from this date onwards",
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=None,
            key="date_filter_end",
            help="Filter meetings up to this date",
        )

    # Validate date range
    if start_date and end_date and start_date > end_date:
        st.warning("⚠️ Start date must be before or equal to end date")
        return None, None

    return start_date, end_date

