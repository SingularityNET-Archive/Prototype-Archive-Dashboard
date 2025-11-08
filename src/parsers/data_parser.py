"""Data parser service for loading and normalizing JSON archive data."""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from src.models.meeting import Meeting
from src.models.decision import Decision
from src.models.action_item import ActionItem
from src.utils.date_parser import parse_date
from src.utils.text_normalizer import (
    parse_comma_separated_string,
    normalize_name,
    normalize_topics,
)
from src.utils.logger import logger


def load_archive(json_file_path: str) -> List[Meeting]:
    """Load and parse JSON archive file into normalized Meeting objects.

    Args:
        json_file_path: Path to meeting-summaries-array-3.json

    Returns:
        List of normalized Meeting objects

    Raises:
        FileNotFoundError: If JSON file doesn't exist
        json.JSONDecodeError: If JSON is malformed
        ValueError: If required fields are missing
    """
    file_path = Path(json_file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")

    logger.info(f"Loading archive from {json_file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON file: {e}")
        raise

    if not isinstance(raw_data, list):
        raise ValueError("JSON file must contain an array of meetings")

    meetings = []
    for index, raw_meeting in enumerate(raw_data):
        try:
            meeting = normalize_meeting(raw_meeting, index)
            meetings.append(meeting)
        except (ValueError, KeyError) as e:
            logger.warning(f"Skipping malformed meeting at index {index}: {e}")
            continue

    logger.info(f"Successfully loaded {len(meetings)} meetings from archive")
    return meetings


def normalize_meeting(raw_meeting: Dict[str, Any], index: int = 0) -> Meeting:
    """Normalize a raw meeting dictionary into a Meeting object.

    Args:
        raw_meeting: Raw meeting dictionary from JSON
        index: Index of meeting in array (for ID generation)

    Returns:
        Normalized Meeting object

    Raises:
        ValueError: If required fields are missing or invalid
        KeyError: If required nested fields are missing
    """
    # Extract required fields
    workgroup = raw_meeting.get("workgroup")
    workgroup_id = raw_meeting.get("workgroup_id")
    meeting_type = raw_meeting.get("type")
    no_summary_given = raw_meeting.get("noSummaryGiven", False)
    canceled_summary = raw_meeting.get("canceledSummary", False)

    # Validate required fields
    if not workgroup:
        raise ValueError("Missing required field: workgroup")
    if not workgroup_id:
        raise ValueError("Missing required field: workgroup_id")
    if not meeting_type:
        raise ValueError("Missing required field: type")

    # Extract meetingInfo
    meeting_info = raw_meeting.get("meetingInfo", {})
    if not meeting_info:
        raise ValueError("Missing required field: meetingInfo")

    date_str = meeting_info.get("date")
    if not date_str:
        raise ValueError("Missing required field: meetingInfo.date")

    # Parse date
    try:
        date = parse_date(date_str)
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date_str}") from e

    # Generate unique ID
    meeting_id = f"{workgroup_id}_{date_str}_{index}"

    # Extract optional fields from meetingInfo
    host = meeting_info.get("host")
    if host:
        host = normalize_name(host)

    documenter = meeting_info.get("documenter")
    if documenter:
        documenter = normalize_name(documenter)

    people_present_str = meeting_info.get("peoplePresent")
    people_present = parse_comma_separated_string(people_present_str)
    people_present = [normalize_name(name) for name in people_present]

    purpose = meeting_info.get("purpose")
    type_of_meeting = meeting_info.get("typeOfMeeting")
    meeting_video_link = meeting_info.get("meetingVideoLink")
    working_docs = meeting_info.get("workingDocs", [])

    # Extract tags
    tags = raw_meeting.get("tags", {})
    topics_covered_str = tags.get("topicsCovered")
    topics_covered = parse_comma_separated_string(topics_covered_str)
    # Normalize topics for matching (lowercase), but preserve original for display
    topics_covered_normalized = normalize_topics(topics_covered)
    # For now, keep original case for display, but we can use normalized for matching
    topics_covered = topics_covered  # Keep original case

    emotions_str = tags.get("emotions")
    emotions = parse_comma_separated_string(emotions_str)

    # Extract discussion points from agendaItems
    discussion_points = []
    agenda_items = raw_meeting.get("agendaItems", [])
    for agenda_item in agenda_items:
        # Handle discussionPoints (array)
        if "discussionPoints" in agenda_item:
            discussion_points.extend(agenda_item["discussionPoints"])

        # Handle narrative (string) - convert to single-item list
        if "narrative" in agenda_item and agenda_item["narrative"]:
            discussion_points.append(agenda_item["narrative"])

    # Handle meetingTopics if present (merge with topics_covered)
    if "meetingTopics" in raw_meeting:
        meeting_topics = raw_meeting["meetingTopics"]
        if isinstance(meeting_topics, list):
            topics_covered.extend(meeting_topics)
        elif isinstance(meeting_topics, str):
            topics_covered.extend(parse_comma_separated_string(meeting_topics))

    # Parse action items and decisions from agendaItems
    action_items = []
    decisions = []
    
    for agenda_item_index, agenda_item in enumerate(agenda_items):
        # Parse action items
        if "actionItems" in agenda_item:
            for action_index, raw_action in enumerate(agenda_item["actionItems"]):
                try:
                    action_id = f"{meeting_id}_action_{agenda_item_index}_{action_index}"
                    action_item = ActionItem(
                        id=action_id,
                        meeting_id=meeting_id,
                        workgroup=workgroup,
                        date=date,
                        text=raw_action.get("text", ""),
                        status=raw_action.get("status", "todo"),
                        assignee=normalize_name(raw_action.get("assignee")) if raw_action.get("assignee") else None,
                        due_date=raw_action.get("dueDate"),
                    )
                    action_items.append(action_item)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping malformed action item in meeting {meeting_id}: {e}")
                    continue

        # Parse decision items
        if "decisionItems" in agenda_item:
            for decision_index, raw_decision in enumerate(agenda_item["decisionItems"]):
                try:
                    decision_id = f"{meeting_id}_decision_{agenda_item_index}_{decision_index}"
                    decision = Decision(
                        id=decision_id,
                        meeting_id=meeting_id,
                        workgroup=workgroup,
                        date=date,
                        decision_text=raw_decision.get("decision", ""),
                        effect=raw_decision.get("effect", "affectsOnlyThisWorkgroup"),
                        rationale=raw_decision.get("rationale"),
                        opposing=raw_decision.get("opposing"),
                    )
                    decisions.append(decision)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping malformed decision in meeting {meeting_id}: {e}")
                    continue

    return Meeting(
        id=meeting_id,
        workgroup=workgroup,
        workgroup_id=workgroup_id,
        date=date,
        type=meeting_type,
        no_summary_given=no_summary_given,
        canceled_summary=canceled_summary,
        host=host,
        documenter=documenter,
        people_present=people_present,
        purpose=purpose,
        type_of_meeting=type_of_meeting,
        meeting_video_link=meeting_video_link,
        working_docs=working_docs,
        action_items=action_items,
        decisions=decisions,
        discussion_points=discussion_points,
        topics_covered=topics_covered,
        emotions=emotions,
    )

