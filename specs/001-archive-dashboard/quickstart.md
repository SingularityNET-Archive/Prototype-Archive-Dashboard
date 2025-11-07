# Quickstart Guide: Meeting Archive Dashboard

**Date**: 2025-11-07  
**Feature**: Meeting Archive Dashboard  
**Purpose**: Get the dashboard running quickly for development and testing

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git (for cloning repository)

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas networkx plotly python-dateutil pytest
```

### 2. Verify Data File

Ensure `meeting-summaries-array-3.json` is in the repository root or `data/` directory.

### 3. Run Dashboard

```bash
# From repository root
streamlit run src/ui/dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

## Usage

### Workgroup Browser (User Story 1)

1. **Select Workgroup**: Use the sidebar dropdown to select a workgroup
2. **View Meetings**: Meetings for the selected workgroup appear in chronological order
3. **View Details**: Click on a meeting to see full details (date, host, documenter, purpose, people present)

### Filter Meetings (User Story 2)

1. **Date Range Filter**: Use date pickers in the sidebar to select start and end dates
2. **Tag Filter**: Select one or more topic tags from the tag selector
3. **Combine Filters**: Apply multiple filters simultaneously (workgroup + date + tags)
4. **Clear Filters**: Click "Clear All Filters" to reset

### Decision Tracker (User Story 3)

1. **View Decisions**: Navigate to "Decision Tracker" tab
2. **Filter by Workgroup**: Use workgroup filter to see decisions for specific workgroups
3. **View Action Items**: Navigate to "Action Items" tab
4. **Filter Action Items**: Filter by assignee, status (todo/in progress/done), or date range

### Graph Explorer (User Story 4)

1. **Navigate to Graph Explorer**: Click "Graph Explorer" tab
2. **Select View**: Choose "People and Workgroups" or "Topics" view
3. **Interact with Graph**: Click nodes to see details, zoom and pan to explore
4. **Filter Graph**: Apply date range or workgroup filters to focus on specific relationships

### Export Data (FR-024)

1. **Export Current View**: Click "Export" button on any view
2. **Choose Format**: Select plain text, CSV, or JSON format
3. **Download**: File downloads to your default download directory

## Development

### Project Structure

```
src/
├── models/          # Data models (Meeting, Workgroup, Decision, etc.)
├── parsers/         # JSON parsing and normalization
├── services/        # Business logic (filtering, aggregation, graphs)
├── ui/              # Streamlit UI components
└── utils/           # Utility functions

tests/
├── contract/        # Contract tests
├── integration/    # Integration tests
└── unit/           # Unit tests
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/contract/
pytest tests/integration/
pytest tests/unit/

# Run with coverage
pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code (if black is installed)
black src/ tests/

# Type checking (if mypy is installed)
mypy src/
```

## Configuration

### Data File Location

By default, the dashboard looks for `meeting-summaries-array-3.json` in:
1. Repository root directory
2. `data/` directory (if exists)

To use a different file, modify the path in `src/parsers/data_parser.py`.

### Performance Tuning

For large datasets (10,000+ meetings):
- Enable caching: Already enabled via `st.cache_data` decorators
- Adjust pagination: Modify page size in UI components if needed
- Graph rendering: Consider limiting graph size for very large datasets

## Troubleshooting

### Dashboard Won't Start

- **Check Python version**: Ensure Python 3.11+ is installed (`python3 --version`)
- **Check dependencies**: Run `pip install -r requirements.txt` (if requirements.txt exists)
- **Check data file**: Ensure JSON file exists and is readable

### Performance Issues

- **Clear cache**: Streamlit caches data - restart the app to clear cache
- **Reduce data size**: Test with a subset of meetings first
- **Check logs**: Look for error messages in terminal/console

### Data Not Loading

- **Check JSON format**: Ensure JSON file is valid (use `python -m json.tool meeting-summaries-array-3.json`)
- **Check file path**: Verify the file path is correct
- **Check permissions**: Ensure file is readable

### Graph Not Rendering

- **Check data**: Ensure meetings have relationships (people, topics)
- **Check browser**: Try a different browser if graph doesn't render
- **Check console**: Look for JavaScript errors in browser console

## Next Steps

1. **Review Specification**: Read `spec.md` for complete feature requirements
2. **Review Data Model**: Read `data-model.md` for entity definitions
3. **Review Contracts**: Read `contracts/` for service interfaces
4. **Start Development**: Begin with User Story 1 (Workgroup Browser)

## Support

- **Documentation**: See `specs/001-archive-dashboard/` for detailed documentation
- **Issues**: Report issues via GitHub Issues
- **Constitution**: See `.specify/memory/constitution.md` for project principles

