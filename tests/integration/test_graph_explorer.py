"""Integration tests for graph explorer workflow."""

import pytest
from datetime import datetime

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.services.graph_service import GraphService


@pytest.fixture
def sample_meetings():
    """Create sample meetings for integration testing."""
    decision1 = Decision(
        id="d1",
        meeting_id="m1",
        workgroup="Workgroup A",
        date=datetime(2025, 1, 1),
        decision_text="Decision 1",
        effect="affectsOnlyThisWorkgroup",
    )
    action1 = ActionItem(
        id="a1",
        meeting_id="m1",
        workgroup="Workgroup A",
        date=datetime(2025, 1, 1),
        text="Action 1",
        status="todo",
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
            host="Person A",
            documenter="Person B",
            people_present=["Person A", "Person B", "Person C"],
            topics_covered=["Topic1", "Topic2"],
            decisions=[decision1],
            action_items=[action1],
        ),
        Meeting(
            id="m2",
            workgroup="Workgroup A",
            workgroup_id="uuid-1",
            date=datetime(2025, 1, 15),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            host="Person B",
            documenter="Person C",
            people_present=["Person B", "Person C"],
            topics_covered=["Topic2", "Topic3"],
        ),
        Meeting(
            id="m3",
            workgroup="Workgroup B",
            workgroup_id="uuid-2",
            date=datetime(2025, 2, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            host="Person A",
            documenter="Person D",
            people_present=["Person A", "Person D"],
            topics_covered=["Topic1", "Topic3"],
        ),
    ]


def test_graph_explorer_workflow_build_and_display(sample_meetings):
    """Test the complete workflow: build graph → convert to Plotly → display."""
    service = GraphService()

    # Step 1: Build people-workgroups graph
    graph = service.build_people_workgroups_graph(sample_meetings)

    assert len(graph.nodes()) > 0
    assert len(graph.edges()) > 0

    # Step 2: Convert to Plotly
    figure = service.graph_to_plotly(graph, graph_type="people_workgroups")

    assert figure is not None
    assert len(figure.data) > 0


def test_graph_explorer_workflow_filter(sample_meetings):
    """Test filtering graph by workgroup."""
    service = GraphService()

    # Build graph
    graph = service.build_people_workgroups_graph(sample_meetings)

    # Filter by workgroup
    filtered_graph = service.filter_graph(
        graph, sample_meetings, workgroup="Workgroup A"
    )

    assert "Workgroup A" in filtered_graph.nodes()
    assert "Workgroup B" not in filtered_graph.nodes()


def test_graph_explorer_workflow_topic_graph(sample_meetings):
    """Test building and displaying topic co-occurrence graph."""
    service = GraphService()

    # Build topic graph
    graph = service.build_topic_cooccurrence_graph(sample_meetings)

    assert len(graph.nodes()) > 0
    assert len(graph.edges()) > 0

    # Convert to Plotly
    figure = service.graph_to_plotly(graph, graph_type="topics")

    assert figure is not None
    assert len(figure.data) > 0


def test_graph_explorer_workflow_filter_by_date(sample_meetings):
    """Test filtering graph by date range."""
    service = GraphService()

    # Build graph
    graph = service.build_people_workgroups_graph(sample_meetings)

    # Filter by date range
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 31)

    filtered_graph = service.filter_graph(
        graph, sample_meetings, start_date=start_date, end_date=end_date
    )

    # Should only include meetings in date range
    assert len(filtered_graph.nodes()) <= len(graph.nodes())


def test_graph_explorer_workflow_interact_with_nodes(sample_meetings):
    """Test that graph nodes contain information for interaction."""
    service = GraphService()

    # Build graph
    graph = service.build_people_workgroups_graph(sample_meetings)

    # Check that nodes have metadata
    for node in graph.nodes():
        node_data = graph.nodes[node]
        assert "node_type" in node_data

    # Convert to Plotly (which includes hover info)
    figure = service.graph_to_plotly(graph, graph_type="people_workgroups")

    # Check that traces have hover information
    for trace in figure.data:
        assert hasattr(trace, "hoverinfo") or hasattr(trace, "text")

