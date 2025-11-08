"""Integration tests for decision tracker workflow."""

import pytest
from datetime import datetime

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.services.aggregation_service import AggregationService
from src.services.filter_service import FilterService


@pytest.fixture
def sample_meetings():
    """Create sample meetings with decisions for integration testing."""
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
    ]


def test_decision_tracker_workflow_aggregate_then_filter(sample_meetings):
    """Test the complete workflow: aggregate decisions → filter by workgroup → display."""
    # Step 1: Aggregate decisions
    aggregation_service = AggregationService()
    all_decisions = aggregation_service.aggregate_decisions(sample_meetings)

    assert len(all_decisions) == 3

    # Step 2: Filter by workgroup
    filter_service = FilterService()
    filtered_decisions = filter_service.filter_decisions(
        all_decisions, workgroup="Workgroup A"
    )

    assert len(filtered_decisions) == 2
    assert all(d.workgroup == "Workgroup A" for d in filtered_decisions)

    # Step 3: Verify decisions have correct context
    for decision in filtered_decisions:
        assert decision.workgroup == "Workgroup A"
        assert decision.date == datetime(2025, 1, 1)
        assert decision.meeting_id in ["m1"]


def test_decision_tracker_workflow_multiple_workgroups(sample_meetings):
    """Test filtering decisions from multiple workgroups."""
    aggregation_service = AggregationService()
    all_decisions = aggregation_service.aggregate_decisions(sample_meetings)

    filter_service = FilterService()

    # Filter for Workgroup A
    wg_a_decisions = filter_service.filter_decisions(
        all_decisions, workgroup="Workgroup A"
    )
    assert len(wg_a_decisions) == 2

    # Filter for Workgroup B
    wg_b_decisions = filter_service.filter_decisions(
        all_decisions, workgroup="Workgroup B"
    )
    assert len(wg_b_decisions) == 1
    assert wg_b_decisions[0].id == "d3"


def test_decision_tracker_workflow_no_filter(sample_meetings):
    """Test displaying all decisions without filtering."""
    aggregation_service = AggregationService()
    all_decisions = aggregation_service.aggregate_decisions(sample_meetings)

    filter_service = FilterService()
    displayed_decisions = filter_service.filter_decisions(all_decisions)

    assert len(displayed_decisions) == 3
    assert displayed_decisions == all_decisions

