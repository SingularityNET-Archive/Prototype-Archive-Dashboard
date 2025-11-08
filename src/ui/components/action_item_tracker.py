"""Streamlit UI component for action item tracker."""

import streamlit as st
from typing import List, Optional
from datetime import datetime, time

from src.models.action_item import ActionItem
from src.services.filter_service import FilterService


def render_action_item_tracker(
    action_items: List[ActionItem],
    filter_service: FilterService,
    selected_workgroup: Optional[str] = None,
    selected_assignee: Optional[str] = None,
    selected_status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> None:
    """Render action item tracker with filtered action items.

    Args:
        action_items: List of ActionItem objects to display
        filter_service: FilterService instance for filtering
        selected_workgroup: Selected workgroup filter (optional)
        selected_assignee: Selected assignee filter (optional)
        selected_status: Selected status filter (optional)
        start_date: Start date filter (optional)
        end_date: End date filter (optional)
    """
    if not action_items:
        st.info("No action items found in the archive.")
        return

    st.header("✅ Action Item Tracker")
    
    # Apply filters
    filtered_items = filter_service.filter_action_items(
        action_items,
        workgroup=selected_workgroup,
        assignee=selected_assignee,
        status=selected_status,
        start_date=start_date,
        end_date=end_date,
    )
    
    st.caption(f"Showing {len(filtered_items)} action item(s) from all meetings")

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
        start_str = start_date.strftime('%Y-%m-%d') if start_date else '...'
        end_str = end_date.strftime('%Y-%m-%d') if end_date else '...'
        filter_info.append(f"Date: {start_str} to {end_str}")

    if filter_info:
        st.subheader(f"Filtered Action Items ({', '.join(filter_info)})")
    else:
        st.subheader("All Action Items")

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

