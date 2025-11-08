"""Integration tests for meeting filtering workflow."""

import json
import pytest
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.parsers.data_parser import load_archive
from src.services.filter_service import FilterService


def test_filtering_workflow():
    """Test complete workflow: apply date filter → apply tag filter → combine filters → clear filters."""
    # Create test JSON data
    test_data = [
        {
            "workgroup": "Archives Workgroup",
            "workgroup_id": "05ddaaf0-1dde-4d84-a722-f82c8479a8e9",
            "meetingInfo": {
                "date": "2025-01-08",
                "host": "Stephen [QADAO]",
                "documenter": "CallyFromAuron",
                "peoplePresent": "André, CallyFromAuron",
                "purpose": "Regular monthly meeting",
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
                "date": "2025-02-15",
                "host": "PeterE",
                "documenter": "CallyFromAuron",
                "peoplePresent": "PeterE, CallyFromAuron",
                "purpose": "Weekly meeting",
            },
            "tags": {
                "topicsCovered": "Topic2, Topic3",
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
                "date": "2025-01-20",
                "host": "PeterE",
                "documenter": "CallyFromAuron",
                "peoplePresent": "PeterE, CallyFromAuron",
                "purpose": "Weekly Governance WG meeting",
            },
            "tags": {
                "topicsCovered": "Topic1, Topic3",
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
        # Load data
        meetings = load_archive(temp_path)
        assert len(meetings) == 3

        service = FilterService()

        # Step 1: Apply date filter
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 31)
        date_filtered = service.filter_meetings(
            meetings, start_date=start_date, end_date=end_date
        )
        assert len(date_filtered) == 2
        assert all(start_date <= m.date <= end_date for m in date_filtered)

        # Step 2: Apply tag filter
        tag_filtered = service.filter_meetings(meetings, tags=["Topic1"])
        assert len(tag_filtered) == 2
        assert all("Topic1" in m.topics_covered for m in tag_filtered)

        # Step 3: Combine filters (date + tags)
        combined_filtered = service.filter_meetings(
            meetings,
            start_date=start_date,
            end_date=end_date,
            tags=["Topic1"],
        )
        assert len(combined_filtered) == 1
        assert combined_filtered[0].date == datetime(2025, 1, 8)
        assert "Topic1" in combined_filtered[0].topics_covered

        # Step 4: Clear filters (no filters = all meetings)
        cleared = service.filter_meetings(meetings)
        assert len(cleared) == 3

    finally:
        Path(temp_path).unlink()

