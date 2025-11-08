"""Contract tests for aggregation service."""

import pytest
from datetime import datetime

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.services.aggregation_service import AggregationService


@pytest.fixture
def sample_meetings_with_decisions():
    """Create sample meetings with decisions for testing."""
    decision1 = Decision(
        id="d1",
        meeting_id="m1",
        workgroup="Workgroup A",
        date=datetime(2025, 1, 1),
        decision_text="Decision 1",
        effect="affectsOnlyThisWorkgroup",
        rationale="Rationale 1",
    )
    decision2 = Decision(
        id="d2",
        meeting_id="m1",
        workgroup="Workgroup A",
        date=datetime(2025, 1, 1),
        decision_text="Decision 2",
        effect="mayAffectOtherPeople",
    )
    decision3 = Decision(
        id="d3",
        meeting_id="m2",
        workgroup="Workgroup B",
        date=datetime(2025, 2, 1),
        decision_text="Decision 3",
        effect="affectsOnlyThisWorkgroup",
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
            decisions=[decision1, decision2],
        ),
        Meeting(
            id="m2",
            workgroup="Workgroup B",
            workgroup_id="uuid-2",
            date=datetime(2025, 2, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            decisions=[decision3],
        ),
        Meeting(
            id="m3",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            decisions=[],  # Meeting with no decisions
        ),
    ]


@pytest.fixture
def sample_meetings_with_action_items():
    """Create sample meetings with action items for testing."""
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
    )
    action3 = ActionItem(
        id="a3",
        meeting_id="m2",
        workgroup="Workgroup B",
        date=datetime(2025, 2, 1),
        text="Action 3",
        status="done",
        assignee="Person A",
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
            action_items=[],  # Meeting with no action items
        ),
    ]


def test_aggregate_decisions_all_included(sample_meetings_with_decisions):
    """Test that all decisions from all meetings are included in result."""
    service = AggregationService()
    aggregated = service.aggregate_decisions(sample_meetings_with_decisions)

    assert len(aggregated) == 3
    decision_ids = {d.id for d in aggregated}
    assert decision_ids == {"d1", "d2", "d3"}


def test_aggregate_decisions_context_preservation(sample_meetings_with_decisions):
    """Test that decisions include workgroup and date from parent meeting."""
    service = AggregationService()
    aggregated = service.aggregate_decisions(sample_meetings_with_decisions)

    # Check that workgroup and date are preserved
    for decision in aggregated:
        # Find the parent meeting
        parent_meeting = next(
            m for m in sample_meetings_with_decisions if decision.meeting_id == m.id
        )
        assert decision.workgroup == parent_meeting.workgroup
        assert decision.date == parent_meeting.date


def test_aggregate_decisions_empty_meetings():
    """Test that empty meetings list returns empty aggregation list."""
    service = AggregationService()
    aggregated = service.aggregate_decisions([])

    assert aggregated == []


def test_aggregate_decisions_meetings_without_decisions(sample_meetings_with_decisions):
    """Test that meetings without decisions don't cause errors."""
    service = AggregationService()
    aggregated = service.aggregate_decisions(sample_meetings_with_decisions)

    # Should still work and return decisions from meetings that have them
    assert len(aggregated) == 3


def test_aggregate_action_items_all_included(sample_meetings_with_action_items):
    """Test that all action items from all meetings are included in result."""
    service = AggregationService()
    aggregated = service.aggregate_action_items(sample_meetings_with_action_items)

    assert len(aggregated) == 3
    action_ids = {a.id for a in aggregated}
    assert action_ids == {"a1", "a2", "a3"}


def test_aggregate_action_items_context_preservation(sample_meetings_with_action_items):
    """Test that action items include workgroup and date from parent meeting."""
    service = AggregationService()
    aggregated = service.aggregate_action_items(sample_meetings_with_action_items)

    # Check that workgroup and date are preserved
    for action in aggregated:
        # Find the parent meeting
        parent_meeting = next(
            m for m in sample_meetings_with_action_items if action.meeting_id == m.id
        )
        assert action.workgroup == parent_meeting.workgroup
        assert action.date == parent_meeting.date


def test_aggregate_action_items_empty_meetings():
    """Test that empty meetings list returns empty aggregation list."""
    service = AggregationService()
    aggregated = service.aggregate_action_items([])

    assert aggregated == []


def test_aggregate_action_items_meetings_without_action_items(
    sample_meetings_with_action_items
):
    """Test that meetings without action items don't cause errors."""
    service = AggregationService()
    aggregated = service.aggregate_action_items(sample_meetings_with_action_items)

    # Should still work and return action items from meetings that have them
    assert len(aggregated) == 3


def test_aggregate_decisions_performance():
    """Test that aggregating 10,000 meetings completes in < 5 seconds (SC-004)."""
    import time

    service = AggregationService()
    # Create 10,000 meetings with decisions
    meetings = []
    for i in range(10000):
        decision = Decision(
            id=f"d{i}",
            meeting_id=f"m{i}",
            workgroup=f"Workgroup {i % 10}",
            date=datetime(2025, 1, 1),
            decision_text=f"Decision {i}",
            effect="affectsOnlyThisWorkgroup",
        )
        meeting = Meeting(
            id=f"m{i}",
            workgroup=f"Workgroup {i % 10}",
            workgroup_id=f"uuid-{i}",
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            decisions=[decision],
        )
        meetings.append(meeting)

    start_time = time.time()
    aggregated = service.aggregate_decisions(meetings)
    elapsed_time = time.time() - start_time

    assert len(aggregated) == 10000
    assert elapsed_time < 5.0, f"Aggregation took {elapsed_time:.2f} seconds, expected < 5 seconds"

