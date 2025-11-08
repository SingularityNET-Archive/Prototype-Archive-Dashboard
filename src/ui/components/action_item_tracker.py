"""Streamlit UI component for action item tracker."""

import streamlit as st
from typing import List, Optional
from datetime import datetime, time

from src.models.action_item import ActionItem
from src.services.filter_service import FilterService


def render_action_item_tracker(
    action_items: List[ActionItem],
    filter_service: FilterService,
    available_workgroups: List[str],
) -> None:
    """Render action item tracker with filtering capabilities.

    Args:
        action_items: List of ActionItem objects to display
        filter_service: FilterService instance for filtering
        available_workgroups: List of available workgroup names for filtering
    """
    if not action_items:
        st.info("No action items found in the archive.")
        return

    st.header("✅ Action Item Tracker")
    st.caption(f"Showing {len(action_items)} action item(s) from all meetings")

    # Filters
    with st.expander("🔍 Filter Action Items", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            # Get unique assignees
            assignees = sorted(
                set(
                    item.assignee
                    for item in action_items
                    if item.assignee is not None
                )
            )
            selected_assignee = st.selectbox(
                "Filter by Assignee",
                options=[None] + assignees,
                format_func=lambda x: "All Assignees" if x is None else x,
                help="Filter action items by assignee",
            )

            # Status filter
            status_options = ["todo", "in progress", "done", "cancelled"]
            selected_status = st.selectbox(
                "Filter by Status",
                options=[None] + status_options,
                format_func=lambda x: "All Statuses" if x is None else x.title(),
                help="Filter action items by status",
            )

        with col2:
            # Date range filter
            start_date_raw = st.date_input(
                "Start Date",
                value=None,
                help="Filter action items from this date onwards (based on meeting date)",
            )
            end_date_raw = st.date_input(
                "End Date",
                value=None,
                help="Filter action items up to this date (based on meeting date)",
            )

            # Convert date objects to datetime objects
            start_date = (
                datetime.combine(start_date_raw, time.min) if start_date_raw else None
            )
            end_date = (
                datetime.combine(end_date_raw, time.max) if end_date_raw else None
            )

            # Validate date range
            if start_date and end_date and start_date > end_date:
                st.warning("⚠️ Start date must be before or equal to end date")
                start_date = None
                end_date = None

    # Apply filters
    filtered_items = filter_service.filter_action_items(
        action_items,
        assignee=selected_assignee,
        status=selected_status,
        start_date=start_date,
        end_date=end_date,
    )

    if not filtered_items:
        st.warning(
            "No action items match the current filters. Try adjusting your filter criteria."
        )
        return

    # Display count
    filter_info = []
    if selected_assignee:
        filter_info.append(f"Assignee: {selected_assignee}")
    if selected_status:
        filter_info.append(f"Status: {selected_status.title()}")
    if start_date or end_date:
        date_range = f"{start_date_raw.strftime('%Y-%m-%d') if start_date_raw else '...'} to {end_date_raw.strftime('%Y-%m-%d') if end_date_raw else '...'}"
        filter_info.append(f"Date: {date_range}")

    if filter_info:
        st.subheader(f"Filtered Action Items ({', '.join(filter_info)})")
    else:
        st.subheader("All Action Items")

    st.caption(f"Showing {len(filtered_items)} of {len(action_items)} action item(s)")

    # Group by status for better organization
    status_groups = {
        "todo": [],
        "in progress": [],
        "done": [],
        "cancelled": [],
    }

    for item in filtered_items:
        if item.status in status_groups:
            status_groups[item.status].append(item)
        else:
            status_groups["todo"].append(item)  # Default to todo

    # Display by status
    for status, items in status_groups.items():
        if not items:
            continue

        status_emoji = {
            "todo": "📝",
            "in progress": "🔄",
            "done": "✅",
            "cancelled": "❌",
        }

        with st.expander(
            f"{status_emoji.get(status, '📋')} {status.title()} ({len(items)})",
            expanded=status in ["todo", "in progress"],
        ):
            for item in items:
                with st.container():
                    # Action Item Text
                    st.write(f"**{item.text}**")

                    # Metadata in columns
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if item.assignee:
                            st.write(f"**Assignee:** {item.assignee}")
                        else:
                            st.write("**Assignee:** *Unassigned*")

                    with col2:
                        st.write(f"**Workgroup:** {item.workgroup}")
                        st.write(f"**Date:** {item.date.strftime('%Y-%m-%d')}")

                    with col3:
                        if item.due_date:
                            st.write(f"**Due Date:** {item.due_date}")
                        else:
                            st.write("**Due Date:** *Not specified*")

                    # Meeting ID (for reference)
                    st.caption(f"Meeting ID: {item.meeting_id}")
                    st.divider()

