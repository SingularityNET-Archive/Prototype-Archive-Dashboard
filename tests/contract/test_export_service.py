"""Contract tests for export service."""

import pytest
from datetime import datetime
import json
import csv
import io

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.services.export_service import ExportService


@pytest.fixture
def sample_meetings():
    """Create sample meetings for testing."""
    return [
        Meeting(
            id="m1",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            host="Person A",
            documenter="Person B",
            purpose="Test meeting",
            people_present=["Person A", "Person B"],
            topics_covered=["Topic1", "Topic2"],
        ),
    ]


@pytest.fixture
def sample_decisions():
    """Create sample decisions for testing."""
    return [
        Decision(
            id="d1",
            meeting_id="m1",
            workgroup="Workgroup A",
            date=datetime(2025, 1, 1),
            decision_text="Test decision",
            effect="affectsOnlyThisWorkgroup",
            rationale="Test rationale",
        ),
    ]


@pytest.fixture
def sample_action_items():
    """Create sample action items for testing."""
    return [
        ActionItem(
            id="a1",
            meeting_id="m1",
            workgroup="Workgroup A",
            date=datetime(2025, 1, 1),
            text="Test action",
            status="todo",
            assignee="Person A",
            due_date="2025-02-01",
        ),
    ]


def test_export_meetings_plain_text(sample_meetings):
    """Test that meetings are exported with all fields, tab-separated."""
    service = ExportService()
    result = service.export_meetings_plain_text(sample_meetings)

    assert isinstance(result, str)
    assert len(result) > 0
    lines = result.split("\n")
    assert len(lines) == 2  # Header + 1 data row
    assert "ID" in lines[0]  # Header
    assert "m1" in lines[1]  # Data


def test_export_meetings_plain_text_attribution(sample_meetings):
    """Test that attribution (host, documenter) is preserved in export."""
    service = ExportService()
    result = service.export_meetings_plain_text(sample_meetings)

    assert "Person A" in result  # Host
    assert "Person B" in result  # Documenter


def test_export_decisions_plain_text(sample_decisions):
    """Test that decisions are exported with all fields, tab-separated."""
    service = ExportService()
    result = service.export_decisions_plain_text(sample_decisions)

    assert isinstance(result, str)
    assert len(result) > 0
    lines = result.split("\n")
    assert len(lines) == 2  # Header + 1 data row
    assert "Decision Text" in lines[0]  # Header
    assert "Test decision" in lines[1]  # Data


def test_export_action_items_plain_text(sample_action_items):
    """Test that action items are exported with all fields, tab-separated."""
    service = ExportService()
    result = service.export_action_items_plain_text(sample_action_items)

    assert isinstance(result, str)
    assert len(result) > 0
    lines = result.split("\n")
    assert len(lines) == 2  # Header + 1 data row
    assert "Text" in lines[0]  # Header
    assert "Test action" in lines[1]  # Data


def test_export_to_csv_meetings(sample_meetings):
    """Test that CSV export works for meetings."""
    service = ExportService()
    csv_bytes = service.export_to_csv(sample_meetings, data_type="meetings")

    assert isinstance(csv_bytes, bytes)
    assert len(csv_bytes) > 0

    # Verify it's valid CSV
    csv_string = csv_bytes.decode("utf-8")
    reader = csv.reader(io.StringIO(csv_string))
    rows = list(reader)
    assert len(rows) == 2  # Header + 1 data row
    assert "ID" in rows[0]


def test_export_to_csv_decisions(sample_decisions):
    """Test that CSV export works for decisions."""
    service = ExportService()
    csv_bytes = service.export_to_csv(sample_decisions, data_type="decisions")

    assert isinstance(csv_bytes, bytes)
    assert len(csv_bytes) > 0

    # Verify it's valid CSV
    csv_string = csv_bytes.decode("utf-8")
    reader = csv.reader(io.StringIO(csv_string))
    rows = list(reader)
    assert len(rows) == 2  # Header + 1 data row


