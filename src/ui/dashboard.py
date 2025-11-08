"""Main Streamlit dashboard page."""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
from datetime import datetime, time

from src.parsers.data_parser import load_archive
from src.services.workgroup_service import WorkgroupService
from src.services.filter_service import FilterService
from src.services.aggregation_service import AggregationService
from src.ui.components.workgroup_selector import render_workgroup_selector
from src.ui.components.meeting_list import render_meeting_list
from src.ui.components.date_filter import render_date_filter
from src.ui.components.tag_filter import render_tag_filter
from src.ui.components.decision_tracker import render_decision_tracker
from src.ui.components.action_item_tracker import render_action_item_tracker


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

        # Initialize services
        workgroup_service = WorkgroupService(meetings)
        filter_service = FilterService()
        aggregation_service = AggregationService()

        # Get workgroups for filters
        workgroups = workgroup_service.get_all_workgroups()
        workgroup_names = [wg.name for wg in workgroups]

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Meetings", "📋 Decisions", "✅ Action Items"])

        # Tab 1: Meetings Browser
        with tab1:
            # Sidebar for filters
            with st.sidebar:
                st.header("Filters")

                # Workgroup selector
                selected_workgroup = render_workgroup_selector(workgroups)

                # Date range filter
                start_date_raw, end_date_raw = render_date_filter()
                
                # Convert date objects to datetime objects for comparison with pandas datetime64[ns]
                # Start date: beginning of day (00:00:00)
                # End date: end of day (23:59:59) to include the entire day
                start_date = datetime.combine(start_date_raw, time.min) if start_date_raw else None
                end_date = datetime.combine(end_date_raw, time.max) if end_date_raw else None

                # Tag filter
                selected_tags = render_tag_filter(meetings)

                # Clear all filters button
                if st.button("Clear All Filters", use_container_width=True):
                    st.rerun()

                # Sort order selector
                st.divider()
                st.subheader("Sort Options")
                sort_order = st.radio(
                    "Sort Order",
                    options=["newest", "oldest"],
                    index=0,
                    help="Choose how to sort meetings chronologically",
                )

            # Main content area
            # Apply filters (workgroup filter is handled by FilterService)
            filtered_meetings = filter_service.filter_meetings(
                meetings,
                workgroup=selected_workgroup,
                start_date=start_date,
                end_date=end_date,
                tags=selected_tags,
            )

            # Sort chronologically
            if sort_order == "oldest":
                filtered_meetings.sort(key=lambda m: m.date)
            else:  # newest (default)
                filtered_meetings.sort(key=lambda m: m.date, reverse=True)

            # Display meetings
            if selected_workgroup:
                st.header(f"Meetings for {selected_workgroup}")
                if len(filtered_meetings) != len(meetings):
                    st.caption(
                        f"Showing {len(filtered_meetings)} of {len(meetings)} meetings (filters applied)"
                    )
                render_meeting_list(filtered_meetings, sort_order=sort_order)
            else:
                if filtered_meetings:
                    st.header("All Meetings")
                    if len(filtered_meetings) != len(meetings):
                        st.caption(
                            f"Showing {len(filtered_meetings)} of {len(meetings)} meetings (filters applied)"
                        )
                    render_meeting_list(filtered_meetings, sort_order=sort_order)
                else:
                    st.info("👈 Select a workgroup from the sidebar to view meetings")
                    if start_date or end_date or selected_tags:
                        st.warning(
                            "No meetings match the current filters. Try adjusting your filter criteria."
                        )

        # Tab 2: Decision Tracker
        with tab2:
            # Aggregate all decisions
            all_decisions = aggregation_service.aggregate_decisions(meetings)
            
            # Render decision tracker with filtering
            render_decision_tracker(
                all_decisions,
                filter_service,
                workgroup_names,
            )

        # Tab 3: Action Item Tracker
        with tab3:
            # Aggregate all action items
            all_action_items = aggregation_service.aggregate_action_items(meetings)
            
            # Render action item tracker with filtering
            render_action_item_tracker(
                all_action_items,
                filter_service,
                workgroup_names,
            )

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

