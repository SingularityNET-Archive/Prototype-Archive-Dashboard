"""Export service for exporting data in various formats."""

import json
import csv
import io
from typing import List, Any
from datetime import datetime

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.utils.logger import logger


class ExportService:
    """Service for exporting data in plain text, CSV, and JSON formats."""

    def __init__(self):
        """Initialize ExportService."""
        pass

    def export_meetings_plain_text(self, meetings: List[Meeting]) -> str:
        """Export meetings to plain text format (tab-separated).

        Includes all fields with attribution preservation (host, documenter).

        Args:
            meetings: List of Meeting objects to export

        Returns:
            Plain text string with tab-separated values
        """
        if not meetings:
            return ""

        # Header row
        headers = [
            "ID",
            "Workgroup",
            "Date",
            "Host",
            "Documenter",
            "Purpose",
            "Type of Meeting",
            "People Present",
            "Topics Covered",
            "Video Link",
        ]
        lines = ["\t".join(headers)]

        # Data rows
        for meeting in meetings:
            row = [
                meeting.id,
                meeting.workgroup,
                meeting.date.strftime("%Y-%m-%d") if meeting.date else "",
                meeting.host or "",
                meeting.documenter or "",
                meeting.purpose or "",
                meeting.type_of_meeting or "",
                ", ".join(meeting.people_present) if meeting.people_present else "",
                ", ".join(meeting.topics_covered) if meeting.topics_covered else "",
                meeting.meeting_video_link or "",
            ]
            # Escape tabs and newlines in data
            row = [str(field).replace("\t", " ").replace("\n", " ") for field in row]
            lines.append("\t".join(row))

        result = "\n".join(lines)
        logger.info(f"Exported {len(meetings)} meetings to plain text format")
        return result

    def export_decisions_plain_text(self, decisions: List[Decision]) -> str:
        """Export decisions to plain text format (tab-separated).

        Includes workgroup and date context with attribution.

        Args:
            decisions: List of Decision objects to export

        Returns:
            Plain text string with tab-separated values
        """
        if not decisions:
            return ""

        # Header row
        headers = [
            "ID",
            "Meeting ID",
            "Workgroup",
            "Date",
            "Decision Text",
            "Rationale",
            "Effect",
            "Opposing Views",
        ]
        lines = ["\t".join(headers)]

        # Data rows
        for decision in decisions:
            row = [
                decision.id,
                decision.meeting_id,
                decision.workgroup,
                decision.date.strftime("%Y-%m-%d") if decision.date else "",
                decision.decision_text,
                decision.rationale or "",
                decision.effect,
                decision.opposing or "",
            ]
            # Escape tabs and newlines in data
            row = [str(field).replace("\t", " ").replace("\n", " ") for field in row]
            lines.append("\t".join(row))

        result = "\n".join(lines)
        logger.info(f"Exported {len(decisions)} decisions to plain text format")
        return result

    def export_action_items_plain_text(self, action_items: List[ActionItem]) -> str:
        """Export action items to plain text format (tab-separated).

        Includes workgroup and date context with assignee information.

        Args:
            action_items: List of ActionItem objects to export

        Returns:
            Plain text string with tab-separated values
        """
        if not action_items:
            return ""

        # Header row
        headers = [
            "ID",
            "Meeting ID",
            "Workgroup",
            "Date",
            "Text",
            "Assignee",
            "Status",
            "Due Date",
        ]
        lines = ["\t".join(headers)]

        # Data rows
        for item in action_items:
            row = [
                item.id,
                item.meeting_id,
                item.workgroup,
                item.date.strftime("%Y-%m-%d") if item.date else "",
                item.text,
                item.assignee or "",
                item.status,
                item.due_date or "",
            ]
            # Escape tabs and newlines in data
            row = [str(field).replace("\t", " ").replace("\n", " ") for field in row]
            lines.append("\t".join(row))

        result = "\n".join(lines)
        logger.info(f"Exported {len(action_items)} action items to plain text format")
        return result

    def export_to_csv(self, data: List[Any], data_type: str = "meetings") -> bytes:
        """Export data to CSV format.

        Args:
            data: List of data objects to export (Meeting, Decision, or ActionItem)
            data_type: Type of data ("meetings", "decisions", or "action_items")

        Returns:
            CSV file as bytes for download
        """
        if not data:
            return b""

        output = io.StringIO()
        writer = csv.writer(output)

        if data_type == "meetings" and isinstance(data[0], Meeting):
            # Write header
            writer.writerow(
                [
                    "ID",
                    "Workgroup",
                    "Date",
                    "Host",
                    "Documenter",
                    "Purpose",
                    "Type of Meeting",
                    "People Present",
                    "Topics Covered",
                    "Video Link",
                ]
            )
            # Write data
            for meeting in data:
                writer.writerow(
                    [
                        meeting.id,
                        meeting.workgroup,
                        meeting.date.strftime("%Y-%m-%d") if meeting.date else "",
                        meeting.host or "",
                        meeting.documenter or "",
                        meeting.purpose or "",
                        meeting.type_of_meeting or "",
                        ", ".join(meeting.people_present) if meeting.people_present else "",
                        ", ".join(meeting.topics_covered) if meeting.topics_covered else "",
                        meeting.meeting_video_link or "",
                    ]
                )

        elif data_type == "decisions" and isinstance(data[0], Decision):
            # Write header
            writer.writerow(
                [
                    "ID",
                    "Meeting ID",
                    "Workgroup",
                    "Date",
                    "Decision Text",
                    "Rationale",
                    "Effect",
                    "Opposing Views",
                ]
            )
            # Write data
            for decision in data:
                writer.writerow(
                    [
                        decision.id,
                        decision.meeting_id,
                        decision.workgroup,
                        decision.date.strftime("%Y-%m-%d") if decision.date else "",
                        decision.decision_text,
                        decision.rationale or "",
                        decision.effect,
                        decision.opposing or "",
                    ]
                )

        elif data_type == "action_items" and isinstance(data[0], ActionItem):
            # Write header
            writer.writerow(
                [
                    "ID",
                    "Meeting ID",
                    "Workgroup",
                    "Date",
                    "Text",
                    "Assignee",
                    "Status",
                    "Due Date",
                ]
            )
            # Write data
            for item in data:
                writer.writerow(
                    [
                        item.id,
                        item.meeting_id,
                        item.workgroup,
                        item.date.strftime("%Y-%m-%d") if item.date else "",
                        item.text,
                        item.assignee or "",
                        item.status,
                        item.due_date or "",
                    ]
                )

        csv_string = output.getvalue()
        output.close()
        logger.info(f"Exported {len(data)} {data_type} to CSV format")
        return csv_string.encode("utf-8")

    def export_to_json(self, data: List[Any]) -> str:
        """Export data to JSON format.

        Args:
            data: List of data objects to export

        Returns:
            JSON string
        """
        if not data:
            return "[]"

        # Convert objects to dictionaries
        json_data = []
        for item in data:
            if isinstance(item, Meeting):
                json_data.append(
                    {
                        "id": item.id,
                        "workgroup": item.workgroup,
                        "workgroup_id": item.workgroup_id,
                        "date": item.date.isoformat() if item.date else None,
                        "host": item.host,
                        "documenter": item.documenter,
                        "purpose": item.purpose,
                        "type_of_meeting": item.type_of_meeting,
                        "people_present": item.people_present,
                        "topics_covered": item.topics_covered,
                        "meeting_video_link": item.meeting_video_link,
                    }
                )
            elif isinstance(item, Decision):
                json_data.append(
                    {
                        "id": item.id,
                        "meeting_id": item.meeting_id,
                        "workgroup": item.workgroup,
                        "date": item.date.isoformat() if item.date else None,
                        "decision_text": item.decision_text,
                        "rationale": item.rationale,
                        "effect": item.effect,
                        "opposing": item.opposing,
                    }
                )
            elif isinstance(item, ActionItem):
                json_data.append(
                    {
                        "id": item.id,
                        "meeting_id": item.meeting_id,
                        "workgroup": item.workgroup,
                        "date": item.date.isoformat() if item.date else None,
                        "text": item.text,
                        "assignee": item.assignee,
                        "status": item.status,
                        "due_date": item.due_date,
                    }
                )

        result = json.dumps(json_data, indent=2, ensure_ascii=False)
        logger.info(f"Exported {len(data)} items to JSON format")
        return result