def test_export_to_csv_action_items(sample_action_items):
    """Test that CSV export works for action items."""
    service = ExportService()
    csv_bytes = service.export_to_csv(sample_action_items, data_type="action_items")

    assert isinstance(csv_bytes, bytes)
    assert len(csv_bytes) > 0

    # Verify it's valid CSV
    csv_string = csv_bytes.decode("utf-8")
    reader = csv.reader(io.StringIO(csv_string))
    rows = list(reader)
    assert len(rows) == 2  # Header + 1 data row


def test_export_to_json_meetings(sample_meetings):
    """Test that JSON export works for meetings."""
    service = ExportService()
    json_string = service.export_to_json(sample_meetings)

    assert isinstance(json_string, str)
    assert len(json_string) > 0

    # Verify it's valid JSON
    data = json.loads(json_string)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == "m1"
    assert data[0]["host"] == "Person A"  # Attribution preserved


def test_export_to_json_decisions(sample_decisions):
    """Test that JSON export works for decisions."""
    service = ExportService()
    json_string = service.export_to_json(sample_decisions)

    assert isinstance(json_string, str)
    assert len(json_string) > 0

    # Verify it's valid JSON
    data = json.loads(json_string)
    assert isinstance(data, list)
    assert len(data) == 1


def test_export_to_json_action_items(sample_action_items):
    """Test that JSON export works for action items."""
    service = ExportService()
    json_string = service.export_to_json(sample_action_items)

    assert isinstance(json_string, str)
    assert len(json_string) > 0

    # Verify it's valid JSON
    data = json.loads(json_string)
    assert isinstance(data, list)
    assert len(data) == 1


def test_export_empty_data():
    """Test that exporting empty lists returns empty file (no errors)."""
    service = ExportService()

    # Test all export methods with empty data
    assert service.export_meetings_plain_text([]) == ""
    assert service.export_decisions_plain_text([]) == ""
    assert service.export_action_items_plain_text([]) == ""
    assert service.export_to_csv([], "meetings") == b""
    assert service.export_to_json([]) == "[]"


def test_export_special_characters():
    """Test that special characters in data are handled correctly in exports."""
    service = ExportService()

    # Create meeting with special characters
    meeting = Meeting(
        id="m1",
        workgroup="Workgroup A",
        workgroup_id="uuid-1",
        date=datetime(2025, 1, 1),
        type="Custom",
        no_summary_given=False,
        canceled_summary=False,
        purpose="Test with\ttabs\nand newlines & special chars",
        host="Person A",
    )

    # Test plain text export
    plain_text = service.export_meetings_plain_text([meeting])
    assert "Test with" in plain_text
    # Tabs and newlines in the data should be replaced with spaces
    # (tabs are used as separators, so they'll be in the row, but the actual data shouldn't have tabs)
    data_row = plain_text.split("\n")[1]
    # The purpose field should have tabs/newlines replaced
    assert "\n" not in data_row  # Newlines should be replaced
    # Check that the purpose text is present but without newlines
    assert "tabs" in data_row and "newlines" in data_row

    # Test CSV export
    csv_bytes = service.export_to_csv([meeting], "meetings")
    csv_string = csv_bytes.decode("utf-8")
    assert "Test with" in csv_string

    # Test JSON export
    json_string = service.export_to_json([meeting])
    data = json.loads(json_string)
    assert "Test with" in data[0]["purpose"]


def test_export_attribution_preservation(sample_meetings):
    """Test that attribution (host, documenter) is preserved in all export formats."""
    service = ExportService()

    # Plain text
    plain_text = service.export_meetings_plain_text(sample_meetings)
    assert "Person A" in plain_text  # Host
    assert "Person B" in plain_text  # Documenter

    # CSV
    csv_bytes = service.export_to_csv(sample_meetings, "meetings")
    csv_string = csv_bytes.decode("utf-8")
    assert "Person A" in csv_string
    assert "Person B" in csv_string

    # JSON
    json_string = service.export_to_json(sample_meetings)
    data = json.loads(json_string)
    assert data[0]["host"] == "Person A"
    assert data[0]["documenter"] == "Person B"

