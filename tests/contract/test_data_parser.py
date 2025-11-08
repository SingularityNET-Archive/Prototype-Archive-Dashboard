"""Contract tests for data parser service."""

import json
import pytest
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.parsers.data_parser import load_archive, normalize_meeting
from src.models.meeting import Meeting


def test_valid_json_parsing():
    """Test that valid JSON file returns list of Meeting objects."""
    # Create a temporary JSON file with valid meeting data
    valid_meeting = {
        "workgroup": "Test Workgroup",
        "workgroup_id": "123e4567-e89b-12d3-a456-426614174000",
        "meetingInfo": {
            "date": "2025-01-08",
            "host": "Test Host",
            "documenter": "Test Documenter",
            "peoplePresent": "Alice, Bob, Charlie",
            "purpose": "Test meeting",
            "typeOfMeeting": "Monthly",
        },
        "tags": {
            "topicsCovered": "Topic1, Topic2",
            "emotions": "Happy, Excited",
        },
        "type": "Custom",
        "noSummaryGiven": False,
        "canceledSummary": False,
    }

    with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([valid_meeting], f)
        temp_path = f.name

    try:
        meetings = load_archive(temp_path)
        assert isinstance(meetings, list)
        assert len(meetings) == 1
        assert isinstance(meetings[0], Meeting)
        assert meetings[0].workgroup == "Test Workgroup"
    finally:
        Path(temp_path).unlink()


def test_missing_optional_fields():
    """Test that missing optional fields are handled gracefully."""
    minimal_meeting = {
        "workgroup": "Test Workgroup",
        "workgroup_id": "123e4567-e89b-12d3-a456-426614174000",
        "meetingInfo": {
            "date": "2025-01-08",
        },
        "type": "Custom",
        "noSummaryGiven": False,
        "canceledSummary": False,
    }

    meeting = normalize_meeting(minimal_meeting, 0)
    assert meeting.host is None
    assert meeting.documenter is None
    assert meeting.people_present == []
    assert meeting.topics_covered == []
    assert meeting.emotions == []
    assert meeting.action_items == []
    assert meeting.decisions == []


def test_date_parsing():
    """Test that ISO dates are parsed correctly to datetime objects."""
    meeting_data = {
        "workgroup": "Test Workgroup",
        "workgroup_id": "123e4567-e89b-12d3-a456-426614174000",
        "meetingInfo": {
            "date": "2025-01-08",
        },
        "type": "Custom",
        "noSummaryGiven": False,
        "canceledSummary": False,
    }

    meeting = normalize_meeting(meeting_data, 0)
    assert isinstance(meeting.date, datetime)
    assert meeting.date.year == 2025
    assert meeting.date.month == 1
    assert meeting.date.day == 8


def test_string_parsing():
    """Test that comma-separated strings are parsed to lists."""
    meeting_data = {
        "workgroup": "Test Workgroup",
        "workgroup_id": "123e4567-e89b-12d3-a456-426614174000",
        "meetingInfo": {
            "date": "2025-01-08",
            "peoplePresent": "Alice, Bob, Charlie",
        },
        "tags": {
            "topicsCovered": "Topic1, Topic2, Topic3",
            "emotions": "Happy, Excited",
        },
        "type": "Custom",
        "noSummaryGiven": False,
        "canceledSummary": False,
    }

    meeting = normalize_meeting(meeting_data, 0)
    assert isinstance(meeting.people_present, list)
    assert len(meeting.people_present) == 3
    assert "Alice" in meeting.people_present
    assert "Bob" in meeting.people_present
    assert "Charlie" in meeting.people_present

    assert isinstance(meeting.topics_covered, list)
    assert len(meeting.topics_covered) == 3
    assert "Topic1" in meeting.topics_covered
    assert "Topic2" in meeting.topics_covered
    assert "Topic3" in meeting.topics_covered


def test_name_normalization():
    """Test that name variations are handled consistently."""
    meeting_data = {
        "workgroup": "Test Workgroup",
        "workgroup_id": "123e4567-e89b-12d3-a456-426614174000",
        "meetingInfo": {
            "date": "2025-01-08",
            "host": "Stephen [QADAO]",
            "documenter": "CallyFromAuron",
            "peoplePresent": "Alice,  Bob  , Charlie",
        },
        "type": "Custom",
        "noSummaryGiven": False,
        "canceledSummary": False,
    }

    meeting = normalize_meeting(meeting_data, 0)
    assert meeting.host == "Stephen [QADAO]"
    assert meeting.documenter == "CallyFromAuron"
    # Names should be trimmed
    assert "Bob" in meeting.people_present
    assert "  Bob  " not in meeting.people_present


def test_error_handling_malformed_meeting():
    """Test that malformed meetings are logged and skipped."""
    valid_meeting = {
        "workgroup": "Test Workgroup",
        "workgroup_id": "123e4567-e89b-12d3-a456-426614174000",
        "meetingInfo": {
            "date": "2025-01-08",
        },
        "type": "Custom",
        "noSummaryGiven": False,
        "canceledSummary": False,
    }

    malformed_meeting = {
        "workgroup": "Missing Workgroup",
        # Missing workgroup_id and other required fields
    }

    with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([valid_meeting, malformed_meeting], f)
        temp_path = f.name

    try:
        meetings = load_archive(temp_path)
        # Should only have the valid meeting
        assert len(meetings) == 1
        assert meetings[0].workgroup == "Test Workgroup"
    finally:
        Path(temp_path).unlink()


def test_attribution_preservation():
    """Test that host and documenter fields are preserved."""
    meeting_data = {
        "workgroup": "Test Workgroup",
        "workgroup_id": "123e4567-e89b-12d3-a456-426614174000",
        "meetingInfo": {
            "date": "2025-01-08",
            "host": "Test Host",
            "documenter": "Test Documenter",
        },
        "type": "Custom",
        "noSummaryGiven": False,
        "canceledSummary": False,
    }

    meeting = normalize_meeting(meeting_data, 0)
    assert meeting.host == "Test Host"
    assert meeting.documenter == "Test Documenter"


def test_file_not_found_error():
    """Test that FileNotFoundError is raised for non-existent files."""
    with pytest.raises(FileNotFoundError):
        load_archive("nonexistent_file.json")


def test_invalid_json_error():
    """Test that json.JSONDecodeError is raised for malformed JSON."""
    with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("invalid json content")
        temp_path = f.name

    try:
        with pytest.raises(json.JSONDecodeError):
            load_archive(temp_path)
    finally:
        Path(temp_path).unlink()


def test_missing_required_fields():
    """Test that ValueError is raised for missing required fields."""
    meeting_data = {
        # Missing workgroup
        "workgroup_id": "123e4567-e89b-12d3-a456-426614174000",
        "meetingInfo": {
            "date": "2025-01-08",
        },
        "type": "Custom",
        "noSummaryGiven": False,
        "canceledSummary": False,
    }

    with pytest.raises(ValueError, match="Missing required field: workgroup"):
        normalize_meeting(meeting_data, 0)

