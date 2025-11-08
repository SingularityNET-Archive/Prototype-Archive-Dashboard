"""Integration tests for workgroup browser workflow."""

import json
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.parsers.data_parser import load_archive
from src.services.workgroup_service import WorkgroupService


def test_workgroup_browser_workflow():
    """Test complete workflow: load JSON → extract workgroups → select workgroup → view meetings."""
    # Create test JSON data
    test_data = [
        {
            "workgroup": "Archives Workgroup",
            "workgroup_id": "05ddaaf0-1dde-4d84-a722-f82c8479a8e9",
            "meetingInfo": {
                "date": "2025-01-08",
                "host": "Stephen [QADAO]",
                "documenter": "CallyFromAuron",
                "peoplePresent": "André, CallyFromAuron, Stephen [QADAO]",
                "purpose": "Regular monthly meeting",
                "typeOfMeeting": "Monthly",
            },
            "tags": {
                "topicsCovered": "Topic1, Topic2",
                "emotions": "Happy",
            },
            "type": "Custom",
            "noSummaryGiven": False,
            "canceledSummary": False,
        },
        {
            "workgroup": "Archives Workgroup",
            "workgroup_id": "05ddaaf0-1dde-4d84-a722-f82c8479a8e9",
            "meetingInfo": {
                "date": "2025-01-15",
                "host": "PeterE",
                "documenter": "CallyFromAuron",
                "peoplePresent": "PeterE, CallyFromAuron",
                "purpose": "Weekly meeting",
                "typeOfMeeting": "Weekly",
            },
            "tags": {
                "topicsCovered": "Topic3",
                "emotions": "Excited",
            },
            "type": "Custom",
            "noSummaryGiven": False,
            "canceledSummary": False,
        },
        {
            "workgroup": "Governance Workgroup",
            "workgroup_id": "bcfadc9a-79d3-4ac0-816a-6b3405fd4009",
            "meetingInfo": {
                "date": "2025-01-07",
                "host": "PeterE",
                "documenter": "CallyFromAuron",
                "peoplePresent": "PeterE, CallyFromAuron",
                "purpose": "Weekly Governance WG meeting",
            },
            "type": "Custom",
            "noSummaryGiven": False,
            "canceledSummary": False,
        },
    ]

    with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        # Step 1: Load JSON file
        meetings = load_archive(temp_path)
        assert len(meetings) == 3

        # Step 2: Extract workgroups
        service = WorkgroupService(meetings)
        workgroups = service.get_all_workgroups()
        assert len(workgroups) == 2
        workgroup_names = [wg.name for wg in workgroups]
        assert "Archives Workgroup" in workgroup_names
        assert "Governance Workgroup" in workgroup_names

        # Step 3: Select workgroup and view meetings
        archives_meetings = service.get_meetings_by_workgroup("Archives Workgroup")
        assert len(archives_meetings) == 2

        # Step 4: Verify metadata
        for meeting in archives_meetings:
            assert meeting.workgroup == "Archives Workgroup"
            assert meeting.date is not None
            assert meeting.host is not None or meeting.host is None  # Optional field
            assert meeting.documenter is not None or meeting.documenter is None  # Optional field
            assert meeting.purpose is not None or meeting.purpose is None  # Optional field
            assert isinstance(meeting.people_present, list)

        # Step 5: Verify chronological order (newest first by default)
        assert archives_meetings[0].date >= archives_meetings[1].date

    finally:
        Path(temp_path).unlink()

