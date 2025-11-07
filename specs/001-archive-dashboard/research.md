# Research: Meeting Archive Dashboard

**Date**: 2025-11-07  
**Feature**: Meeting Archive Dashboard  
**Purpose**: Resolve technical decisions for dashboard framework, graph visualization, and testing approach

## Research Questions

### 1. Dashboard Framework: Streamlit vs Dash vs Flask+Plotly

**Decision**: **Streamlit**

**Rationale**:
- **Rapid development**: Streamlit is designed for data apps with minimal boilerplate, ideal for MVP
- **Built-in interactivity**: Native support for filters, selectors, and reactive updates without custom JavaScript
- **Accessibility**: Streamlit's component library includes tooltips, clear labels, and responsive design out of the box (aligns with FR-023)
- **Data visualization**: Native integration with Plotly, Matplotlib, and other visualization libraries
- **Non-technical user focus**: Streamlit's declarative API produces clear, intuitive UIs (aligns with constitution Accessibility principle)
- **Performance**: Sufficient for 10,000 meetings with proper data loading strategies (caching, lazy loading)
- **Export capabilities**: Easy to add CSV/JSON export buttons (FR-024)

**Alternatives Considered**:
- **Dash**: More flexible but requires more code for similar functionality, steeper learning curve
- **Flask+Plotly**: Maximum flexibility but requires significant frontend/backend separation, more complex deployment

**Implementation Notes**:
- Use `st.cache_data` for JSON parsing and data normalization to meet performance goals
- Use `st.sidebar` for filters (workgroup, date range, tags)
- Use `st.tabs` or `st.selectbox` for view switching (workgroup browser, decision tracker, graph explorer)
- Use `st.download_button` for plain-text export

### 2. Graph Visualization Library

**Decision**: **NetworkX + Plotly** (via `plotly.graph_objects`)

**Rationale**:
- **NetworkX**: Industry-standard Python library for graph data structures and algorithms
  - Efficient graph construction from meeting data
  - Built-in algorithms for node/edge analysis
  - Handles 1000+ nodes efficiently (meets SC-006)
- **Plotly**: Interactive graph visualization with zoom, pan, hover tooltips
  - Native Streamlit integration via `st.plotly_chart`
  - Interactive node clicking for detail views (FR-019)
  - Responsive rendering for large graphs
  - Export capabilities for graph images

**Alternatives Considered**:
- **D3.js via JavaScript**: More powerful but requires frontend/backend separation, adds complexity
- **Cytoscape.js**: Good for web but requires JavaScript integration layer
- **Matplotlib**: Static graphs, no interactivity required by FR-019

**Implementation Notes**:
- Use NetworkX to build graph structures from normalized meeting data
- Convert NetworkX graphs to Plotly format using `plotly.graph_objects` for visualization
- Implement node click handlers to show detail views (FR-019)
- Use graph layout algorithms (spring, force-directed) for readable visualizations

### 3. Data Processing Libraries

**Decision**: **pandas + standard library json**

**Rationale**:
- **pandas**: Efficient data manipulation for filtering, aggregation, and transformation
  - Fast filtering by date range, workgroup, tags (meets SC-002, SC-003)
  - Efficient aggregation for decisions and action items (meets SC-004)
  - Handles 10,000+ records without performance issues (meets SC-009)
  - Easy export to CSV/JSON (FR-024)
- **json (standard library)**: Sufficient for parsing JSON archive file
  - No additional dependencies
  - Handles malformed JSON with proper error handling (edge case)

**Alternatives Considered**:
- **pydantic**: Type validation but adds complexity for MVP, can be added later for schema validation
- **jsonschema**: Schema validation useful but not required for MVP (can add in Phase 2)

**Implementation Notes**:
- Use pandas DataFrame for in-memory data storage after JSON parsing
- Use pandas filtering for date range, workgroup, tag filters
- Use pandas groupby for aggregating decisions and action items
- Cache parsed DataFrame using Streamlit's caching to avoid re-parsing on every interaction

