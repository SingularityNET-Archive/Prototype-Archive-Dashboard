"""Contract tests for workgroup service."""

import pytest
from datetime import datetime

from src.models.meeting import Meeting
from src.models.workgroup import Workgroup
from src.services.workgroup_service import WorkgroupService


def test_get_all_workgroups():
    """Test that get_all_workgroups returns unique workgroups."""
    # Create test meetings from different workgroups
    meetings = [
        Meeting(
            id="1",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
        Meeting(
            id="2",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 2),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
        Meeting(
            id="3",
            workgroup="Workgroup B",
            workgroup_id="uuid-2",
            date=datetime(2025, 1, 3),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
    ]

    service = WorkgroupService(meetings)
    workgroups = service.get_all_workgroups()

    assert len(workgroups) == 2
    workgroup_names = [wg.name for wg in workgroups]
    assert "Workgroup A" in workgroup_names
    assert "Workgroup B" in workgroup_names


def test_get_all_workgroups_empty_list():
    """Test that get_all_workgroups returns empty list for no meetings."""
    service = WorkgroupService([])
    workgroups = service.get_all_workgroups()
    assert workgroups == []


def test_get_meetings_by_workgroup():
    """Test that get_meetings_by_workgroup returns correct meetings."""
    meetings = [
        Meeting(
            id="1",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
        Meeting(
            id="2",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 2),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
        Meeting(
            id="3",
            workgroup="Workgroup B",
            workgroup_id="uuid-2",
            date=datetime(2025, 1, 3),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
    ]

    service = WorkgroupService(meetings)
    workgroup_a_meetings = service.get_meetings_by_workgroup("Workgroup A")

    assert len(workgroup_a_meetings) == 2
    assert all(m.workgroup == "Workgroup A" for m in workgroup_a_meetings)


def test_get_meetings_by_workgroup_chronological_newest_first():
    """Test that get_meetings_by_workgroup returns meetings in chronological order (newest first)."""
    meetings = [
        Meeting(
            id="1",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
        Meeting(
            id="2",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 3),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
        Meeting(
            id="3",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 2),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
    ]

    service = WorkgroupService(meetings)
    workgroup_meetings = service.get_meetings_by_workgroup("Workgroup A", sort_order="newest")

    assert len(workgroup_meetings) == 3
    assert workgroup_meetings[0].date == datetime(2025, 1, 3)
    assert workgroup_meetings[1].date == datetime(2025, 1, 2)
    assert workgroup_meetings[2].date == datetime(2025, 1, 1)


def test_get_meetings_by_workgroup_chronological_oldest_first():
    """Test that get_meetings_by_workgroup returns meetings in chronological order (oldest first)."""
    meetings = [
        Meeting(
            id="1",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
        Meeting(
            id="2",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 3),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
        Meeting(
            id="3",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 2),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
    ]

    service = WorkgroupService(meetings)
    workgroup_meetings = service.get_meetings_by_workgroup("Workgroup A", sort_order="oldest")

    assert len(workgroup_meetings) == 3
    assert workgroup_meetings[0].date == datetime(2025, 1, 1)
    assert workgroup_meetings[1].date == datetime(2025, 1, 2)
    assert workgroup_meetings[2].date == datetime(2025, 1, 3)


def test_get_meetings_by_workgroup_nonexistent():
    """Test that get_meetings_by_workgroup returns empty list for nonexistent workgroup."""
    meetings = [
        Meeting(
            id="1",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        ),
    ]

    service = WorkgroupService(meetings)
    workgroup_meetings = service.get_meetings_by_workgroup("Nonexistent Workgroup")

    assert workgroup_meetings == []

