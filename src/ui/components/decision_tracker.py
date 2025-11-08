"""Streamlit UI component for decision tracker."""

import streamlit as st
from typing import List, Optional

from src.models.decision import Decision
from src.services.filter_service import FilterService


def render_decision_tracker(
    decisions: List[Decision],
    filter_service: FilterService,
    available_workgroups: List[str],
) -> None:
    """Render decision tracker with filtering capabilities.

    Args:
        decisions: List of Decision objects to display
        filter_service: FilterService instance for filtering
        available_workgroups: List of available workgroup names for filtering
    """
    if not decisions:
        st.info("No decisions found in the archive.")
        return

    st.header("📋 Decision Tracker")
    st.caption(f"Showing {len(decisions)} decision(s) from all meetings")

    # Filters in sidebar (if not already in main sidebar)
    with st.expander("🔍 Filter Decisions", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            selected_workgroup = st.selectbox(
                "Filter by Workgroup",
                options=[None] + available_workgroups,
                format_func=lambda x: "All Workgroups" if x is None else x,
                help="Filter decisions by workgroup",
            )

    # Apply filters
    filtered_decisions = filter_service.filter_decisions(
        decisions,
        workgroup=selected_workgroup,
    )

    if not filtered_decisions:
        st.warning(
            "No decisions match the current filters. Try adjusting your filter criteria."
        )
        return

    # Display count
    if selected_workgroup:
        st.subheader(f"Decisions for {selected_workgroup}")
    else:
        st.subheader("All Decisions")

    st.caption(f"Showing {len(filtered_decisions)} of {len(decisions)} decision(s)")

    # Display decisions
    for decision in filtered_decisions:
        with st.expander(
            f"📅 {decision.date.strftime('%Y-%m-%d')} - {decision.workgroup}",
            expanded=False,
        ):
            # Workgroup
            st.write(f"**Workgroup:** {decision.workgroup}")

            # Date
            st.write(f"**Date:** {decision.date.strftime('%Y-%m-%d')}")

            # Decision Text
            st.write("**Decision:**")
            st.write(decision.decision_text)

            # Rationale (if available)
            if decision.rationale:
                st.write("**Rationale:**")
                st.write(decision.rationale)

            # Effect
            effect_label = (
                "Affects Only This Workgroup"
                if decision.effect == "affectsOnlyThisWorkgroup"
                else "May Affect Other People"
            )
            st.write(f"**Effect:** {effect_label}")

            # Opposing Views (if available)
            if decision.opposing and decision.opposing.lower() != "none":
                st.write("**Opposing Views:**")
                st.write(decision.opposing)

            # Meeting ID (for reference)
            st.caption(f"Meeting ID: {decision.meeting_id}")

