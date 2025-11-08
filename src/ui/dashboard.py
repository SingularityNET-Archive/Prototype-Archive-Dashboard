"""Main Streamlit dashboard page."""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
import json
from datetime import datetime, time

from src.parsers.data_parser import load_archive
from src.services.workgroup_service import WorkgroupService
from src.services.filter_service import FilterService
from src.services.aggregation_service import AggregationService
from src.services.graph_service import GraphService
from src.ui.components.workgroup_selector import render_workgroup_selector
from src.ui.components.meeting_list import render_meeting_list
from src.ui.components.date_filter import render_date_filter
from src.ui.components.tag_filter import render_tag_filter
from src.ui.components.decision_tracker import render_decision_tracker
from src.ui.components.action_item_tracker import render_action_item_tracker
from src.ui.components.graph_explorer import render_graph_explorer


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
        graph_service = GraphService()

        # Get workgroups for filters
        workgroups = workgroup_service.get_all_workgroups()
        workgroup_names = [wg.name for wg in workgroups]

        # Sidebar for all filters (shared across all tabs)
        with st.sidebar:
            st.header("Filters")

            # Clear all filters button (placed early so it can reset state)
            if st.button("Clear All Filters", use_container_width=True, key="clear_filters_btn"):
                # Clear all filter-related session state keys
                keys_to_clear = [
                    "workgroup_selector",
                    "date_filter_start",
                    "date_filter_end",
                    "tag_filter",
                    "assignee_filter",
                    "status_filter",
                ]
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

            # Workgroup selector (used for meetings and decisions)
            selected_workgroup = render_workgroup_selector(workgroups)

            # Filter meetings by workgroup to get context for other filters
            # This ensures topics and assignees are filtered by selected workgroup
            meetings_for_filters = filter_service.filter_meetings(
                meetings,
                workgroup=selected_workgroup,
            )

            # Date range filter (used for meetings and action items)
            start_date_raw, end_date_raw = render_date_filter()
            
            # Convert date objects to datetime objects for comparison with pandas datetime64[ns]
            # Start date: beginning of day (00:00:00)
            # End date: end of day (23:59:59) to include the entire day
            start_date = datetime.combine(start_date_raw, time.min) if start_date_raw else None
            end_date = datetime.combine(end_date_raw, time.max) if end_date_raw else None

            # Tag filter (used for meetings) - filtered by selected workgroup
            selected_tags = render_tag_filter(meetings_for_filters)

            # Action Item specific filters - filtered by selected workgroup
            st.divider()
            st.subheader("Action Item Filters")
            
            # Get assignees from action items in the filtered workgroup
            action_items_for_filters = aggregation_service.aggregate_action_items(meetings_for_filters)
            assignees = sorted(
                set(
                    item.assignee
                    for item in action_items_for_filters
                    if item.assignee is not None
                )
            )
            
            # Assignee filter
            selected_assignee = st.selectbox(
                "Filter by Assignee",
                options=[None] + assignees,
                format_func=lambda x: "All Assignees" if x is None else x,
                key="assignee_filter",
                help="Filter action items by assignee (only shows assignees from selected workgroup)",
            )

            # Status filter
            status_options = ["todo", "in progress", "done", "cancelled"]
            selected_status = st.selectbox(
                "Filter by Status",
                options=[None] + status_options,
                format_func=lambda x: "All Statuses" if x is None else x.title(),
                key="status_filter",
                help="Filter action items by status",
            )

            # Sort order selector (for meetings tab)
            st.divider()
            st.subheader("Sort Options")
            sort_order = st.radio(
                "Sort Order",
                options=["newest", "oldest"],
                index=0,
                help="Choose how to sort meetings chronologically",
            )

        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(
            ["📊 Meetings", "📋 Decisions", "✅ Action Items", "🔗 Relationships"]
        )

        # Tab 1: Meetings Browser
        with tab1:

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
            # When no filters are applied, show all meetings
            if not selected_workgroup and not start_date and not end_date and not selected_tags:
                st.header("All Meetings")
                st.caption(f"Showing all {len(meetings)} meetings")
                # Sort all meetings
                all_meetings_sorted = sorted(meetings, key=lambda m: m.date, reverse=(sort_order == "newest"))
                render_meeting_list(all_meetings_sorted, sort_order=sort_order)
            elif selected_workgroup:
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
            # First filter meetings based on workgroup, date, and tags
            # Then aggregate decisions from filtered meetings
            # (Decisions are already filtered since they come from filtered meetings)
            filtered_meetings_for_decisions = filter_service.filter_meetings(
                meetings,
                workgroup=selected_workgroup,
                start_date=start_date,
                end_date=end_date,
                tags=selected_tags,
            )
            
            # Aggregate decisions from filtered meetings
            filtered_decisions = aggregation_service.aggregate_decisions(filtered_meetings_for_decisions)
            
            # Render decision tracker (decisions already filtered via meetings)
            render_decision_tracker(
                filtered_decisions,
                filter_service,
                selected_workgroup=None,  # Already filtered at meeting level
                start_date=None,  # Already filtered at meeting level
                end_date=None,  # Already filtered at meeting level
            )

        # Tab 3: Action Item Tracker
        with tab3:
            # First filter meetings based on workgroup, date, and tags
            # Then aggregate action items from filtered meetings
            # (Workgroup and date already applied via meeting filtering)
            filtered_meetings_for_actions = filter_service.filter_meetings(
                meetings,
                workgroup=selected_workgroup,
                start_date=start_date,
                end_date=end_date,
                tags=selected_tags,
            )
            
            # Aggregate action items from filtered meetings
            filtered_action_items = aggregation_service.aggregate_action_items(filtered_meetings_for_actions)
            
            # Render action item tracker with action-item-specific filters
            # (Workgroup and date already filtered at meeting level)
            render_action_item_tracker(
                filtered_action_items,
                filter_service,
                selected_workgroup=None,  # Already filtered at meeting level
                selected_assignee=selected_assignee,
                selected_status=selected_status,
                start_date=None,  # Already filtered at meeting level
                end_date=None,  # Already filtered at meeting level
            )

        # Tab 4: Graph Explorer (lazy loaded - only builds when tab is selected)
        with tab4:
            # Render graph explorer with filters from sidebar
            # Graph is built lazily when this tab is selected
            render_graph_explorer(
                meetings,
                graph_service,
                selected_workgroup=selected_workgroup,
                start_date=start_date,
                end_date=end_date,
            )

    except FileNotFoundError as e:
        st.error("❌ **Data File Not Found**")
        st.error(f"Could not find the meeting archive file: {e}")
        st.info(
            "**How to fix:**\n"
            "- Ensure `meeting-summaries-array-3.json` is in the `data/` directory, or\n"
            "- Place it in the repository root directory"
        )
        st.code("data/meeting-summaries-array-3.json", language="text")
    except json.JSONDecodeError as e:
        st.error("❌ **Invalid JSON Format**")
        st.error(f"The meeting archive file contains invalid JSON: {e}")
        st.info(
            "**How to fix:**\n"
            "- Verify the JSON file is valid and properly formatted\n"
            "- Check for syntax errors, missing brackets, or commas"
        )
    except ValueError as e:
        st.error("❌ **Data Validation Error**")
        st.error(f"Invalid data in the meeting archive: {e}")
        st.info(
            "**How to fix:**\n"
            "- Check that all required fields are present in the JSON\n"
            "- Verify date formats are correct (YYYY-MM-DD)"
        )
    except Exception as e:
        st.error("❌ **Unexpected Error**")
        st.error(f"An unexpected error occurred: {e}")
        st.info(
            "**What to do:**\n"
            "- Try refreshing the page\n"
            "- Check the browser console for more details\n"
            "- If the problem persists, please report this issue"
        )
        with st.expander("Technical Details"):
            st.exception(e)


if __name__ == "__main__":
    main()

