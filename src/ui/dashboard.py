"""Main Streamlit dashboard page."""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st

from src.parsers.data_parser import load_archive
from src.services.workgroup_service import WorkgroupService
from src.ui.components.workgroup_selector import render_workgroup_selector
from src.ui.components.meeting_list import render_meeting_list


@st.cache_data
def load_meeting_data():
    """Load meeting data from JSON file with caching.

    Returns:
        List of Meeting objects
    """
    # Try data/ directory first, then repository root
    data_paths = [
        Path("data/meeting-summaries-array-3.json"),
        Path("meeting-summaries-array-3.json"),
    ]

    for data_path in data_paths:
        if data_path.exists():
            return load_archive(str(data_path))

    raise FileNotFoundError(
        "Could not find meeting-summaries-array-3.json in data/ or repository root"
    )


def main():
    """Main dashboard function."""
    st.set_page_config(
        page_title="Meeting Archive Dashboard",
        page_icon="📊",
        layout="wide",
    )

    st.title("📊 Meeting Archive Dashboard")
    st.markdown("Browse meeting archives by workgroup")

    try:
        # Load data (cached)
        meetings = load_meeting_data()
        st.success(f"Loaded {len(meetings)} meetings from archive")

        # Initialize service
        service = WorkgroupService(meetings)

        # Sidebar for workgroup selection
        with st.sidebar:
            st.header("Filters")
            workgroups = service.get_all_workgroups()
            selected_workgroup = render_workgroup_selector(workgroups)

            # Sort order selector
            sort_order = st.radio(
                "Sort Order",
                options=["newest", "oldest"],
                index=0,
                help="Choose how to sort meetings chronologically",
            )

        # Main content area
        if selected_workgroup:
            st.header(f"Meetings for {selected_workgroup}")

            # Get meetings for selected workgroup
            workgroup_meetings = service.get_meetings_by_workgroup(
                selected_workgroup, sort_order=sort_order
            )

            # Display meetings
            render_meeting_list(workgroup_meetings, sort_order=sort_order)
        else:
            st.info("👈 Select a workgroup from the sidebar to view meetings")

    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        st.info(
            "Please ensure meeting-summaries-array-3.json is in the data/ directory or repository root"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.exception(e)


if __name__ == "__main__":
    main()

