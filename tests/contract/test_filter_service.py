"""Contract tests for filter service."""

import pytest
from datetime import datetime

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.services.filter_service import FilterService


@pytest.fixture
def sample_meetings():
    """Create sample meetings for testing."""
    return [
        Meeting(
            id="1",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            topics_covered=["Topic1", "Topic2"],
        ),
        Meeting(
            id="2",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            topics_covered=["Topic2", "Topic3"],
        ),
        Meeting(
            id="3",
            workgroup="Workgroup B",
            workgroup_id="uuid-2",
            date=datetime(2025, 2, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            topics_covered=["Topic1", "Topic3"],
        ),
    ]


def test_workgroup_filter(sample_meetings):
    """Test that filter by workgroup returns only meetings from that workgroup."""
    service = FilterService()
    filtered = service.filter_meetings(sample_meetings, workgroup="Workgroup A")

    assert len(filtered) == 2
    assert all(m.workgroup == "Workgroup A" for m in filtered)


def test_date_range_filter(sample_meetings):
    """Test that filter by date range returns only meetings within range (inclusive)."""
    service = FilterService()
    start_date = datetime(2025, 1, 10)
    end_date = datetime(2025, 1, 20)

    filtered = service.filter_meetings(
        sample_meetings, start_date=start_date, end_date=end_date
    )

    assert len(filtered) == 1
    assert filtered[0].date == datetime(2025, 1, 15)


def test_date_range_filter_inclusive(sample_meetings):
    """Test that date range filter is inclusive of start and end dates."""
    service = FilterService()
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 1)

    filtered = service.filter_meetings(
        sample_meetings, start_date=start_date, end_date=end_date
    )

    assert len(filtered) == 1
    assert filtered[0].date == datetime(2025, 1, 1)


def test_tag_filter(sample_meetings):
    """Test that filter by tags returns only meetings containing at least one of the tags."""
    service = FilterService()
    filtered = service.filter_meetings(sample_meetings, tags=["Topic1"])

    assert len(filtered) == 2
    assert all("Topic1" in m.topics_covered for m in filtered)


def test_tag_filter_multiple_tags(sample_meetings):
    """Test that filter with multiple tags returns meetings containing any of the tags."""
    service = FilterService()
    filtered = service.filter_meetings(sample_meetings, tags=["Topic1", "Topic3"])

    assert len(filtered) == 3  # All meetings have Topic1 or Topic3


def test_combined_filters(sample_meetings):
    """Test that multiple filters applied with AND logic (all criteria must match)."""
    service = FilterService()
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 31)

    filtered = service.filter_meetings(
        sample_meetings,
        workgroup="Workgroup A",
        start_date=start_date,
        end_date=end_date,
        tags=["Topic2"],
    )

    assert len(filtered) == 2
    assert all(m.workgroup == "Workgroup A" for m in filtered)
    assert all("Topic2" in m.topics_covered for m in filtered)
    assert all(start_date <= m.date <= end_date for m in filtered)


def test_empty_results(sample_meetings):
    """Test that filtering with no matches returns empty list (no errors)."""
    service = FilterService()
    filtered = service.filter_meetings(
        sample_meetings, workgroup="Nonexistent Workgroup"
    )

    assert filtered == []


def test_no_filters(sample_meetings):
    """Test that calling with no filter parameters returns all items."""
    service = FilterService()
    filtered = service.filter_meetings(sample_meetings)

    assert len(filtered) == len(sample_meetings)
    assert filtered == sample_meetings


def test_tag_filter_case_insensitive(sample_meetings):
    """Test that tag filtering is case-insensitive for matching."""
    service = FilterService()
    # Topics are stored with original case, but matching should be case-insensitive
    filtered = service.filter_meetings(sample_meetings, tags=["topic1"])

    # Should match meetings with "Topic1" (case-insensitive)
    assert len(filtered) == 2


def test_date_range_only_start(sample_meetings):
    """Test filtering with only start date (no end date)."""
    service = FilterService()
    start_date = datetime(2025, 1, 15)

    filtered = service.filter_meetings(sample_meetings, start_date=start_date)

    assert len(filtered) == 2
    assert all(m.date >= start_date for m in filtered)


def test_date_range_only_end(sample_meetings):
    """Test filtering with only end date (no start date)."""
    service = FilterService()
    end_date = datetime(2025, 1, 15)

    filtered = service.filter_meetings(sample_meetings, end_date=end_date)

    assert len(filtered) == 2
    assert all(m.date <= end_date for m in filtered)


