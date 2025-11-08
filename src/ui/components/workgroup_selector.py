"""Streamlit UI component for workgroup selection."""

import streamlit as st
from typing import List, Optional

from src.models.workgroup import Workgroup


def render_workgroup_selector(workgroups: List[Workgroup]) -> Optional[str]:
    """Render a workgroup selector dropdown.

    Args:
        workgroups: List of Workgroup objects

    Returns:
        Selected workgroup name or None if no selection
    """
    if not workgroups:
        st.info("No workgroups available.")
        return None

    workgroup_names = [wg.name for wg in workgroups]
    workgroup_names.sort()  # Sort alphabetically for better UX

    selected_workgroup = st.selectbox(
        "Select a Workgroup",
        options=[""] + workgroup_names,
        index=0,
        help="Choose a workgroup to view its meetings",
    )

    if selected_workgroup == "":
        return None

    return selected_workgroup

