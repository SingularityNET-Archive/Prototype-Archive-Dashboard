# Data Model: Meeting Archive Dashboard

**Date**: 2025-11-07  
**Feature**: Meeting Archive Dashboard  
**Purpose**: Define data entities, relationships, validation rules, and normalization logic

## Overview

The dashboard processes JSON archive data into normalized Python data models for efficient querying, filtering, and visualization. All entities preserve attribution metadata as required by the constitution (FR-022).

## Core Entities

### 1. Meeting

**Purpose**: Represents a single meeting record from the archive.

**Fields**:
- `id` (str, generated): Unique identifier for the meeting (derived from workgroup_id + date + index)
- `workgroup` (str, required): Workgroup name
- `workgroup_id` (str, required): Unique workgroup identifier (UUID format)
- `date` (datetime, required): Meeting date (ISO format YYYY-MM-DD, parsed to datetime)
- `host` (str, optional): Meeting host name
- `documenter` (str, optional): Person who documented the meeting
- `people_present` (list[str], optional): List of people present (parsed from comma-separated string)
- `purpose` (str, optional): Meeting purpose/description
- `type_of_meeting` (str, optional): e.g., "Monthly", "Weekly"
- `meeting_video_link` (str, optional): URL to meeting video
- `working_docs` (list[dict], optional): List of {title: str, link: str} objects
- `action_items` (list[ActionItem], optional): List of action items from this meeting
- `decisions` (list[Decision], optional): List of decisions from this meeting
- `discussion_points` (list[str], optional): List of discussion points (from discussionPoints or narrative)
- `topics_covered` (list[str], optional): List of topics (parsed from tags.topicsCovered)
- `emotions` (list[str], optional): List of emotions (parsed from tags.emotions)
- `type` (str, required): Meeting type (e.g., "Custom")
- `no_summary_given` (bool, required): Flag indicating if summary was provided
- `canceled_summary` (bool, required): Flag indicating if summary was canceled

**Validation Rules**:
- `date` must be parseable as ISO date (YYYY-MM-DD) or valid date format
- `workgroup` and `workgroup_id` must both be present (required fields)
- `people_present` must be a list (empty list if not present)
- `topics_covered` must be a list (empty list if not present)
- `action_items` and `decisions` must be lists (empty lists if not present)

**Normalization**:
- Parse `peoplePresent` comma-separated string into list, trim whitespace
- Parse `topicsCovered` comma-separated string into list, normalize (trim, lowercase for matching)
- Parse `emotions` comma-separated string into list, trim whitespace
- Handle `discussionPoints` (array) or `narrative` (string) - convert narrative to single-item list
- Handle `meetingTopics` (array) - merge with topics_covered if present
- Convert date string to datetime object for filtering and sorting
- Generate unique `id` from workgroup_id + date + meeting index

**State Transitions**: None (immutable data model)

### 2. Workgroup

**Purpose**: Represents a community workgroup.

**Fields**:
- `id` (str, required): Unique workgroup identifier (UUID format from workgroup_id)
- `name` (str, required): Workgroup name
- `meeting_count` (int, computed): Number of meetings for this workgroup
- `meetings` (list[Meeting], computed): List of meetings for this workgroup

**Validation Rules**:
- `id` must be valid UUID format
- `name` must be non-empty string

**Relationships**:
- One-to-many with Meeting (one workgroup has many meetings)

### 3. Decision

**Purpose**: Represents a decision made in a meeting.

**Fields**:
- `id` (str, generated): Unique identifier (derived from meeting_id + decision index)
- `meeting_id` (str, required): Reference to parent meeting
- `workgroup` (str, required): Workgroup name (from parent meeting)
- `date` (datetime, required): Meeting date (from parent meeting)
- `decision_text` (str, required): The decision text
- `rationale` (str, optional): Rationale for the decision
- `effect` (str, required): Effect scope - "affectsOnlyThisWorkgroup" or "mayAffectOtherPeople"
- `opposing` (str, optional): Opposing views or "none"

**Validation Rules**:
- `decision_text` must be non-empty string
- `effect` must be one of: "affectsOnlyThisWorkgroup", "mayAffectOtherPeople"
- `meeting_id` must reference a valid meeting

**Normalization**:
- Trim whitespace from decision_text and rationale
- Normalize effect value (case-insensitive matching)

**Relationships**:
- Many-to-one with Meeting (many decisions belong to one meeting)
- Many-to-one with Workgroup (many decisions belong to one workgroup)

### 4. ActionItem

**Purpose**: Represents a task or action item from a meeting.

**Fields**:
- `id` (str, generated): Unique identifier (derived from meeting_id + action index)
- `meeting_id` (str, required): Reference to parent meeting
- `workgroup` (str, required): Workgroup name (from parent meeting)
- `date` (datetime, required): Meeting date (from parent meeting)
- `text` (str, required): Action item description
- `assignee` (str, optional): Person assigned to the action
- `due_date` (str, optional): Due date (may be in various formats, e.g., "15 January 2025")
- `status` (str, required): Status - "todo", "in progress", "done", or "cancelled"

**Validation Rules**:
- `text` must be non-empty string
- `status` must be one of: "todo", "in progress", "done", "cancelled"
- `meeting_id` must reference a valid meeting
- `due_date` is optional but should be parseable if present

**Normalization**:
- Trim whitespace from text and assignee
- Normalize status value (case-insensitive matching, handle variations)
- Parse due_date to datetime if possible, otherwise keep as string for display

**Relationships**:
- Many-to-one with Meeting (many action items belong to one meeting)
- Many-to-one with Workgroup (many action items belong to one workgroup)
- Many-to-one with Person (many action items assigned to one person)

### 5. Person

**Purpose**: Represents a community member.

