"""Streamlit UI component for decision tracker."""

import streamlit as st
from typing import List, Optional
from datetime import datetime

from src.models.decision import Decision
from src.services.filter_service import FilterService


def render_decision_tracker(
    decisions: List[Decision],
    filter_service: FilterService,
    selected_workgroup: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> None:
    """Render decision tracker with filtered decisions.

    Args:
        decisions: List of Decision objects to display
        filter_service: FilterService instance for filtering
        selected_workgroup: Selected workgroup filter (optional)
        start_date: Start date filter (optional)
        end_date: End date filter (optional)
    """
    if not decisions:
        st.info("No decisions found in the archive.")
        return

    st.header("📋 Decision Tracker")
    
    # Apply filters
    filtered_decisions = filter_service.filter_decisions(
        decisions,
        workgroup=selected_workgroup,
        start_date=start_date,
        end_date=end_date,
    )
    
    st.caption(f"Showing {len(filtered_decisions)} decision(s) from all meetings")

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

