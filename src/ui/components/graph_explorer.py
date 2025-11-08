"""Streamlit UI component for graph explorer."""

import streamlit as st
from typing import List, Optional
from datetime import datetime

from src.models.meeting import Meeting
from src.services.graph_service import GraphService


def render_graph_explorer(
    meetings: List[Meeting],
    graph_service: GraphService,
    selected_workgroup: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> None:
    """Render graph explorer with filtering capabilities.

    Args:
        meetings: List of Meeting objects to visualize
        graph_service: GraphService instance for building graphs
        selected_workgroup: Selected workgroup filter (optional)
        start_date: Start date filter (optional)
        end_date: End date filter (optional)
    """
    if not meetings:
        st.info("No meetings available to visualize.")
        return

    st.header("🔗 Relationship Explorer")
    st.caption("Explore relationships between people, workgroups, and topics")

    # Filter meetings first
    filtered_meetings = meetings
    if selected_workgroup:
        filtered_meetings = [
            m for m in filtered_meetings if m.workgroup == selected_workgroup
        ]
    if start_date:
        filtered_meetings = [
            m for m in filtered_meetings if m.date >= start_date
        ]
    if end_date:
        filtered_meetings = [
            m for m in filtered_meetings if m.date <= end_date
        ]

    if not filtered_meetings:
        st.warning(
            "No meetings match the current filters. Try adjusting your filter criteria."
        )
        return

    # View selector
    view_type = st.radio(
        "Select View",
        options=["People and Workgroups", "Topics"],
        horizontal=True,
        help="Choose which relationships to visualize. 'People and Workgroups' shows connections between people and their workgroups. 'Topics' shows which topics appear together in meetings.",
    )

    # Build graph based on view type
    if view_type == "People and Workgroups":
        with st.spinner("Building people-workgroups graph..."):
            graph = graph_service.build_people_workgroups_graph(filtered_meetings)
            figure = graph_service.graph_to_plotly(graph, graph_type="people_workgroups")
    else:  # Topics
        with st.spinner("Building topic co-occurrence graph..."):
            graph = graph_service.build_topic_cooccurrence_graph(filtered_meetings)
            figure = graph_service.graph_to_plotly(graph, graph_type="topics")

    # Display graph
    if len(graph.nodes()) == 0:
        st.info("No relationships found to display.")
        return

    st.subheader(f"{view_type} Graph")
    st.caption(
        f"Showing {len(graph.nodes())} nodes and {len(graph.edges())} relationships from {len(filtered_meetings)} meeting(s)"
    )

    # Display Plotly chart
    st.plotly_chart(figure, use_container_width=True)

    # Display graph statistics
    with st.expander("📊 Graph Statistics", expanded=False, help="View detailed statistics about the relationship graph including node counts, edge counts, and breakdown by type"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nodes", len(graph.nodes()))
        with col2:
            st.metric("Edges", len(graph.edges()))
        with col3:
            st.metric("Meetings", len(filtered_meetings))

        # Show node details
        if view_type == "People and Workgroups":
            people_nodes = [
                n for n in graph.nodes() if graph.nodes[n].get("node_type") == "person"
            ]
            workgroup_nodes = [
                n
                for n in graph.nodes()
                if graph.nodes[n].get("node_type") == "workgroup"
            ]
            st.write(f"**People:** {len(people_nodes)}")
            st.write(f"**Workgroups:** {len(workgroup_nodes)}")
        else:
            topic_nodes = [
                n for n in graph.nodes() if graph.nodes[n].get("node_type") == "topic"
            ]
            st.write(f"**Topics:** {len(topic_nodes)}")

