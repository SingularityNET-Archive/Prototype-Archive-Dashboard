# Tasks: Meeting Archive Dashboard

**Input**: Design documents from `/specs/001-archive-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Contract tests, unit tests, and integration tests are included to ensure data correctness and performance requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow the single project structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan (src/models/, src/parsers/, src/services/, src/ui/, src/utils/, tests/contract/, tests/integration/, tests/unit/, data/, docs/schemas/)
- [x] T002 Initialize Python 3.11+ project with dependencies (streamlit, pandas, networkx, plotly, python-dateutil, pytest) in requirements.txt
- [x] T003 [P] Configure pytest in pytest.ini or pyproject.toml
- [x] T004 [P] Create .gitignore for Python project (venv/, __pycache__/, *.pyc, .pytest_cache/, etc.)
- [x] T005 [P] Create README.md with project description and setup instructions
- [x] T006 Copy meeting-summaries-array-3.json to data/ directory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create base Meeting model in src/models/meeting.py with all fields from data-model.md (id, workgroup, workgroup_id, date, host, documenter, people_present, purpose, type_of_meeting, meeting_video_link, working_docs, action_items, decisions, discussion_points, topics_covered, emotions, type, no_summary_given, canceled_summary)
- [x] T008 Create base Workgroup model in src/models/workgroup.py with fields (id, name, meeting_count, meetings)
- [x] T009 [P] Create utility functions for date parsing in src/utils/date_parser.py using dateutil.parser and pandas.to_datetime
- [x] T010 [P] Create utility functions for text normalization in src/utils/text_normalizer.py (comma-separated string parsing, whitespace trimming, name normalization)
- [x] T011 Implement data parser service in src/parsers/data_parser.py with load_archive() and normalize_meeting() functions per data-parser.md contract
- [x] T012 Add error handling and logging infrastructure in src/utils/logger.py
- [x] T013 [P] Create contract test for data parser in tests/contract/test_data_parser.py (valid JSON parsing, missing optional fields, date parsing, string parsing, name normalization, error handling, attribution preservation)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Load and Browse Meeting Archives by Workgroup (Priority: P1) 🎯 MVP

**Goal**: Enable users to select a workgroup and view all meetings for that workgroup in chronological order with basic meeting information displayed.

**Independent Test**: Load JSON file, display list of unique workgroups, select one workgroup, verify all meetings for that workgroup are displayed with correct metadata (date, host, documenter, purpose, people present) in chronological order.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T014 [P] [US1] Create contract test for workgroup list extraction in tests/contract/test_workgroup_service.py
- [x] T015 [P] [US1] Create integration test for workgroup browser workflow in tests/integration/test_workgroup_browser.py (load JSON → extract workgroups → select workgroup → view meetings)

### Implementation for User Story 1

- [x] T016 [US1] Create WorkgroupService in src/services/workgroup_service.py with get_all_workgroups() method that extracts unique workgroups from meetings
- [x] T017 [US1] Create WorkgroupService method get_meetings_by_workgroup(workgroup_name: str) -> List[Meeting] in src/services/workgroup_service.py
- [x] T018 [US1] Add chronological sorting (newest-first or oldest-first) to get_meetings_by_workgroup() in src/services/workgroup_service.py
- [x] T019 [US1] Create Streamlit UI component for workgroup selection in src/ui/components/workgroup_selector.py with st.selectbox for workgroup list
- [x] T020 [US1] Create Streamlit UI component for meeting list display in src/ui/components/meeting_list.py showing date, host, documenter, purpose, people present
- [x] T021 [US1] Create main dashboard page in src/ui/dashboard.py integrating workgroup selector and meeting list components
- [x] T022 [US1] Add Streamlit caching decorator @st.cache_data to data loading function in src/ui/dashboard.py for performance (SC-001)
- [x] T023 [US1] Add error handling for missing optional fields in meeting display (handle None values gracefully) in src/ui/components/meeting_list.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can select a workgroup and view all meetings with correct metadata.

---

## Phase 4: User Story 2 - Filter Meetings by Date Range and Tags (Priority: P2)

**Goal**: Enable users to filter meetings by date range and/or topic tags to find relevant meetings efficiently.

**Independent Test**: Apply date range filters and tag filters independently, verify only meetings matching criteria are displayed. Test combined filters (date + tags) and clear filters functionality.

### Tests for User Story 2

- [ ] T024 [P] [US2] Create contract test for filter service in tests/contract/test_filter_service.py (workgroup filter, date range filter, tag filter, combined filters, empty results, no filters, performance)
- [ ] T025 [P] [US2] Create integration test for filtering workflow in tests/integration/test_meeting_filters.py (apply date filter → apply tag filter → combine filters → clear filters)

### Implementation for User Story 2

- [ ] T026 [US2] Create Topic model in src/models/topic.py with fields (name, meetings, workgroups, co_occurrences) per data-model.md
- [ ] T027 [US2] Create FilterService in src/services/filter_service.py with filter_meetings() method per filter-service.md contract (workgroup, start_date, end_date, tags parameters)
- [ ] T028 [US2] Implement date range filtering logic in FilterService.filter_meetings() using pandas datetime comparison
- [ ] T029 [US2] Implement tag filtering logic in FilterService.filter_meetings() checking if any tag in tags list appears in meeting.topics_covered
- [ ] T030 [US2] Implement combined filter logic (AND logic for all filters) in FilterService.filter_meetings()
- [ ] T031 [US2] Create Streamlit UI component for date range filter in src/ui/components/date_filter.py with st.date_input for start and end dates
- [ ] T032 [US2] Create Streamlit UI component for tag filter in src/ui/components/tag_filter.py with st.multiselect showing all available topics
- [ ] T033 [US2] Create utility function to extract all unique topics from meetings in src/utils/topic_extractor.py
- [ ] T034 [US2] Integrate date and tag filters into main dashboard in src/ui/dashboard.py (add to sidebar)
- [ ] T035 [US2] Add "Clear All Filters" button in src/ui/dashboard.py that resets all filter values
- [ ] T036 [US2] Update meeting list display to show filtered results in src/ui/components/meeting_list.py
- [ ] T037 [US2] Add performance optimization for filtering (use pandas DataFrame for efficient filtering) in src/services/filter_service.py to meet SC-002 and SC-003 (< 2 seconds)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can browse by workgroup and filter by date range and tags.

---

## Phase 5: User Story 3 - Track Decisions and Action Items Across Meetings (Priority: P3)

**Goal**: Enable users to view aggregated lists of all decisions and action items with filtering capabilities.

**Independent Test**: Display aggregated decisions and action items, filter by workgroup, assignee, status, and date range. Verify data accurately reflects source meetings.

### Tests for User Story 3

- [ ] T038 [P] [US3] Create contract test for aggregation service in tests/contract/test_aggregation_service.py (decision aggregation, action item aggregation, context preservation, empty meetings, performance)
- [ ] T039 [P] [US3] Create contract test for decision and action item filtering in tests/contract/test_filter_service.py (filter_decisions, filter_action_items)
- [ ] T040 [P] [US3] Create integration test for decision tracker workflow in tests/integration/test_decision_tracker.py (aggregate decisions → filter by workgroup → display)
- [ ] T041 [P] [US3] Create integration test for action item tracker workflow in tests/integration/test_action_item_tracker.py (aggregate action items → filter by assignee/status → display)

### Implementation for User Story 3

- [ ] T042 [US3] Create Decision model in src/models/decision.py with fields (id, meeting_id, workgroup, date, decision_text, rationale, effect, opposing) per data-model.md
- [ ] T043 [US3] Create ActionItem model in src/models/action_item.py with fields (id, meeting_id, workgroup, date, text, assignee, due_date, status) per data-model.md
- [ ] T044 [US3] Update Meeting model to include decisions and action_items as lists of Decision and ActionItem objects in src/models/meeting.py
- [ ] T045 [US3] Create AggregationService in src/services/aggregation_service.py with aggregate_decisions() and aggregate_action_items() methods per aggregation-service.md contract
- [ ] T046 [US3] Implement aggregate_decisions() to flatten all decisions from all meetings with workgroup and date context in src/services/aggregation_service.py
- [ ] T047 [US3] Implement aggregate_action_items() to flatten all action items from all meetings with workgroup and date context in src/services/aggregation_service.py
- [ ] T048 [US3] Extend FilterService with filter_decisions() method per filter-service.md contract in src/services/filter_service.py
- [ ] T049 [US3] Extend FilterService with filter_action_items() method per filter-service.md contract in src/services/filter_service.py
- [ ] T050 [US3] Create Streamlit UI component for decision tracker in src/ui/components/decision_tracker.py displaying decisions with workgroup, date, decision text, rationale, effect
- [ ] T051 [US3] Create Streamlit UI component for action item tracker in src/ui/components/action_item_tracker.py displaying action items with assignee, due date, status, workgroup
- [ ] T052 [US3] Add workgroup filter to decision tracker UI in src/ui/components/decision_tracker.py
- [ ] T053 [US3] Add assignee filter to action item tracker UI in src/ui/components/action_item_tracker.py
- [ ] T054 [US3] Add status filter (todo/in progress/done/cancelled) to action item tracker UI in src/ui/components/action_item_tracker.py
- [ ] T055 [US3] Add date range filter to action item tracker UI (based on due date or meeting date) in src/ui/components/action_item_tracker.py
- [ ] T056 [US3] Integrate decision tracker and action item tracker as tabs in main dashboard in src/ui/dashboard.py
- [ ] T057 [US3] Add performance optimization for aggregation (use pandas for efficient flattening) in src/services/aggregation_service.py to meet SC-004 (< 5 seconds) and SC-005 (< 2 seconds)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. Users can browse meetings, filter them, and track decisions and action items.

---

## Phase 6: User Story 4 - Explore Relationships in Meeting Data (Priority: P4)

**Goal**: Enable users to view graph visualizations showing relationships between people, topics, and workgroups.

**Independent Test**: Generate graph visualizations showing people-workgroup relationships and topic co-occurrence. Verify relationships accurately reflect meeting data. Test node interaction and graph filtering.

### Tests for User Story 4

- [ ] T058 [P] [US4] Create contract test for graph service in tests/contract/test_graph_service.py (people-workgroups graph, topic co-occurrence graph, graph filtering, empty data, performance)
- [ ] T059 [P] [US4] Create integration test for graph explorer workflow in tests/integration/test_graph_explorer.py (build graph → convert to Plotly → display → filter → interact with nodes)

### Implementation for User Story 4

- [ ] T060 [US4] Create Person model in src/models/person.py with fields (name, workgroups, meetings_attended, action_items_assigned, roles) per data-model.md
- [ ] T061 [US4] Create utility function to extract and normalize people from meetings in src/utils/person_extractor.py (from host, documenter, peoplePresent, actionItems assignee)
- [ ] T062 [US4] Create GraphService in src/services/graph_service.py with build_people_workgroups_graph() method per graph-service.md contract
- [ ] T063 [US4] Create GraphService method build_topic_cooccurrence_graph() per graph-service.md contract in src/services/graph_service.py
- [ ] T064 [US4] Implement build_people_workgroups_graph() using NetworkX to create graph with people and workgroups as nodes, participation as edges in src/services/graph_service.py
- [ ] T065 [US4] Implement build_topic_cooccurrence_graph() using NetworkX to create graph with topics as nodes, co-occurrence in same meetings as edges in src/services/graph_service.py
- [ ] T066 [US4] Create GraphService method graph_to_plotly() to convert NetworkX graph to Plotly figure per graph-service.md contract in src/services/graph_service.py
- [ ] T067 [US4] Create GraphService method filter_graph() to filter graph by workgroup or date range per graph-service.md contract in src/services/graph_service.py
- [ ] T068 [US4] Create Streamlit UI component for graph explorer in src/ui/components/graph_explorer.py with view selector (People and Workgroups / Topics)
- [ ] T069 [US4] Add Plotly graph visualization to graph explorer using st.plotly_chart() in src/ui/components/graph_explorer.py
- [ ] T070 [US4] Implement node click interaction to show detailed information (meetings, relationships) in src/ui/components/graph_explorer.py
- [ ] T071 [US4] Add graph filtering controls (date range, workgroup) to graph explorer UI in src/ui/components/graph_explorer.py
- [ ] T072 [US4] Integrate graph explorer as a tab in main dashboard in src/ui/dashboard.py
- [ ] T073 [US4] Add lazy loading for graph visualizations (only build when graph explorer tab is selected) in src/ui/components/graph_explorer.py for performance
- [ ] T074 [US4] Add performance optimization for graph rendering (efficient NetworkX graph construction, Plotly conversion) in src/services/graph_service.py to meet SC-006 (< 10 seconds for 100 workgroups and 1000 people)

**Checkpoint**: All user stories should now be independently functional. Users can browse meetings, filter them, track decisions/action items, and explore relationships via graphs.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T075 [P] Create ExportService in src/services/export_service.py with export_meetings_plain_text(), export_decisions_plain_text(), export_action_items_plain_text() methods per export-service.md contract
- [ ] T076 [P] Add export_to_csv() and export_to_json() methods to ExportService in src/services/export_service.py
- [ ] T077 [P] Add export buttons to all views (workgroup browser, decision tracker, action item tracker) in src/ui/components/ with st.download_button
- [ ] T078 [P] Create contract test for export service in tests/contract/test_export_service.py (plain text export, CSV export, JSON export, attribution preservation, empty data, special characters)
- [ ] T079 [P] Add tooltips and clear labels to all UI components per FR-023 (Accessibility) in src/ui/components/
- [ ] T080 [P] Add comprehensive error handling and user-friendly error messages throughout the application
- [ ] T081 [P] Add logging for all major operations (data loading, filtering, aggregation, graph generation) in src/services/
- [ ] T082 [P] Create unit tests for all models in tests/unit/test_models.py (Meeting, Workgroup, Decision, ActionItem, Person, Topic)
- [ ] T083 [P] Create unit tests for utility functions in tests/unit/test_utils.py (date_parser, text_normalizer, topic_extractor, person_extractor)
- [ ] T084 Add performance tests to verify SC-001 through SC-006 timing requirements in tests/integration/test_performance.py
- [ ] T085 Add data validation tests for edge cases (malformed JSON, missing fields, special characters) in tests/contract/test_data_parser.py
- [ ] T086 Update README.md with usage instructions and quickstart guide
- [ ] T087 Create JSON schema file for input validation in docs/schemas/meeting-archive-schema.json per data-model.md
- [ ] T088 Run quickstart.md validation to ensure all setup steps work correctly
- [ ] T089 Code cleanup and refactoring (remove unused code, improve code organization)
- [ ] T090 Add docstrings to all public functions and classes following Python conventions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for Topic model and FilterService integration
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 for base models, can use US2 FilterService
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on US1 for base models, can use US2 FilterService for graph filtering

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005)
- All Foundational tasks marked [P] can run in parallel (T009, T010, T013)
- Once Foundational phase completes, user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for workgroup list extraction in tests/contract/test_workgroup_service.py"
Task: "Integration test for workgroup browser workflow in tests/integration/test_workgroup_browser.py"

# Launch UI components for User Story 1 together (after service is done):
Task: "Create Streamlit UI component for workgroup selection in src/ui/components/workgroup_selector.py"
Task: "Create Streamlit UI component for meeting list display in src/ui/components/meeting_list.py"
```

## Parallel Example: User Story 2

```bash
# Launch models and services for User Story 2 together:
Task: "Create Topic model in src/models/topic.py"
Task: "Create FilterService in src/services/filter_service.py"

# Launch UI components for User Story 2 together (after service is done):
Task: "Create Streamlit UI component for date range filter in src/ui/components/date_filter.py"
Task: "Create Streamlit UI component for tag filter in src/ui/components/tag_filter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add Polish phase → Final release
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MVP)
   - Developer B: User Story 2 (can start after US1 models are done)
   - Developer C: User Story 3 (can start after US1 models are done)
   - Developer D: User Story 4 (can start after US1 models are done)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths are relative to repository root
- Performance requirements (SC-001 through SC-006) must be verified in tests

