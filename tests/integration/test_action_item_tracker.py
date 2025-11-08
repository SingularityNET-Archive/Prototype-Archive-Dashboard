"""Integration tests for action item tracker workflow."""

import pytest
from datetime import datetime

from src.models.meeting import Meeting
from src.models.action_item import ActionItem
from src.services.aggregation_service import AggregationService
from src.services.filter_service import FilterService


@pytest.fixture
def sample_meetings():
    """Create sample meetings with action items for integration testing."""
    action1 = ActionItem(
        id="a1",
        meeting_id="m1",
        workgroup="Workgroup A",
        date=datetime(2025, 1, 1),
        text="Action 1",
        status="todo",
        assignee="Person A",
        due_date="15 January 2025",
    )
    action2 = ActionItem(
        id="a2",
        meeting_id="m1",
        workgroup="Workgroup A",
        date=datetime(2025, 1, 1),
        text="Action 2",
        status="in progress",
        assignee="Person B",
        due_date="20 January 2025",
    )
    action3 = ActionItem(
        id="a3",
        meeting_id="m2",
        workgroup="Workgroup B",
        date=datetime(2025, 2, 1),
        text="Action 3",
        status="done",
        assignee="Person A",
        due_date="1 February 2025",
    )
    action4 = ActionItem(
        id="a4",
        meeting_id="m3",
        workgroup="Workgroup A",
        date=datetime(2025, 1, 15),
        text="Action 4",
        status="todo",
        assignee=None,
        due_date=None,
    )

    return [
        Meeting(
            id="m1",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            action_items=[action1, action2],
        ),
        Meeting(
            id="m2",
            workgroup="Workgroup B",
            workgroup_id="uuid-2",
            date=datetime(2025, 2, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            action_items=[action3],
        ),
        Meeting(
            id="m3",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            action_items=[action4],
        ),
    ]


def test_action_item_tracker_workflow_aggregate_then_filter(sample_meetings):
    """Test the complete workflow: aggregate action items → filter by assignee/status → display."""
    # Step 1: Aggregate action items
    aggregation_service = AggregationService()
    all_action_items = aggregation_service.aggregate_action_items(sample_meetings)

    assert len(all_action_items) == 4

    # Step 2: Filter by assignee
    filter_service = FilterService()
    filtered_by_assignee = filter_service.filter_action_items(
        all_action_items, assignee="Person A"
    )

    assert len(filtered_by_assignee) == 2
    assert all(a.assignee == "Person A" for a in filtered_by_assignee)

    # Step 3: Filter by status
    filtered_by_status = filter_service.filter_action_items(
        all_action_items, status="todo"
    )

    assert len(filtered_by_status) == 2
    assert all(a.status == "todo" for a in filtered_by_status)


def test_action_item_tracker_workflow_filter_by_assignee(sample_meetings):
    """Test filtering action items by assignee."""
    aggregation_service = AggregationService()
    all_action_items = aggregation_service.aggregate_action_items(sample_meetings)

    filter_service = FilterService()

    # Filter for Person A
    person_a_items = filter_service.filter_action_items(
        all_action_items, assignee="Person A"
    )
    assert len(person_a_items) == 2
    assert all(a.assignee == "Person A" for a in person_a_items)

    # Filter for Person B
    person_b_items = filter_service.filter_action_items(
        all_action_items, assignee="Person B"
    )
    assert len(person_b_items) == 1
    assert person_b_items[0].id == "a2"


def test_action_item_tracker_workflow_filter_by_status(sample_meetings):
    """Test filtering action items by status."""
    aggregation_service = AggregationService()
    all_action_items = aggregation_service.aggregate_action_items(sample_meetings)

    filter_service = FilterService()

    # Filter for todo items
    todo_items = filter_service.filter_action_items(all_action_items, status="todo")
    assert len(todo_items) == 2
    assert all(a.status == "todo" for a in todo_items)

    # Filter for in progress items
    in_progress_items = filter_service.filter_action_items(
        all_action_items, status="in progress"
    )
    assert len(in_progress_items) == 1
    assert in_progress_items[0].id == "a2"

    # Filter for done items
    done_items = filter_service.filter_action_items(all_action_items, status="done")
    assert len(done_items) == 1
    assert done_items[0].id == "a3"


def test_action_item_tracker_workflow_filter_by_date_range(sample_meetings):
    """Test filtering action items by date range."""
    aggregation_service = AggregationService()
    all_action_items = aggregation_service.aggregate_action_items(sample_meetings)

    filter_service = FilterService()

    # Filter by date range
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 31)

    filtered_items = filter_service.filter_action_items(
        all_action_items, start_date=start_date, end_date=end_date
    )

    assert len(filtered_items) == 3
    assert all(start_date <= a.date <= end_date for a in filtered_items)


def test_action_item_tracker_workflow_combined_filters(sample_meetings):
    """Test combining multiple filters (assignee + status + date range)."""
    aggregation_service = AggregationService()
    all_action_items = aggregation_service.aggregate_action_items(sample_meetings)

    filter_service = FilterService()

    # Combine filters: Person A, todo status, within date range
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 31)

    filtered_items = filter_service.filter_action_items(
        all_action_items,
        assignee="Person A",
        status="todo",
        start_date=start_date,
        end_date=end_date,
    )

    # Should match action1 (Person A, todo, within date range)
    assert len(filtered_items) == 1
    assert filtered_items[0].id == "a1"


def test_action_item_tracker_workflow_no_filter(sample_meetings):
    """Test displaying all action items without filtering."""
    aggregation_service = AggregationService()
    all_action_items = aggregation_service.aggregate_action_items(sample_meetings)

    filter_service = FilterService()
    displayed_items = filter_service.filter_action_items(all_action_items)

    assert len(displayed_items) == 4
    assert displayed_items == all_action_items

