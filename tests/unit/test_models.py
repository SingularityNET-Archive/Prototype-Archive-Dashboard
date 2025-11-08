"""Unit tests for data models."""

import pytest
from datetime import datetime
from src.models.meeting import Meeting
from src.models.workgroup import Workgroup
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.models.person import Person
from src.models.topic import Topic


class TestMeeting:
    """Test Meeting model."""

    def test_meeting_creation(self):
        """Test creating a Meeting with required fields."""
        meeting = Meeting(
            id="test_meeting_1",
            workgroup="Test Workgroup",
            workgroup_id="test-wg-123",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        )
        assert meeting.id == "test_meeting_1"
        assert meeting.workgroup == "Test Workgroup"
        assert meeting.workgroup_id == "test-wg-123"
        assert meeting.date == datetime(2024, 1, 15)
        assert meeting.type == "Custom"
        assert meeting.no_summary_given is False
        assert meeting.canceled_summary is False

    def test_meeting_with_optional_fields(self):
        """Test creating a Meeting with optional fields."""
        meeting = Meeting(
            id="test_meeting_2",
            workgroup="Test Workgroup",
            workgroup_id="test-wg-123",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            host="John Doe",
            documenter="Jane Smith",
            purpose="Test meeting purpose",
            people_present=["Alice", "Bob"],
            topics_covered=["Topic 1", "Topic 2"],
        )
        assert meeting.host == "John Doe"
        assert meeting.documenter == "Jane Smith"
        assert meeting.purpose == "Test meeting purpose"
        assert meeting.people_present == ["Alice", "Bob"]
        assert meeting.topics_covered == ["Topic 1", "Topic 2"]

    def test_meeting_repr(self):
        """Test Meeting string representation."""
        meeting = Meeting(
            id="test_meeting_3",
            workgroup="Test Workgroup",
            workgroup_id="test-wg-123",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        )
        repr_str = repr(meeting)
        assert "Meeting" in repr_str
        assert "test_meeting_3" in repr_str
        assert "Test Workgroup" in repr_str


