# Implementation Plan: Meeting Archive Dashboard

**Branch**: `001-archive-dashboard` | **Date**: 2025-11-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-archive-dashboard/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

A modular, Python-based web dashboard for browsing workgroup meeting archives. The dashboard loads JSON archive data, normalizes it, and provides interactive interfaces for browsing by workgroup, filtering by date/tags, tracking decisions and action items, and exploring relationships via graph visualizations. The implementation will use a Python web framework (Streamlit, Dash, or Flask with Plotly) to create an accessible, non-technical-user-friendly interface that preserves attribution and supports data export.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: streamlit, pandas, networkx, plotly, python-dateutil, pytest  
**Storage**: File-based (JSON archive file, no database required for MVP)  
**Testing**: pytest with contract tests, unit tests, and integration tests  
**Target Platform**: Web browser (desktop and mobile responsive)  
**Project Type**: Web application (single-page dashboard with multiple views using Streamlit)  
**Performance Goals**: Load workgroup meetings within 3 seconds, filter results within 2 seconds, render graph visualizations for 100 workgroups/1000 people within 10 seconds (per SC-001, SC-002, SC-006)  
**Constraints**: Must handle JSON files up to 10,000 meetings without performance degradation (SC-009), must preserve all attribution metadata (FR-022), must support plain-text export (FR-024)  
**Scale/Scope**: 120 meetings initially (current JSON), designed to scale to 10,000 meetings, 16 workgroups, multiple views (workgroup browser, decision tracker, graph explorer)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Check ✅ PASS

**Transparency**: ✅ All data schemas and transformation scripts will be documented and viewable in repository (data-model.md, parser code in src/)  
**Interoperability**: ✅ Data structures align with community schemas (JSON input, JSON/CSV export support per FR-024, GraphQL export possible)  
**Accountability**: ✅ Changes will be logged in GitHub Issues/PRs with justification (standard workflow)  
**Accessibility**: ✅ UI design supports non-technical users (clear labels, tooltips per FR-023, plain-text exports per FR-024)  
**Ethical AI Use**: ✅ No AI/LLM usage planned for MVP (graph visualizations use deterministic algorithms, not AI)  
**Change Protocol**: ✅ JSON schema validation (data-model.md will include schema), documentation updates (all artifacts tracked), tests included (pytest test suite)

### Post-Design Check ✅ PASS

**Transparency**: ✅ **VERIFIED** - data-model.md documents all schemas, contracts/ define transformation logic, parser code will be in src/parsers/  
**Interoperability**: ✅ **VERIFIED** - JSON input schema defined, CSV/JSON export contracts specified (export-service.md), data structures align with community schemas  
**Accountability**: ✅ **VERIFIED** - All design decisions documented in research.md, changes tracked via Git/PRs  
**Accessibility**: ✅ **VERIFIED** - Streamlit framework provides built-in accessibility features, export contracts ensure plain-text support (FR-024)  
**Ethical AI Use**: ✅ **VERIFIED** - No AI/LLM usage in design (NetworkX + Plotly for deterministic graph algorithms)  
**Change Protocol**: ✅ **VERIFIED** - JSON schema defined in data-model.md, contract tests specified in contracts/, pytest test suite planned

**Gate Status**: ✅ **PASS** - All constitution requirements verified and met in Phase 1 design.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── models/              # Data models (Meeting, Workgroup, Decision, ActionItem, Person, Topic)
├── parsers/            # JSON parsing and data normalization
├── services/           # Business logic (filtering, aggregation, graph generation)
├── ui/                 # Dashboard UI components (framework-specific)
└── utils/              # Utility functions (date parsing, text normalization, export)

tests/
├── contract/           # Contract tests for data parsing and normalization
├── integration/       # Integration tests for end-to-end workflows
└── unit/              # Unit tests for models, services, utilities

data/
└── meeting-summaries-array-3.json  # Input JSON archive file

docs/
└── schemas/            # JSON schema definitions for validation
```

**Structure Decision**: Single Python project structure chosen because:
- Dashboard is a single web application (no separate frontend/backend needed for Streamlit/Dash)
- All components share the same data models and services
- Simpler deployment and development workflow
- Aligns with Python web dashboard frameworks (Streamlit/Dash are single-app frameworks)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
