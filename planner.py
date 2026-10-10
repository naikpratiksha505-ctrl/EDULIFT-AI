"""
EduLift AI - Basic Study Planner Generator
Generates realistic, balanced weekly study schedules based on student availability,
upcoming assessments, and priority subjects, incorporating built-in short breaks.
"""

from typing import List, Dict, Any


def generate_study_schedule(
    subjects: List[Dict[str, Any]],
    available_hours: float,
    upcoming_assessments: List[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate a balanced weekly schedule of 45-minute focused study sessions
    with built-in break intervals, respecting the student's stated weekly hours.

    Parameters:
    - subjects: list of subject dicts with 'id', 'name', 'code'
    - available_hours: total hours student has available this week (e.g. 5 to 20)
    - upcoming_assessments: list of assessments soon due
    """
    if not subjects or available_hours <= 0:
        return []

    upcoming_assessments = upcoming_assessments or []

    # Map upcoming subjects to boost priority
    urgent_subject_ids = {a.get("subject_id") for a in upcoming_assessments if a.get("subject_id")}

    # Calculate total 45-minute sessions that fit in available hours
    total_minutes = int(available_hours * 60)
    session_duration = 45  # 45 minutes focused session + 15 min break
    num_sessions = max(1, total_minutes // 60)

    # Days of the week to distribute across
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    # Standard evening study time slots
    slots = ["17:00", "18:00", "19:00", "20:00"]

    suggested_tasks = []
    subject_index = 0

    for i in range(num_sessions):
        # Rotate through days
        day = days[i % len(days)]
        slot = slots[(i // len(days)) % len(slots)]

        # Determine subject: prioritize subjects with upcoming assessments
        if urgent_subject_ids and (i % 2 == 0):
            # Pick from urgent subjects
            urgent_list = [s for s in subjects if s["id"] in urgent_subject_ids]
            subject = urgent_list[i % len(urgent_list)] if urgent_list else subjects[subject_index % len(subjects)]
            priority = "High"
            task_type = "Exam Prep & Practice Problems"
        else:
            subject = subjects[subject_index % len(subjects)]
            priority = "Medium"
            task_type = "Concept Review & Notes Summary"
            subject_index += 1

        suggested_tasks.append({
            "subject_id": subject["id"],
            "subject_name": subject["name"],
            "title": f"{subject['name']}: {task_type}",
            "day_of_week": day,
            "start_time": slot,
            "duration_minutes": session_duration,
            "priority": priority,
        })

    return suggested_tasks
