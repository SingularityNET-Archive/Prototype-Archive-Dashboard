<!--
Sync Impact Report:
Version change: N/A → 1.0.0 (initial constitution)
Modified principles: N/A (all new)
Added sections: Mission, Core Principles (5), Governance
Removed sections: N/A
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section exists, no changes needed
  ✅ spec-template.md - No constitution references found, no changes needed
  ✅ tasks-template.md - No constitution references found, no changes needed
Follow-up TODOs: None
-->

# Prototype Archive Dashboard Constitution

## Mission

To make the collective memory of the community (meeting records, decisions, and actions) accessible, searchable, and explorable through a transparent, open-source dashboard.

## Core Principles

### I. Transparency

All data, schemas, and transformation scripts MUST be viewable in the repository. No hidden data processing or opaque transformations are permitted. Rationale: Community trust requires full visibility into how data is handled and presented.

### II. Interoperability

Data structures MUST align with community-driven schemas (JSON, CSV, GraphQL). The dashboard MUST support standard formats for data import and export. Rationale: Enables integration with other community tools and ensures long-term data portability.

### III. Accountability

Changes to the dashboard logic (e.g., filtering or data transformation) MUST be logged and version-controlled in GitHub Issues and PRs. All modifications to data processing, filtering rules, or display logic require documented justification. Rationale: Ensures traceability of decisions and allows community review of changes that affect data presentation.

### IV. Accessibility

UI MUST support non-technical users with clear labels, tooltips, and plain-text exports. Interface design MUST prioritize clarity and ease of use over technical sophistication. Rationale: The dashboard serves the entire community, not just technical members.

### V. Ethical AI Use

If any LLM or graph reasoning is used, its boundaries, datasets, and contextual assumptions MUST be documented (e.g., via a context.md file). AI-assisted features require explicit documentation of limitations, training data sources, and decision-making processes. Rationale: Prevents misuse and ensures users understand the capabilities and limitations of AI features.

## Governance

### Spec Review Board

Contributors approve any new data schema or feature via a pull request linked to a GitHub Issue. All schema changes and feature additions require community review before implementation.

### Change Protocol

No change merges without:

- JSON schema validation
- Updated documentation
- Passing dashboard tests

All PRs must demonstrate compliance with these requirements before merge approval.

### Licensing & Attribution

MUST preserve attribution of meeting documenters and workgroups as seen in meetingInfo. All meeting records retain their original attribution metadata, and the dashboard displays this information prominently.

**Version**: 1.0.0 | **Ratified**: 2025-11-07 | **Last Amended**: 2025-11-07