class TestWorkgroup:
    """Test Workgroup model."""

    def test_workgroup_creation(self):
        """Test creating a Workgroup."""
        workgroup = Workgroup(id="test-wg-123", name="Test Workgroup")
        assert workgroup.id == "test-wg-123"
        assert workgroup.name == "Test Workgroup"
        assert workgroup.meetings == []

    def test_workgroup_with_meetings(self):
        """Test Workgroup with meetings."""
        meeting1 = Meeting(
            id="m1",
            workgroup="Test Workgroup",
            workgroup_id="test-wg-123",
            date=datetime(2024, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        )
        meeting2 = Meeting(
            id="m2",
            workgroup="Test Workgroup",
            workgroup_id="test-wg-123",
            date=datetime(2024, 2, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
        )
        workgroup = Workgroup(
            id="test-wg-123", name="Test Workgroup", meetings=[meeting1, meeting2]
        )
        assert len(workgroup.meetings) == 2
        assert workgroup.meeting_count == 2

    def test_workgroup_meeting_count_property(self):
        """Test Workgroup meeting_count property."""
        workgroup = Workgroup(id="test-wg-123", name="Test Workgroup")
        assert workgroup.meeting_count == 0

    def test_workgroup_repr(self):
        """Test Workgroup string representation."""
        workgroup = Workgroup(id="test-wg-123", name="Test Workgroup")
        repr_str = repr(workgroup)
        assert "Workgroup" in repr_str
        assert "test-wg-123" in repr_str
        assert "Test Workgroup" in repr_str


class TestDecision:
    """Test Decision model."""

    def test_decision_creation(self):
        """Test creating a Decision with required fields."""
        decision = Decision(
            id="decision_1",
            meeting_id="meeting_1",
            workgroup="Test Workgroup",
            date=datetime(2024, 1, 15),
            decision_text="Test decision",
            effect="affectsOnlyThisWorkgroup",
        )
        assert decision.id == "decision_1"
        assert decision.meeting_id == "meeting_1"
        assert decision.workgroup == "Test Workgroup"
        assert decision.date == datetime(2024, 1, 15)
        assert decision.decision_text == "Test decision"
        assert decision.effect == "affectsOnlyThisWorkgroup"

    def test_decision_with_optional_fields(self):
        """Test creating a Decision with optional fields."""
        decision = Decision(
            id="decision_2",
            meeting_id="meeting_1",
            workgroup="Test Workgroup",
            date=datetime(2024, 1, 15),
            decision_text="Test decision",
            effect="mayAffectOtherPeople",
            rationale="Test rationale",
            opposing="Test opposing views",
        )
        assert decision.rationale == "Test rationale"
        assert decision.opposing == "Test opposing views"
        assert decision.effect == "mayAffectOtherPeople"

    def test_decision_effect_normalization(self):
        """Test Decision effect field normalization (case-insensitive)."""
        # Test lowercase
        decision1 = Decision(
            id="d1",
            meeting_id="m1",
            workgroup="WG",
            date=datetime(2024, 1, 15),
            decision_text="Test",
            effect="affectsonlythisworkgroup",
        )
        assert decision1.effect == "affectsOnlyThisWorkgroup"

        # Test mixed case
        decision2 = Decision(
            id="d2",
            meeting_id="m1",
            workgroup="WG",
            date=datetime(2024, 1, 15),
            decision_text="Test",
            effect="MAYAFFECTOTHERPEOPLE",
        )
        assert decision2.effect == "mayAffectOtherPeople"

    def test_decision_empty_text_raises_error(self):
        """Test that Decision with empty text raises ValueError."""
        with pytest.raises(ValueError, match="decision_text must be non-empty"):
            Decision(
                id="d1",
                meeting_id="m1",
                workgroup="WG",
                date=datetime(2024, 1, 15),
                decision_text="",
                effect="affectsOnlyThisWorkgroup",
            )

    def test_decision_invalid_effect_raises_error(self):
        """Test that Decision with invalid effect raises ValueError."""
        with pytest.raises(ValueError, match="effect must be"):
            Decision(
                id="d1",
                meeting_id="m1",
                workgroup="WG",
                date=datetime(2024, 1, 15),
                decision_text="Test",
                effect="invalid_effect",
            )

    def test_decision_repr(self):
        """Test Decision string representation."""
        decision = Decision(
            id="decision_1",
            meeting_id="meeting_1",
            workgroup="Test Workgroup",
            date=datetime(2024, 1, 15),
            decision_text="Test decision",
            effect="affectsOnlyThisWorkgroup",
        )
        repr_str = repr(decision)
        assert "Decision" in repr_str
        assert "decision_1" in repr_str
        assert "Test Workgroup" in repr_str


class TestActionItem:
    """Test ActionItem model."""

    def test_action_item_creation(self):
        """Test creating an ActionItem with required fields."""
        action_item = ActionItem(
            id="action_1",
            meeting_id="meeting_1",
            workgroup="Test Workgroup",
            date=datetime(2024, 1, 15),
            text="Test action item",
            status="todo",
        )
        assert action_item.id == "action_1"
        assert action_item.meeting_id == "meeting_1"
        assert action_item.workgroup == "Test Workgroup"
        assert action_item.date == datetime(2024, 1, 15)
        assert action_item.text == "Test action item"
        assert action_item.status == "todo"

    def test_action_item_with_optional_fields(self):
        """Test creating an ActionItem with optional fields."""
        action_item = ActionItem(
            id="action_2",
            meeting_id="meeting_1",
            workgroup="Test Workgroup",
            date=datetime(2024, 1, 15),
            text="Test action item",
            status="in progress",
            assignee="John Doe",
            due_date="2024-02-01",
        )
        assert action_item.assignee == "John Doe"
        assert action_item.due_date == "2024-02-01"
        assert action_item.status == "in progress"

    def test_action_item_status_normalization(self):
        """Test ActionItem status field normalization."""
        # Test variations
        test_cases = [
            ("todo", "todo"),
            ("To Do", "todo"),
            ("TO-DO", "todo"),
            ("in progress", "in progress"),
            ("In Progress", "in progress"),
            ("IN-PROGRESS", "in progress"),
            ("done", "done"),
            ("Done", "done"),
            ("COMPLETED", "done"),
            ("cancelled", "cancelled"),
            ("Canceled", "cancelled"),
        ]

        for input_status, expected_status in test_cases:
            action_item = ActionItem(
                id="a1",
                meeting_id="m1",
                workgroup="WG",
                date=datetime(2024, 1, 15),
                text="Test",
                status=input_status,
            )
            assert action_item.status == expected_status

    def test_action_item_empty_text_raises_error(self):
        """Test that ActionItem with empty text raises ValueError."""
        with pytest.raises(ValueError, match="text must be non-empty"):
            ActionItem(
                id="a1",
                meeting_id="m1",
                workgroup="WG",
                date=datetime(2024, 1, 15),
                text="",
                status="todo",
            )

    def test_action_item_invalid_status_defaults_to_todo(self):
        """Test that ActionItem with invalid status defaults to 'todo'."""
        # The ActionItem model normalizes unrecognized statuses to "todo"
        action_item = ActionItem(
            id="a1",
            meeting_id="m1",
            workgroup="WG",
            date=datetime(2024, 1, 15),
            text="Test",
            status="invalid_status",
        )
        assert action_item.status == "todo"

    def test_action_item_repr(self):
        """Test ActionItem string representation."""
        action_item = ActionItem(
            id="action_1",
            meeting_id="meeting_1",
            workgroup="Test Workgroup",
            date=datetime(2024, 1, 15),
            text="Test action item",
            status="todo",
        )
        repr_str = repr(action_item)
        assert "ActionItem" in repr_str
        assert "action_1" in repr_str
        assert "Test Workgroup" in repr_str


class TestPerson:
    """Test Person model."""

    def test_person_creation(self):
        """Test creating a Person."""
        person = Person(name="John Doe")
        assert person.name == "John Doe"
        assert person.workgroups == set()
        assert person.meetings_attended == []
        assert person.action_items_assigned == []
        assert person.roles == {}

    def test_person_empty_name_raises_error(self):
        """Test that Person with empty name raises ValueError."""
        with pytest.raises(ValueError, match="name must be non-empty string"):
            Person(name="")

    def test_person_add_workgroup(self):
        """Test adding a workgroup to a Person."""
        person = Person(name="John Doe")
        person.add_workgroup("wg-1", role="host")
        assert "wg-1" in person.workgroups
        assert "wg-1" in person.roles
        assert "host" in person.roles["wg-1"]

    def test_person_add_meeting(self):
        """Test adding a meeting to a Person."""
        person = Person(name="John Doe")
        person.add_meeting("meeting-1")
        assert "meeting-1" in person.meetings_attended
        # Adding same meeting twice should not duplicate
        person.add_meeting("meeting-1")
        assert person.meetings_attended.count("meeting-1") == 1

    def test_person_add_action_item(self):
        """Test adding an action item to a Person."""
        person = Person(name="John Doe")
        person.add_action_item("action-1")
        assert "action-1" in person.action_items_assigned
        # Adding same action item twice should not duplicate
        person.add_action_item("action-1")
        assert person.action_items_assigned.count("action-1") == 1

    def test_person_repr(self):
        """Test Person string representation."""
        person = Person(name="John Doe")
        repr_str = repr(person)
        assert "Person" in repr_str
        assert "John Doe" in repr_str


class TestTopic:
    """Test Topic model."""

    def test_topic_creation(self):
        """Test creating a Topic."""
        topic = Topic(name="Test Topic")
        assert topic.name == "Test Topic"
        assert topic.meetings == []
        assert topic.workgroups == set()
        assert topic.co_occurrences == {}

    def test_topic_with_data(self):
        """Test Topic with meetings and workgroups."""
        topic = Topic(
            name="Test Topic",
            meetings=["meeting-1", "meeting-2"],
            workgroups={"wg-1", "wg-2"},
            co_occurrences={"Other Topic": 3},
        )
        assert len(topic.meetings) == 2
        assert len(topic.workgroups) == 2
        assert topic.co_occurrences["Other Topic"] == 3

    def test_topic_repr(self):
        """Test Topic string representation."""
        topic = Topic(name="Test Topic")
        repr_str = repr(topic)
        assert "Topic" in repr_str
        assert "Test Topic" in repr_str