**Fields**:
- `name` (str, required): Person's name (normalized)
- `workgroups` (set[str], computed): Set of workgroup IDs this person participates in
- `meetings_attended` (list[str], computed): List of meeting IDs this person attended
- `action_items_assigned` (list[str], computed): List of action item IDs assigned to this person
- `roles` (dict, computed): Dictionary of roles: {workgroup_id: [host, documenter, participant]}

**Validation Rules**:
- `name` must be non-empty string after normalization

**Normalization**:
- Normalize name variations (handle brackets, aliases, case variations)
- Extract from: meetingInfo.host, meetingInfo.documenter, meetingInfo.peoplePresent, actionItems[].assignee
- Handle name variations like "Stephen [QADAO]" → normalize to consistent format

**Relationships**:
- Many-to-many with Workgroup (people participate in multiple workgroups)
- Many-to-many with Meeting (people attend multiple meetings)
- One-to-many with ActionItem (people can have multiple action items)

### 6. Topic

**Purpose**: Represents a subject or theme discussed in meetings.

**Fields**:
- `name` (str, required): Topic name (normalized)
- `meetings` (list[str], computed): List of meeting IDs where this topic was discussed
- `workgroups` (set[str], computed): Set of workgroup IDs that discussed this topic
- `co_occurrences` (dict, computed): Dictionary of topics that co-occur: {topic_name: count}

**Validation Rules**:
- `name` must be non-empty string after normalization

**Normalization**:
- Parse from tags.topicsCovered (comma-separated string)
- Normalize topic names (trim whitespace, handle case variations for matching)
- Lowercase for matching, preserve original case for display

**Relationships**:
- Many-to-many with Meeting (topics appear in multiple meetings)
- Many-to-many with Workgroup (topics discussed by multiple workgroups)
- Many-to-many with Topic (topics co-occur with other topics)

## Data Flow

### 1. JSON Parsing (FR-001, FR-002)

```
JSON File → Parser → Normalized Data Models
```

**Parser Responsibilities**:
- Load JSON file (meeting-summaries-array-3.json)
- Parse each meeting record
- Normalize data (handle missing fields, parse strings, convert types)
- Build entity relationships
- Handle errors gracefully (malformed JSON, missing required fields)

**Error Handling**:
- Log warnings for missing optional fields
- Skip malformed meetings with error logging
- Continue processing remaining meetings

### 2. Data Normalization (FR-002)

**Normalization Steps**:
1. Parse dates: Convert ISO date strings to datetime objects
2. Parse strings: Split comma-separated strings (peoplePresent, topicsCovered) into lists
3. Normalize names: Handle name variations and aliases
4. Normalize topics: Trim, lowercase for matching, preserve original for display
5. Handle variations: Convert narrative to discussionPoints format, merge meetingTopics
6. Generate IDs: Create unique identifiers for entities

### 3. Data Access Patterns

**Filtering** (FR-007, FR-008, FR-009):
- Filter by workgroup: `meetings[meetings.workgroup == selected_workgroup]`
- Filter by date range: `meetings[(meetings.date >= start) & (meetings.date <= end)]`
- Filter by tags: `meetings[meetings.topics_covered.apply(lambda x: tag in x)]`
- Combine filters: Apply all filters with AND logic

**Aggregation** (FR-011, FR-012):
- Aggregate decisions: Flatten all decisions from all meetings, add workgroup/date context
- Aggregate action items: Flatten all action items from all meetings, add workgroup/date context
- Filter aggregated data: Apply filters (workgroup, assignee, status, date range)

**Graph Generation** (FR-017, FR-018):
- People-Workgroups graph: Nodes = people + workgroups, Edges = participation
- Topic co-occurrence graph: Nodes = topics, Edges = co-occurrence in same meetings
- Build NetworkX graph from relationships
- Convert to Plotly format for visualization

## Validation Schema

### JSON Schema (for input validation)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["workgroup", "workgroup_id", "meetingInfo", "type", "noSummaryGiven", "canceledSummary"],
    "properties": {
      "workgroup": {"type": "string"},
      "workgroup_id": {"type": "string", "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"},
      "meetingInfo": {
        "type": "object",
        "required": ["date"],
        "properties": {
          "date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
          "host": {"type": "string"},
          "documenter": {"type": "string"},
          "peoplePresent": {"type": "string"},
          "purpose": {"type": "string"}
        }
      },
      "agendaItems": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "actionItems": {"type": "array"},
            "decisionItems": {"type": "array"},
            "discussionPoints": {"type": "array"},
            "narrative": {"type": "string"}
          }
        }
      },
      "tags": {
        "type": "object",
        "properties": {
          "topicsCovered": {"type": "string"},
          "emotions": {"type": "string"}
        }
      }
    }
  }
}
```

## Performance Considerations

- **Caching**: Cache parsed and normalized data using Streamlit's `st.cache_data` to avoid re-parsing on every interaction
- **Lazy Loading**: Load graph visualizations only when graph explorer view is selected
- **Indexing**: Use pandas DataFrame indexing for fast filtering operations
- **Memory**: Store normalized data in memory (pandas DataFrame) for fast access, designed to handle 10,000 meetings

## Attribution Preservation (FR-022)

All attribution metadata is preserved in the data models:
- `host` and `documenter` fields in Meeting entity
- Displayed prominently in UI
- Included in exports (FR-024)

## Export Formats (FR-024)

**Plain Text Export**:
- Meetings: Tab-separated format with all fields
- Decisions: Tab-separated format with workgroup, date, decision, rationale, effect
- Action Items: Tab-separated format with workgroup, date, assignee, text, status, due_date

**CSV Export**:
- Same structure as plain text, CSV format

**JSON Export**:
- Normalized JSON structure matching data models

