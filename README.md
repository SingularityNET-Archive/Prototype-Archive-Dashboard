# Meeting Archive Dashboard

A modular, Python-based web dashboard for browsing workgroup meeting archives. The dashboard loads JSON archive data, normalizes it, and provides interactive interfaces for browsing by workgroup, filtering by date/tags, tracking decisions and action items, and exploring relationships via graph visualizations.

## Features

- **Workgroup Browser**: Select a workgroup and view all meetings in chronological order
- **Meeting Filters**: Filter meetings by date range and topic tags
- **Decision Tracker**: View aggregated decisions with filtering capabilities
- **Action Item Tracker**: Track action items with assignee, status, and due date filtering
- **Graph Explorer**: Visualize relationships between people, topics, and workgroups

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## Setup

### 1. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Data File

Ensure `meeting-summaries-array-3.json` is in the `data/` directory.

### 4. Run Dashboard

```bash
streamlit run src/ui/dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

## Project Structure

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

data/
└── meeting-summaries-array-3.json  # Input JSON archive file

docs/
└── schemas/         # JSON schema definitions
```

## Running Tests

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

## Development

See `specs/001-archive-dashboard/` for detailed documentation including:
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `data-model.md` - Data model definitions
- `quickstart.md` - Quickstart guide
- `contracts/` - Service contracts

## License

[Add license information if applicable]

