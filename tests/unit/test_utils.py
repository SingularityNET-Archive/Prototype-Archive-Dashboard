"""Unit tests for utility functions."""

import pytest
from datetime import datetime
from src.utils.date_parser import parse_date, parse_optional_date
from src.utils.text_normalizer import (
    parse_comma_separated_string,
    normalize_name,
    normalize_topic,
    normalize_topics,
)
from src.utils.topic_extractor import extract_all_topics, extract_topics_normalized
from src.utils.person_extractor import extract_all_people, get_people_list
from src.models.meeting import Meeting
from src.models.person import Person


class TestDateParser:
    """Test date parsing utilities."""

    def test_parse_date_iso_format(self):
        """Test parsing ISO format date string."""
        date = parse_date("2024-01-15")
        assert isinstance(date, datetime)
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15

    def test_parse_date_flexible_format(self):
        """Test parsing flexible date format."""
        date = parse_date("January 15, 2024")
        assert isinstance(date, datetime)
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15

    def test_parse_date_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Date string cannot be empty"):
            parse_date("")

    def test_parse_optional_date_with_value(self):
        """Test parse_optional_date with a value."""
        date = parse_optional_date("2024-01-15")
        assert isinstance(date, datetime)
        assert date.year == 2024

    def test_parse_optional_date_none(self):
        """Test parse_optional_date with None."""
        assert parse_optional_date(None) is None

    def test_parse_optional_date_empty_string(self):
        """Test parse_optional_date with empty string."""
        assert parse_optional_date("") is None


class TestTextNormalizer:
    """Test text normalization utilities."""

    def test_parse_comma_separated_string(self):
        """Test parsing comma-separated string."""
        result = parse_comma_separated_string("Alice, Bob, Charlie")
        assert result == ["Alice", "Bob", "Charlie"]

    def test_parse_comma_separated_string_with_spaces(self):
        """Test parsing with extra spaces."""
        result = parse_comma_separated_string("Alice , Bob , Charlie ")
        assert result == ["Alice", "Bob", "Charlie"]

    def test_parse_comma_separated_string_empty(self):
        """Test parsing empty string."""
        result = parse_comma_separated_string("")
        assert result == []

    def test_parse_comma_separated_string_none(self):
        """Test parsing None."""
        result = parse_comma_separated_string(None)
        assert result == []

    def test_normalize_name(self):
        """Test name normalization."""
        assert normalize_name("John Doe") == "John Doe"
        assert normalize_name("  John Doe  ") == "John Doe"
        assert normalize_name("John [QADAO]") == "John [QADAO]"

    def test_normalize_name_empty(self):
        """Test normalizing empty name."""
        assert normalize_name("") == ""
        assert normalize_name(None) == ""

    def test_normalize_topic(self):
        """Test topic normalization."""
        assert normalize_topic("Test Topic") == "test topic"
        assert normalize_topic("  TEST TOPIC  ") == "test topic"
        assert normalize_topic("Mixed Case Topic") == "mixed case topic"

    def test_normalize_topic_empty(self):
        """Test normalizing empty topic."""
        assert normalize_topic("") == ""
        assert normalize_topic(None) == ""

    def test_normalize_topics(self):
        """Test normalizing list of topics."""
        topics = ["Topic One", "Topic Two", "  Topic Three  "]
        normalized = normalize_topics(topics)
        assert normalized == ["topic one", "topic two", "topic three"]

    def test_normalize_topics_with_empty(self):
        """Test normalizing topics list with empty strings."""
        topics = ["Topic One", "", "  ", "Topic Two"]
        normalized = normalize_topics(topics)
        assert normalized == ["topic one", "topic two"]


class TestTopicExtractor:
    """Test topic extraction utilities."""

    def test_extract_all_topics(self):
        """Test extracting all unique topics from meetings."""
        meeting1 = Meeting(
            id="m1",
            workgroup="WG",
            workgroup_id="wg-1",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            topics_covered=["Topic A", "Topic B"],
        )
        meeting2 = Meeting(
            id="m2",
            workgroup="WG",
            workgroup_id="wg-1",
            date=datetime(2024, 2, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            topics_covered=["Topic B", "Topic C"],
        )
        topics = extract_all_topics([meeting1, meeting2])
        assert len(topics) == 3
        assert "Topic A" in topics
        assert "Topic B" in topics
        assert "Topic C" in topics
        # Should be sorted
        assert topics == sorted(topics)

    def test_extract_all_topics_empty(self):
        """Test extracting topics from empty meeting list."""
        topics = extract_all_topics([])
        assert topics == []

    def test_extract_all_topics_no_topics(self):
        """Test extracting topics from meetings with no topics."""
        meeting = Meeting(
            id="m1",
            workgroup="WG",
            workgroup_id="wg-1",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        )
        topics = extract_all_topics([meeting])
        assert topics == []

    def test_extract_topics_normalized(self):
        """Test extracting normalized topics."""
        meeting1 = Meeting(
            id="m1",
            workgroup="WG",
            workgroup_id="wg-1",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            topics_covered=["Topic A", "topic a"],
        )
        normalized = extract_topics_normalized([meeting1])
        # Should normalize to lowercase and deduplicate
        assert "topic a" in normalized
        assert len(normalized) == 1  # Duplicates removed


class TestPersonExtractor:
    """Test person extraction utilities."""

    def test_extract_all_people(self):
        """Test extracting all people from meetings."""
        meeting = Meeting(
            id="m1",
            workgroup="WG",
            workgroup_id="wg-1",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            host="John Doe",
            documenter="Jane Smith",
            people_present=["Alice", "Bob"],
        )
        people_dict = extract_all_people([meeting])
        assert len(people_dict) == 4
        assert "John Doe" in people_dict
        assert "Jane Smith" in people_dict
        assert "Alice" in people_dict
        assert "Bob" in people_dict

    def test_extract_all_people_roles(self):
        """Test that people have correct roles."""
        meeting = Meeting(
            id="m1",
            workgroup="WG",
            workgroup_id="wg-1",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            host="John Doe",
            documenter="Jane Smith",
        )
        people_dict = extract_all_people([meeting])
        john = people_dict["John Doe"]
        assert "wg-1" in john.workgroups
        assert "host" in john.roles["wg-1"]
        jane = people_dict["Jane Smith"]
        assert "wg-1" in jane.workgroups
        assert "documenter" in jane.roles["wg-1"]

    def test_extract_all_people_empty(self):
        """Test extracting people from empty meeting list."""
        people_dict = extract_all_people([])
        assert people_dict == {}

    def test_get_people_list(self):
        """Test getting list of people."""
        meeting = Meeting(
            id="m1",
            workgroup="WG",
            workgroup_id="wg-1",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            host="John Doe",
        )
        people_list = get_people_list([meeting])
        assert len(people_list) == 1
        assert isinstance(people_list[0], Person)
        assert people_list[0].name == "John Doe"

