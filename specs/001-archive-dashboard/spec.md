# Feature Specification: Meeting Archive Dashboard

**Feature Branch**: `001-archive-dashboard`  
**Created**: 2025-11-07  
**Status**: Draft  
**Input**: User description: "A modular, Python-based dashboard for browsing workgroup meeting archives. Input: JSON archive (meeting-summaries-array-3.json). Output: Interactive interface (Streamlit, Dash, or Flask with Plotly). Key Components: Data parser (loads JSON and normalizes it), Workgroup browser (filters by group, date, or tags), Decision tracker (aggregates decisions and action items), Graph explorer (shows relationships among people, topics, and workgroups)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Load and Browse Meeting Archives by Workgroup (Priority: P1)

A community member wants to explore meeting records from specific workgroups to understand what each group has been discussing. They can select a workgroup from a list and view all meetings for that workgroup in chronological order, with basic meeting information (date, host, documenter, purpose) clearly displayed.

**Why this priority**: This is the foundational capability that enables users to access the archive data. Without the ability to load and view meetings by workgroup, none of the other features can be demonstrated or tested. It provides immediate value by making meeting records accessible.

**Independent Test**: Can be fully tested by loading the JSON file, displaying a list of workgroups, selecting one workgroup, and verifying that all meetings for that workgroup are displayed with correct metadata. This delivers value by enabling users to browse meeting history for any workgroup.

**Acceptance Scenarios**:

1. **Given** the dashboard has loaded the JSON archive file, **When** a user views the workgroup selection interface, **Then** they see a list of all unique workgroups from the archive
2. **Given** a user has selected a workgroup, **When** they view the meeting list, **Then** they see all meetings for that workgroup displayed in chronological order (newest first or oldest first)
3. **Given** a user is viewing a meeting in the list, **When** they examine the meeting details, **Then** they see the date, host, documenter, purpose, and people present
4. **Given** the JSON file contains meetings with missing optional fields, **When** the dashboard displays those meetings, **Then** it handles missing data gracefully without errors

---

### User Story 2 - Filter Meetings by Date Range and Tags (Priority: P2)

A community member wants to find meetings that occurred during a specific time period or that covered particular topics. They can filter meetings by selecting a date range or by choosing one or more tags from the available topics.

**Why this priority**: Filtering is essential for navigating large archives efficiently. Users need to narrow down results to find relevant meetings without scrolling through hundreds of entries. This significantly improves usability and makes the dashboard practical for real-world use.

**Independent Test**: Can be fully tested by applying date range filters and tag filters independently, verifying that only meetings matching the criteria are displayed. This delivers value by enabling users to quickly find meetings relevant to their interests or time period.

**Acceptance Scenarios**:

1. **Given** a user is viewing meetings, **When** they select a start date and end date, **Then** only meetings within that date range are displayed
2. **Given** a user is viewing meetings, **When** they select one or more topic tags, **Then** only meetings containing those tags in their topicsCovered field are displayed
3. **Given** a user has applied both date and tag filters, **When** they view results, **Then** only meetings matching both criteria are displayed
4. **Given** a user has applied filters, **When** they clear all filters, **Then** all meetings are displayed again

---

### User Story 3 - Track Decisions and Action Items Across Meetings (Priority: P3)

A community member wants to understand what decisions have been made and what action items are pending across workgroups. They can view aggregated lists of all decisions and action items, with the ability to filter by workgroup, assignee, status, or date range.

**Why this priority**: Decision tracking provides critical value for community governance and accountability. Users need to see what has been decided, what actions are pending, and who is responsible. This transforms the archive from a passive record into an active governance tool.

**Independent Test**: Can be fully tested by displaying aggregated decisions and action items, filtering by various criteria, and verifying that the data accurately reflects the source meetings. This delivers value by enabling users to track community decisions and follow up on action items.

**Acceptance Scenarios**:

1. **Given** a user is viewing the decision tracker, **When** they see the decisions list, **Then** all decisions from all meetings are displayed with workgroup, date, decision text, rationale, and effect
2. **Given** a user is viewing the action items list, **When** they see the action items, **Then** all action items are displayed with assignee, due date, status (todo/in progress/done), and associated workgroup
3. **Given** a user wants to find action items for a specific person, **When** they filter by assignee, **Then** only action items assigned to that person are displayed
4. **Given** a user wants to see pending work, **When** they filter action items by status "todo" or "in progress", **Then** only incomplete action items are displayed
5. **Given** a user is viewing decisions, **When** they filter by workgroup, **Then** only decisions from that workgroup are displayed

---

### User Story 4 - Explore Relationships in Meeting Data (Priority: P4)

A community member wants to understand connections between people, topics, and workgroups across the archive. They can view a graph visualization showing how people participate in different workgroups, which topics appear together, and how workgroups relate through shared participants or topics.

**Why this priority**: Graph exploration provides advanced analytical capabilities that reveal patterns and relationships not visible in linear lists. While valuable for power users and analysis, it's not essential for basic archive browsing, making it a lower priority than core browsing and filtering features.

**Independent Test**: Can be fully tested by generating graph visualizations showing people-workgroup relationships, topic co-occurrence, and workgroup connections, verifying that the relationships accurately reflect the meeting data. This delivers value by enabling users to discover patterns and connections in the community's activities.

**Acceptance Scenarios**:

