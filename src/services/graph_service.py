"""Graph service for generating relationship visualizations."""

from typing import List, Optional, Dict, Set
from datetime import datetime
import networkx as nx
import plotly.graph_objects as go
from plotly.graph_objs import Scatter

from src.models.meeting import Meeting
from src.utils.person_extractor import extract_all_people
from src.utils.topic_extractor import extract_all_topics
from src.utils.logger import logger


class GraphService:
    """Service for generating graph visualizations of relationships in meeting data."""

    def __init__(self):
        """Initialize GraphService."""
        pass

    def build_people_workgroups_graph(self, meetings: List[Meeting]) -> nx.Graph:
        """Build NetworkX graph showing relationships between people and workgroups.

        Nodes: People and workgroups
        Edges: Participation (person participates in workgroup)

        Args:
            meetings: List of Meeting objects

        Returns:
            NetworkX graph with people and workgroups as nodes, participation as edges
        """
        graph = nx.Graph()

        if not meetings:
            return graph

        # Extract all people from meetings
        people_dict = extract_all_people(meetings)

        # Add workgroup nodes
        workgroups = set()
        for meeting in meetings:
            workgroups.add(meeting.workgroup)

        for workgroup in workgroups:
            graph.add_node(workgroup, node_type="workgroup")

        # Add people nodes and edges
        for person in people_dict.values():
            graph.add_node(person.name, node_type="person")
            
            # Add edges for each workgroup the person participates in
            for workgroup_id in person.workgroups:
                # Find workgroup name from meetings
                workgroup_name = None
                for meeting in meetings:
                    if meeting.workgroup_id == workgroup_id:
                        workgroup_name = meeting.workgroup
                        break
                
                if workgroup_name:
                    graph.add_edge(person.name, workgroup_name)

        logger.info(
            f"Built people-workgroups graph with {len(graph.nodes())} nodes and {len(graph.edges())} edges"
        )
        return graph

    def build_topic_cooccurrence_graph(self, meetings: List[Meeting]) -> nx.Graph:
        """Build NetworkX graph showing topic co-occurrence relationships.

        Nodes: Topics
        Edges: Co-occurrence (topics appear together in same meetings)

        Args:
            meetings: List of Meeting objects

        Returns:
            NetworkX graph with topics as nodes, co-occurrence as edges
        """
        graph = nx.Graph()

        if not meetings:
            return graph

        # Track topic co-occurrences
        topic_cooccurrences: Dict[tuple, int] = {}

        for meeting in meetings:
            if not meeting.topics_covered:
                continue

            # Normalize topics for matching
            normalized_topics = [t.lower().strip() for t in meeting.topics_covered if t.strip()]
            
            # Create edges for all pairs of topics in this meeting
            for i, topic1 in enumerate(normalized_topics):
                graph.add_node(topic1, node_type="topic")
                
                for topic2 in normalized_topics[i + 1:]:
                    graph.add_node(topic2, node_type="topic")
                    
                    # Create or update edge (order doesn't matter)
                    edge = tuple(sorted([topic1, topic2]))
                    topic_cooccurrences[edge] = topic_cooccurrences.get(edge, 0) + 1
                    
                    # Add edge with weight (co-occurrence count)
                    if graph.has_edge(topic1, topic2):
                        graph[topic1][topic2]["weight"] = topic_cooccurrences[edge]
                    else:
                        graph.add_edge(topic1, topic2, weight=topic_cooccurrences[edge])

        logger.info(
            f"Built topic co-occurrence graph with {len(graph.nodes())} nodes and {len(graph.edges())} edges"
        )
        return graph

    def graph_to_plotly(
        self, nx_graph: nx.Graph, graph_type: str
    ) -> go.Figure:
        """Convert NetworkX graph to Plotly figure for visualization.

        Args:
            nx_graph: NetworkX graph
            graph_type: "people_workgroups" or "topics"

        Returns:
            Plotly figure object for interactive visualization
        """
        if len(nx_graph.nodes()) == 0:
            # Return empty figure
            fig = go.Figure()
            fig.add_annotation(
                text="No data to display",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )
            return fig

        # Use spring layout for positioning
        pos = nx.spring_layout(nx_graph, k=1, iterations=50)

        # Separate nodes by type for different styling
        if graph_type == "people_workgroups":
            people_nodes = [n for n in nx_graph.nodes() if nx_graph.nodes[n].get("node_type") == "person"]
            workgroup_nodes = [n for n in nx_graph.nodes() if nx_graph.nodes[n].get("node_type") == "workgroup"]
        else:  # topics
            people_nodes = []
            workgroup_nodes = []
            topic_nodes = list(nx_graph.nodes())

        # Extract edge information
        edge_x = []
        edge_y = []
        for edge in nx_graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color="#888"),
            hoverinfo="none",
            mode="lines",
        )

        # Create node traces
        node_traces = []

        if graph_type == "people_workgroups":
            # People nodes
            if people_nodes:
                people_x = [pos[node][0] for node in people_nodes]
                people_y = [pos[node][1] for node in people_nodes]
                people_text = [f"Person: {node}" for node in people_nodes]

                node_traces.append(
                    go.Scatter(
                        x=people_x,
                        y=people_y,
                        mode="markers+text",
                        name="People",
                        marker=dict(
                            size=10,
                            color="lightblue",
                            line=dict(width=2, color="blue"),
                        ),
                        text=people_text,
                        textposition="middle center",
                        hoverinfo="text",
                    )
                )

            # Workgroup nodes
            if workgroup_nodes:
                workgroup_x = [pos[node][0] for node in workgroup_nodes]
                workgroup_y = [pos[node][1] for node in workgroup_nodes]
                workgroup_text = [f"Workgroup: {node}" for node in workgroup_nodes]

                node_traces.append(
                    go.Scatter(
                        x=workgroup_x,
                        y=workgroup_y,
                        mode="markers+text",
                        name="Workgroups",
                        marker=dict(
                            size=15,
                            color="lightgreen",
                            line=dict(width=2, color="green"),
                        ),
                        text=workgroup_text,
                        textposition="middle center",
                        hoverinfo="text",
                    )
                )
        else:  # topics
            topic_x = [pos[node][0] for node in topic_nodes]
            topic_y = [pos[node][1] for node in topic_nodes]
            topic_text = [f"Topic: {node}" for node in topic_nodes]

            node_traces.append(
                go.Scatter(
                    x=topic_x,
                    y=topic_y,
                    mode="markers+text",
                    name="Topics",
                    marker=dict(
                        size=12,
                        color="lightcoral",
                        line=dict(width=2, color="red"),
                    ),
                    text=topic_text,
                    textposition="middle center",
                    hoverinfo="text",
                )
            )

        # Create figure
        fig = go.Figure(
            data=[edge_trace] + node_traces,
            layout=go.Layout(
                title=dict(text="Relationship Graph", font=dict(size=16)),
                showlegend=True,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[
                    dict(
                        text="",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=0.005,
                        y=-0.002,
                        xanchor="left",
                        yanchor="bottom",
                        font=dict(color="#888", size=12),
                    )
                ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )

        return fig

    def filter_graph(
        self,
        nx_graph: nx.Graph,
        meetings: List[Meeting],
        workgroup: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> nx.Graph:
        """Filter graph to show only relationships within date range or workgroup.

        Note: This method filters the source meetings first, then rebuilds the graph.
        This ensures the graph accurately reflects the filtered data.

        Args:
            nx_graph: NetworkX graph to filter (original graph, used for reference)
            meetings: List of Meeting objects (source data)
            workgroup: Workgroup to filter by (optional)
            start_date: Start date for date range filter (optional)
            end_date: End date for date range filter (optional)

        Returns:
            Filtered NetworkX graph
        """
        # Filter meetings first
        filtered_meetings = meetings

        if workgroup:
            filtered_meetings = [
                m for m in filtered_meetings if m.workgroup == workgroup
            ]

        if start_date:
            filtered_meetings = [
                m for m in filtered_meetings if m.date >= start_date
            ]

        if end_date:
            filtered_meetings = [
                m for m in filtered_meetings if m.date <= end_date
            ]

        # Determine graph type from original graph
        # Check node types to determine if it's people_workgroups or topics
        node_types = {
            nx_graph.nodes[n].get("node_type") for n in nx_graph.nodes()
        }
        
        if "person" in node_types or "workgroup" in node_types:
            # Rebuild people-workgroups graph with filtered meetings
            return self.build_people_workgroups_graph(filtered_meetings)
        else:
            # Rebuild topic co-occurrence graph with filtered meetings
            return self.build_topic_cooccurrence_graph(filtered_meetings)

