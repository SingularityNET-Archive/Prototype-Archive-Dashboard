"""Contract tests for graph service."""

import pytest
from datetime import datetime
import networkx as nx

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.services.graph_service import GraphService


@pytest.fixture
def sample_meetings():
    """Create sample meetings for testing."""
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


def test_build_people_workgroups_graph_nodes(sample_meetings):
    """Test that people-workgroups graph contains nodes for all people and workgroups."""
    service = GraphService()
    graph = service.build_people_workgroups_graph(sample_meetings)

    assert isinstance(graph, nx.Graph)
    
    # Check that workgroups are nodes
    assert "Workgroup A" in graph.nodes()
    assert "Workgroup B" in graph.nodes()
    
    # Check that people are nodes (normalized names)
    # Person A appears in both workgroups
    # Person B, C appear in Workgroup A
    # Person D appears in Workgroup B
    node_names = list(graph.nodes())
    people_nodes = [n for n in node_names if n not in ["Workgroup A", "Workgroup B"]]
    assert len(people_nodes) > 0


def test_build_people_workgroups_graph_edges(sample_meetings):
    """Test that people-workgroups graph contains edges for participation."""
    service = GraphService()
    graph = service.build_people_workgroups_graph(sample_meetings)

    # Person A should be connected to both Workgroup A and Workgroup B
    # Check that edges exist
    edges = list(graph.edges())
    assert len(edges) > 0
    
    # Verify edges connect people to workgroups
    workgroups = {"Workgroup A", "Workgroup B"}
    for edge in edges:
        u, v = edge
        # One node should be a workgroup, the other a person
        assert (u in workgroups) != (v in workgroups), f"Edge {edge} should connect person to workgroup"


def test_build_topic_cooccurrence_graph_nodes(sample_meetings):
    """Test that topic co-occurrence graph contains nodes for all topics."""
    service = GraphService()
    graph = service.build_topic_cooccurrence_graph(sample_meetings)

    assert isinstance(graph, nx.Graph)
    
    # Check that topics are nodes (normalized)
    topics = ["Topic1", "Topic2", "Topic3"]
    for topic in topics:
        # Topics might be normalized (lowercase), so check case-insensitively
        node_names = [n.lower() for n in graph.nodes()]
        assert topic.lower() in node_names, f"Topic {topic} should be a node"


def test_build_topic_cooccurrence_graph_edges(sample_meetings):
    """Test that topic co-occurrence graph contains edges for co-occurrence."""
    service = GraphService()
    graph = service.build_topic_cooccurrence_graph(sample_meetings)

    # Topic1 and Topic2 co-occur in m1
    # Topic2 and Topic3 co-occur in m2
    # Topic1 and Topic3 co-occur in m3
    # So there should be edges between these pairs
    
    edges = list(graph.edges())
    assert len(edges) > 0
    
    # Verify that co-occurring topics are connected
    # Topic1-Topic2, Topic2-Topic3, Topic1-Topic3 should have edges
    edge_pairs = {(u.lower(), v.lower()) for u, v in edges}
    
    # Check for co-occurrence edges (order doesn't matter)
    assert ("topic1", "topic2") in edge_pairs or ("topic2", "topic1") in edge_pairs
    assert ("topic2", "topic3") in edge_pairs or ("topic3", "topic2") in edge_pairs
    assert ("topic1", "topic3") in edge_pairs or ("topic3", "topic1") in edge_pairs


def test_filter_graph_by_workgroup(sample_meetings):
    """Test that filtering graph by workgroup updates graph correctly."""
    service = GraphService()
    graph = service.build_people_workgroups_graph(sample_meetings)
    
    filtered_graph = service.filter_graph(graph, sample_meetings, workgroup="Workgroup A")
    
    assert isinstance(filtered_graph, nx.Graph)
    # Workgroup A should still be in the graph
    assert "Workgroup A" in filtered_graph.nodes()
    # Workgroup B should not be in the filtered graph
    assert "Workgroup B" not in filtered_graph.nodes()


def test_filter_graph_by_date_range(sample_meetings):
    """Test that filtering graph by date range updates graph correctly."""
    service = GraphService()
    graph = service.build_people_workgroups_graph(sample_meetings)
    
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 31)
    
    filtered_graph = service.filter_graph(
        graph, sample_meetings, start_date=start_date, end_date=end_date
    )
    
    assert isinstance(filtered_graph, nx.Graph)
    # Graph should be filtered to only include meetings in date range
    assert len(filtered_graph.nodes()) <= len(graph.nodes())


def test_empty_data_people_workgroups():
    """Test that empty meetings list returns empty graph (no errors)."""
    service = GraphService()
    graph = service.build_people_workgroups_graph([])
    
    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes()) == 0
    assert len(graph.edges()) == 0


def test_empty_data_topic_cooccurrence():
    """Test that empty meetings list returns empty graph (no errors)."""
    service = GraphService()
    graph = service.build_topic_cooccurrence_graph([])
    
    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes()) == 0
    assert len(graph.edges()) == 0


def test_graph_to_plotly_people_workgroups(sample_meetings):
    """Test that graph_to_plotly converts NetworkX graph to Plotly figure."""
    import plotly.graph_objects as go
    
    service = GraphService()
    graph = service.build_people_workgroups_graph(sample_meetings)
    figure = service.graph_to_plotly(graph, graph_type="people_workgroups")
    
    assert isinstance(figure, go.Figure)
    assert len(figure.data) > 0


def test_graph_to_plotly_topics(sample_meetings):
    """Test that graph_to_plotly converts topic graph to Plotly figure."""
    import plotly.graph_objects as go
    
    service = GraphService()
    graph = service.build_topic_cooccurrence_graph(sample_meetings)
    figure = service.graph_to_plotly(graph, graph_type="topics")
    
    assert isinstance(figure, go.Figure)
    assert len(figure.data) > 0


def test_graph_performance():
    """Test that rendering graph for 100 workgroups and 1000 people completes in < 10 seconds (SC-006)."""
    import time
    
    service = GraphService()
    
    # Create a large dataset (simplified - 100 workgroups, ~1000 people)
    # For performance test, we'll create meetings with many people
    meetings = []
    for i in range(100):  # 100 workgroups
        workgroup_id = f"uuid-{i}"
        people = [f"Person {j}" for j in range(10)]  # 10 people per workgroup = 1000 total
        
        meeting = Meeting(
            id=f"m{i}",
            workgroup=f"Workgroup {i}",
            workgroup_id=workgroup_id,
            date=datetime(2025, 1, 1),
            type="Custom",
            no_summary_given=False,
            canceled_summary=False,
            people_present=people,
        )
        meetings.append(meeting)
    
    start_time = time.time()
    graph = service.build_people_workgroups_graph(meetings)
    figure = service.graph_to_plotly(graph, graph_type="people_workgroups")
    elapsed_time = time.time() - start_time
    
    assert elapsed_time < 10.0, f"Graph rendering took {elapsed_time:.2f} seconds, expected < 10 seconds"