### 4. Testing Approach for Interactive Dashboard

**Decision**: **pytest + Streamlit testing utilities + contract tests**

**Rationale**:
- **pytest**: Standard Python testing framework, well-documented and widely used
- **Contract tests**: Test data parsing and normalization independently of UI (FR-001, FR-002)
- **Unit tests**: Test models, services, and utilities in isolation
- **Integration tests**: Test end-to-end workflows (load → filter → display) using Streamlit's testing utilities
- **UI component testing**: Use Streamlit's `st.testing` utilities or manual testing for interactive components

**Alternatives Considered**:
- **Playwright/Selenium**: Full browser automation but overkill for MVP, adds complexity
- **Manual testing only**: Insufficient for ensuring data correctness and performance

**Implementation Notes**:
- Contract tests: Verify JSON parsing produces correct data models
- Unit tests: Test filtering logic, aggregation logic, graph generation independently
- Integration tests: Test complete user workflows (select workgroup → view meetings → apply filters)
- Performance tests: Verify SC-001 through SC-006 timing requirements
- UI testing: Manual testing for accessibility and usability (FR-023)

### 5. Date Parsing and Normalization

**Decision**: **dateutil.parser + pandas.to_datetime**

**Rationale**:
- **dateutil.parser**: Handles various date formats flexibly (edge case: inconsistent date formats)
- **pandas.to_datetime**: Efficient conversion to datetime objects for filtering and sorting
- Both handle ISO format (YYYY-MM-DD) as primary format, with fallback for variations

**Implementation Notes**:
- Primary: Parse ISO dates (YYYY-MM-DD) as specified in assumptions
- Fallback: Use dateutil.parser for non-standard formats
- Normalize all dates to datetime objects for consistent filtering and sorting

### 6. Text Parsing and Normalization

**Decision**: **Standard library string methods + custom normalization**

**Rationale**:
- **Comma-separated parsing**: Use `str.split(',')` for topicsCovered and peoplePresent
- **Text normalization**: Custom functions to handle whitespace, case variations, special characters
- **Topic extraction**: Parse comma-separated topicsCovered string, normalize (trim, lowercase for matching)

**Implementation Notes**:
- Parse `peoplePresent` comma-separated string into list
- Parse `topicsCovered` comma-separated string into list of topics
- Normalize topic names for consistent filtering (trim whitespace, handle case variations)
- Handle special characters in names and topics (edge case)

## Summary of Technical Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| Dashboard Framework | Streamlit | Rapid development, built-in interactivity, accessibility features |
| Graph Visualization | NetworkX + Plotly | Efficient graph algorithms + interactive visualization |
| Data Processing | pandas + json | Efficient filtering/aggregation, standard JSON parsing |
| Testing | pytest + contract tests | Comprehensive test coverage for data correctness |
| Date Parsing | dateutil.parser + pandas | Flexible date format handling |
| Text Parsing | Standard library + custom | Simple, sufficient for comma-separated strings |

## Dependencies Summary

**Core Dependencies**:
- `streamlit` - Dashboard framework
- `pandas` - Data manipulation and filtering
- `networkx` - Graph data structures and algorithms
- `plotly` - Interactive graph visualization
- `python-dateutil` - Flexible date parsing
- `pytest` - Testing framework

**Development Dependencies**:
- `pytest-cov` - Test coverage reporting
- `black` - Code formatting (constitution: transparency)
- `mypy` - Type checking (optional, for code quality)

## Performance Considerations

- **Caching**: Use `st.cache_data` for JSON parsing and data normalization to avoid re-parsing on every interaction
- **Lazy loading**: Load graph visualizations only when graph explorer view is selected
- **Pagination**: Consider pagination for large result sets (10,000+ meetings) if performance degrades
- **Data structures**: Use pandas DataFrame for efficient filtering and aggregation operations

## Next Steps

1. Create data-model.md with entity definitions and validation rules
2. Design API contracts for data access layer (even if internal to Streamlit app)
3. Create quickstart.md with setup and usage instructions
4. Update agent context with selected technologies

