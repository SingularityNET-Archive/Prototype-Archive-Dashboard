"""Utility functions for extracting and normalizing people from meetings."""

from typing import List, Dict
from collections import defaultdict

from src.models.meeting import Meeting
from src.models.person import Person
from src.utils.text_normalizer import normalize_name, parse_comma_separated_string
from src.utils.logger import logger


def extract_all_people(meetings: List[Meeting]) -> Dict[str, Person]:
    """Extract and normalize all people from meetings.

    Extracts people from:
    - meetingInfo.host
    - meetingInfo.documenter
    - meetingInfo.peoplePresent (comma-separated string)
    - actionItems[].assignee

    Args:
        meetings: List of Meeting objects

    Returns:
        Dictionary mapping normalized person names to Person objects
    """
    people_dict: Dict[str, Person] = {}

    for meeting in meetings:
        # Extract from host
        if meeting.host:
            person_name = normalize_name(meeting.host)
            if person_name:
                person = _get_or_create_person(people_dict, person_name)
                person.add_workgroup(meeting.workgroup_id, role="host")
                person.add_meeting(meeting.id)

        # Extract from documenter
        if meeting.documenter:
            person_name = normalize_name(meeting.documenter)
            if person_name:
                person = _get_or_create_person(people_dict, person_name)
                person.add_workgroup(meeting.workgroup_id, role="documenter")
                person.add_meeting(meeting.id)

        # Extract from people_present
        if meeting.people_present:
            for person_name_raw in meeting.people_present:
                person_name = normalize_name(person_name_raw)
                if person_name:
                    person = _get_or_create_person(people_dict, person_name)
                    person.add_workgroup(meeting.workgroup_id, role="participant")
                    person.add_meeting(meeting.id)

        # Extract from action items assignees
        if meeting.action_items:
            for action_item in meeting.action_items:
                if action_item.assignee:
                    person_name = normalize_name(action_item.assignee)
                    if person_name:
                        person = _get_or_create_person(people_dict, person_name)
                        person.add_workgroup(meeting.workgroup_id, role="participant")
                        person.add_meeting(meeting.id)
                        person.add_action_item(action_item.id)

    logger.info(f"Extracted {len(people_dict)} unique people from {len(meetings)} meetings")
    return people_dict


def _get_or_create_person(people_dict: Dict[str, Person], name: str) -> Person:
    """Get existing person or create new one.

    Args:
        people_dict: Dictionary of people
        name: Normalized person name

    Returns:
        Person object
    """
    if name not in people_dict:
        people_dict[name] = Person(name)
    return people_dict[name]


def get_people_list(meetings: List[Meeting]) -> List[Person]:
    """Get list of all people from meetings.

    Args:
        meetings: List of Meeting objects

    Returns:
        List of Person objects
    """
    people_dict = extract_all_people(meetings)
    return list(people_dict.values())

