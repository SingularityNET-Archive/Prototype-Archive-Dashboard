# Graph Service Contract

**Service**: Graph Service  
**Purpose**: Generate graph visualizations showing relationships in meeting data  
**Implements**: FR-017, FR-018, FR-019, FR-020

## Interface

```python
def build_people_workgroups_graph(meetings: List[Meeting]) -> nx.Graph:
    """
    Build NetworkX graph showing relationships between people and workgroups.
    
    Args:
        meetings: List of Meeting objects
        
    Returns:
        NetworkX graph with people and workgroups as nodes, participation as edges
    """
    pass

def build_topic_cooccurrence_graph(meetings: List[Meeting]) -> nx.Graph:
    """
    Build NetworkX graph showing topic co-occurrence relationships.
    
    Args:
        meetings: List of Meeting objects
        
    Returns:
        NetworkX graph with topics as nodes, co-occurrence as edges
    """
    pass

def graph_to_plotly(nx_graph: nx.Graph, graph_type: str) -> go.Figure:
    """
    Convert NetworkX graph to Plotly figure for visualization.
    
    Args:
        nx_graph: NetworkX graph
        graph_type: "people_workgroups" or "topics"
        
    Returns:
        Plotly figure object for interactive visualization
    """
    pass

def filter_graph(
    nx_graph: nx.Graph,
    workgroup: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> nx.Graph:
    """
    Filter graph to show only relationships within date range or workgroup.
    
    Args:
        nx_graph: NetworkX graph to filter
        workgroup: Workgroup to filter by (optional)
        start_date: Start date for date range filter (optional)
        end_date: End date for date range filter (optional)
        
    Returns:
        Filtered NetworkX graph
    """
    pass
```

## Contract Tests

1. **People-workgroups graph**: Graph contains nodes for all people and workgroups, edges for participation
2. **Topic co-occurrence graph**: Graph contains nodes for all topics, edges for co-occurrence in same meetings
3. **Graph filtering**: Filtering by workgroup or date range updates graph correctly
4. **Empty data**: Empty meetings list returns empty graph (no errors)
5. **Node details**: Clicking node provides access to detailed information (meetings, relationships)
6. **Performance**: Rendering graph for 100 workgroups and 1000 people completes in < 10 seconds (SC-006)

## Performance Requirements

- Render graph visualization: < 10 seconds for 100 workgroups and 1000 people (SC-006)