1. **Given** a user is viewing the graph explorer, **When** they select "People and Workgroups" view, **Then** they see a graph with people and workgroups as nodes, connected by edges showing participation
2. **Given** a user is viewing the graph explorer, **When** they select "Topics" view, **Then** they see topics as nodes, connected by edges showing co-occurrence in the same meetings
3. **Given** a user clicks on a person node in the graph, **When** they view details, **Then** they see all workgroups that person has participated in and all meetings they attended
4. **Given** a user clicks on a topic node, **When** they view details, **Then** they see all meetings where that topic was discussed and which workgroups covered it
5. **Given** the graph contains many nodes, **When** a user applies filters (e.g., date range or specific workgroups), **Then** the graph updates to show only relevant relationships

---

### Edge Cases

- What happens when the JSON file is malformed or missing required fields?
- How does the system handle meetings with no agenda items, decisions, or action items?
- What happens when a user filters by a date range that contains no meetings?
- How does the system handle duplicate workgroup names or inconsistent naming?
- What happens when action items have missing assignees or due dates?
- How does the graph explorer handle workgroups or people with no connections?
- What happens when the JSON file is very large (thousands of meetings)?
- How does the system handle special characters in names, topics, or decision text?
- What happens when meetings have conflicting or inconsistent date formats?
- How does the system handle meetings marked as canceled or with noSummaryGiven flags?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load and parse the JSON archive file (meeting-summaries-array-3.json) without errors
- **FR-002**: System MUST normalize the loaded data to handle variations in structure and missing optional fields
- **FR-003**: System MUST display a list of all unique workgroups found in the archive
- **FR-004**: System MUST allow users to select a workgroup and view all meetings for that workgroup
- **FR-005**: System MUST display meeting information including date, host, documenter, purpose, and people present
- **FR-006**: System MUST display meetings in chronological order (configurable as newest-first or oldest-first)
- **FR-007**: System MUST allow users to filter meetings by date range (start date and end date)
- **FR-008**: System MUST allow users to filter meetings by one or more topic tags
- **FR-009**: System MUST support combining multiple filters (workgroup, date range, tags) simultaneously
- **FR-010**: System MUST allow users to clear all filters and return to viewing all meetings
- **FR-011**: System MUST aggregate and display all decisions from all meetings with workgroup, date, decision text, rationale, and effect
- **FR-012**: System MUST aggregate and display all action items with assignee, due date, status, and associated workgroup
- **FR-013**: System MUST allow users to filter decisions by workgroup
- **FR-014**: System MUST allow users to filter action items by assignee
- **FR-015**: System MUST allow users to filter action items by status (todo, in progress, done)
- **FR-016**: System MUST allow users to filter action items by date range (based on due date or meeting date)
- **FR-017**: System MUST generate graph visualizations showing relationships between people and workgroups
- **FR-018**: System MUST generate graph visualizations showing topic co-occurrence relationships
- **FR-019**: System MUST allow users to interact with graph nodes to view detailed information
- **FR-020**: System MUST allow users to filter graph visualizations by date range or workgroup
- **FR-021**: System MUST handle missing or null values in the JSON data gracefully without causing errors
- **FR-022**: System MUST preserve attribution information (documenter, host) from meetingInfo as required by constitution
- **FR-023**: System MUST provide an interactive interface that supports non-technical users with clear labels and tooltips
- **FR-024**: System MUST support exporting filtered results or aggregated data in plain-text format

### Key Entities *(include if feature involves data)*

- **Meeting**: Represents a single meeting record with workgroup, meetingInfo (date, host, documenter, peoplePresent, purpose, links), agendaItems (actionItems, decisionItems, discussionPoints), tags (topicsCovered, emotions), and metadata (type, noSummaryGiven, canceledSummary)

- **Workgroup**: Represents a community workgroup with a unique identifier and name, associated with multiple meetings

- **Decision**: Represents a decision made in a meeting with decision text, rationale, effect (affectsOnlyThisWorkgroup/mayAffectOtherPeople), opposing views, and association to a specific meeting and workgroup

- **Action Item**: Represents a task or action item from a meeting with text, assignee, due date, status (todo/in progress/done), and association to a specific meeting and workgroup

- **Person**: Represents a community member who may appear as host, documenter, or participant in meetings, or as assignee of action items

- **Topic**: Represents a subject or theme discussed in meetings, extracted from tags.topicsCovered, with relationships to meetings and workgroups

## Assumptions

- The JSON archive file (meeting-summaries-array-3.json) follows a consistent structure with the fields described in Key Entities
- Meeting dates are in ISO format (YYYY-MM-DD) or can be reliably parsed
- Workgroup names and IDs are consistent across meetings (same workgroup always uses same name/ID)
- Topic tags in topicsCovered are comma-separated strings that can be parsed and normalized
- Action item status values are standardized as "todo", "in progress", or "done"
- The dashboard will be accessed via web browser (desktop or mobile)
- Users have basic familiarity with web interfaces but may not be technical
- The JSON file will be updated periodically, and the dashboard should reload or refresh when new data is available

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can load and view meetings for any workgroup within 3 seconds of selecting the workgroup
- **SC-002**: Users can successfully filter meetings by date range and see only relevant results in under 2 seconds
- **SC-003**: Users can successfully filter meetings by tags and see only relevant results in under 2 seconds
- **SC-004**: Users can view aggregated decisions and action items for all workgroups within 5 seconds
- **SC-005**: Users can filter action items by assignee and status, finding specific items within 2 seconds
- **SC-006**: Graph visualizations render and display relationships for datasets with up to 100 workgroups and 1000 people within 10 seconds
- **SC-007**: 90% of users can successfully browse meetings by workgroup without assistance on first use
- **SC-008**: 85% of users can successfully apply filters (date range or tags) without assistance on first use
- **SC-009**: System handles JSON files containing up to 10,000 meetings without performance degradation
- **SC-010**: All meeting attribution information (documenter, host) is preserved and displayed correctly for 100% of meetings
