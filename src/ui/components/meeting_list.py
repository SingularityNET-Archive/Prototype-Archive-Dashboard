"""Streamlit UI component for displaying meeting lists."""

import streamlit as st
from typing import List, Optional

from src.models.meeting import Meeting


def render_meeting_list(meetings: List[Meeting], sort_order: str = "newest"):
    """Render a list of meetings with their metadata.

    Args:
        meetings: List of Meeting objects to display
        sort_order: Sort order indicator for display ("newest" or "oldest")
    """
    if not meetings:
        st.info("No meetings found for the selected workgroup.")
        return

    # Display sort order info
    sort_label = "Newest first" if sort_order == "newest" else "Oldest first"
    st.caption(f"Showing {len(meetings)} meeting(s) - {sort_label}")

    # Display each meeting
    for meeting in meetings:
        with st.expander(
            f"📅 {meeting.date.strftime('%Y-%m-%d')} - {meeting.workgroup}",
            expanded=False,
        ):
            # Date
            st.write(f"**Date:** {meeting.date.strftime('%Y-%m-%d')}")

            # Host (if available)
            if meeting.host:
                st.write(f"**Host:** {meeting.host}")
            else:
                st.write("**Host:** *Not specified*")

            # Documenter (if available)
            if meeting.documenter:
                st.write(f"**Documenter:** {meeting.documenter}")
            else:
                st.write("**Documenter:** *Not specified*")

            # Purpose (if available)
            if meeting.purpose:
                st.write(f"**Purpose:** {meeting.purpose}")
            else:
                st.write("**Purpose:** *Not specified*")

            # People Present
            if meeting.people_present:
                people_str = ", ".join(meeting.people_present)
                st.write(f"**People Present:** {people_str}")
            else:
                st.write("**People Present:** *Not specified*")

            # Type of Meeting
            if meeting.type_of_meeting:
                st.write(f"**Type of Meeting:** {meeting.type_of_meeting}")

            # Meeting Video Link (if available)
            if meeting.meeting_video_link:
                st.write(f"**Video Link:** {meeting.meeting_video_link}")

            # Working Docs (if available)
            if meeting.working_docs:
                st.write("**Working Documents:**")
                for doc in meeting.working_docs:
                    if isinstance(doc, dict) and "title" in doc and "link" in doc:
                        st.write(f"  - [{doc['title']}]({doc['link']})")

            # Topics Covered (if available)
            if meeting.topics_covered:
                topics_str = ", ".join(meeting.topics_covered)
                st.write(f"**Topics Covered:** {topics_str}")

            # Discussion Points (if available)
            if meeting.discussion_points:
                st.write("**Discussion Points:**")
                for point in meeting.discussion_points:
                    st.write(f"  - {point}")