# Decision filtering tests (T039)
@pytest.fixture
def sample_decisions():
    """Create sample decisions for testing."""
    return [
        Decision(
            id="d1",
            meeting_id="m1",
            workgroup="Workgroup A",
            date=datetime(2025, 1, 1),
            decision_text="Decision 1",
            effect="affectsOnlyThisWorkgroup",
        ),
        Decision(
            id="d2",
            meeting_id="m2",
            workgroup="Workgroup A",
            date=datetime(2025, 1, 15),
            decision_text="Decision 2",
            effect="mayAffectOtherPeople",
        ),
        Decision(
            id="d3",
            meeting_id="m3",
            workgroup="Workgroup B",
            date=datetime(2025, 2, 1),
            decision_text="Decision 3",
            effect="affectsOnlyThisWorkgroup",
        ),
    ]


def test_filter_decisions_by_workgroup(sample_decisions):
    """Test that filter_decisions by workgroup returns only decisions from that workgroup."""
    service = FilterService()
    filtered = service.filter_decisions(sample_decisions, workgroup="Workgroup A")

    assert len(filtered) == 2
    assert all(d.workgroup == "Workgroup A" for d in filtered)


def test_filter_decisions_no_filter(sample_decisions):
    """Test that filter_decisions with no filter returns all decisions."""
    service = FilterService()
    filtered = service.filter_decisions(sample_decisions)

    assert len(filtered) == len(sample_decisions)
    assert filtered == sample_decisions


def test_filter_decisions_empty_results(sample_decisions):
    """Test that filter_decisions with no matches returns empty list."""
    service = FilterService()
    filtered = service.filter_decisions(sample_decisions, workgroup="Nonexistent")

    assert filtered == []


# Action item filtering tests (T039)
@pytest.fixture
def sample_action_items():
    """Create sample action items for testing."""
    return [
        ActionItem(
            id="a1",
            meeting_id="m1",
            workgroup="Workgroup A",
            date=datetime(2025, 1, 1),
            text="Action 1",
            status="todo",
            assignee="Person A",
            due_date="15 January 2025",
        ),
        ActionItem(
            id="a2",
            meeting_id="m2",
            workgroup="Workgroup A",
            date=datetime(2025, 1, 15),
            text="Action 2",
            status="in progress",
            assignee="Person B",
            due_date="20 January 2025",
        ),
        ActionItem(
            id="a3",
            meeting_id="m3",
            workgroup="Workgroup B",
            date=datetime(2025, 2, 1),
            text="Action 3",
            status="done",
            assignee="Person A",
            due_date="1 February 2025",
        ),
        ActionItem(
            id="a4",
            meeting_id="m4",
            workgroup="Workgroup B",
            date=datetime(2025, 2, 15),
            text="Action 4",
            status="todo",
            assignee=None,
            due_date=None,
        ),
    ]


def test_filter_action_items_by_assignee(sample_action_items):
    """Test that filter_action_items by assignee returns only items assigned to that person."""
    service = FilterService()
    filtered = service.filter_action_items(sample_action_items, assignee="Person A")

    assert len(filtered) == 2
    assert all(a.assignee == "Person A" for a in filtered)


def test_filter_action_items_by_status(sample_action_items):
    """Test that filter_action_items by status returns only items with that status."""
    service = FilterService()
    filtered = service.filter_action_items(sample_action_items, status="todo")

    assert len(filtered) == 2
    assert all(a.status == "todo" for a in filtered)


def test_filter_action_items_by_date_range(sample_action_items):
    """Test that filter_action_items by date range returns only items within range."""
    service = FilterService()
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 31)

    filtered = service.filter_action_items(
        sample_action_items, start_date=start_date, end_date=end_date
    )

    assert len(filtered) == 2
    assert all(start_date <= a.date <= end_date for a in filtered)


def test_filter_action_items_combined(sample_action_items):
    """Test that filter_action_items with multiple filters uses AND logic."""
    service = FilterService()
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 31)

    filtered = service.filter_action_items(
        sample_action_items,
        assignee="Person A",
        status="todo",
        start_date=start_date,
        end_date=end_date,
    )

    assert len(filtered) == 1
    assert filtered[0].id == "a1"


def test_filter_action_items_no_filter(sample_action_items):
    """Test that filter_action_items with no filter returns all items."""
    service = FilterService()
    filtered = service.filter_action_items(sample_action_items)

    assert len(filtered) == len(sample_action_items)
    assert filtered == sample_action_items


def test_filter_action_items_empty_results(sample_action_items):
    """Test that filter_action_items with no matches returns empty list."""
    service = FilterService()
    filtered = service.filter_action_items(sample_action_items, assignee="Nonexistent")

    assert filtered == []


def test_filter_action_items_no_assignee(sample_action_items):
    """Test filtering action items with no assignee."""
    service = FilterService()
    # Filter for items with no assignee (None)
    # This is a special case - we need to handle None assignees
    all_items = service.filter_action_items(sample_action_items)
    items_without_assignee = [a for a in all_items if a.assignee is None]

    assert len(items_without_assignee) == 1
    assert items_without_assignee[0].id == "a4"

