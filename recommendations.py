"""
EduLift AI - Simple Rule-Based Recommendation Engine
Generates constructive, actionable, and supportive recommendations for students.
All thresholds are demonstration rules and do not label students negatively.
"""

from typing import List, Dict, Any

# Configurable demonstration thresholds (can be modified by instructors)
DEFAULT_ATTENDANCE_THRESHOLD = 75.0
PERFORMANCE_ATTENTION_THRESHOLD = 65.0
EXCELLENCE_THRESHOLD = 80.0


def analyze_student_academic_health(
    attendance_summary: Dict[str, Any],
    marks_summary: Dict[str, Any],
    attendance_threshold: float = DEFAULT_ATTENDANCE_THRESHOLD,
) -> Dict[str, Any]:
    """
    Examine attendance, marks, and trends to produce supportive recommendations,
    strengths, and areas that may benefit from focus.
    """
    recommendations: List[Dict[str, str]] = []
    strengths: List[str] = []
    needs_focus: List[str] = []
    indicators: List[str] = []

    overall_attendance = attendance_summary.get("overall_percentage", 0.0)
    attendance_records = attendance_summary.get("records", [])
    overall_avg = marks_summary.get("overall_average", 0.0)
    subject_stats = marks_summary.get("subject_stats", [])
    recent_assessments = marks_summary.get("recent_assessments", [])

    # 1. Evaluate Overall Attendance
    if attendance_records:
        if overall_attendance < attendance_threshold:
            indicators.append("Attendance below demo threshold")
            recommendations.append({
                "title": "Discuss Attendance Support with Faculty Advisor",
                "category": "Attendance",
                "urgency": "High",
                "reason": (
                    f"Overall attendance is currently {overall_attendance}%, which is below "
                    f"the course guide threshold of {attendance_threshold}%."
                ),
                "evidence": f"Total attended: {attendance_summary.get('attended_classes', 0)} of {attendance_summary.get('total_classes', 0)} classes.",
                "action": (
                    "Schedule a brief check-in with your mentor or class advisor to discuss any "
                    "scheduling, commute, or personal challenges and explore makeup sessions."
                ),
            })
        elif overall_attendance >= 85.0:
            strengths.append(f"Consistent Class Engagement ({overall_attendance}% overall attendance)")

    # 1b. Check Subject-Specific Attendance
    for att in attendance_records:
        sub_name = att["subject_name"]
        tot = att["total_classes"]
        att_cnt = att["attended_classes"]
        sub_pct = round((att_cnt / tot * 100), 1) if tot > 0 else 0.0

        if tot > 0 and sub_pct < attendance_threshold:
            needs_focus.append(f"{sub_name} Attendance ({sub_pct}%)")
            indicators.append(f"Low attendance in {sub_name} ({sub_pct}%)")
            recommendations.append({
                "title": f"Attendance Reinforcement in {sub_name}",
                "category": "Attendance",
                "urgency": "Medium",
                "reason": f"Your attendance in {sub_name} is currently {sub_pct}%, below the {attendance_threshold}% target.",
                "evidence": f"Attended {att_cnt} of {tot} scheduled lectures.",
                "action": f"Prioritize attending the next 3 upcoming {sub_name} sessions and review lecture recordings for missed dates.",
            })

    # 2. Evaluate Subject-Wise Marks & Performance
    for stat in subject_stats:
        sub_name = stat["subject_name"]
        avg_score = stat["avg_score_pct"]

        if avg_score is not None:
            if avg_score >= EXCELLENCE_THRESHOLD:
                strengths.append(f"Strong performance in {sub_name} ({round(avg_score, 1)}%)")
            elif avg_score < PERFORMANCE_ATTENTION_THRESHOLD:
                needs_focus.append(f"{sub_name} (Average: {round(avg_score, 1)}%)")
                indicators.append(f"Score improvement opportunity in {sub_name}")
                recommendations.append({
                    "title": f"Targeted Review for {sub_name}",
                    "category": "Academic Review",
                    "urgency": "Medium",
                    "reason": f"Current average mark is {round(avg_score, 1)}%, suggesting core concepts would benefit from reinforcement.",
                    "evidence": f"Subject assessments show an average of {round(avg_score, 1)}%.",
                    "action": (
                        f"Dedicate 45 minutes of weekly study planner time to review lecture notes "
                        f"and practice 3 sample problems in {sub_name}."
                    ),
                })

    # 3. Evaluate Recent Trend (comparing last 2 assessments if available)
    if len(recent_assessments) >= 2:
        latest = recent_assessments[0]
        previous = recent_assessments[1]
        latest_pct = (latest["score"] / latest["max_score"]) * 100
        prev_pct = (previous["score"] / previous["max_score"]) * 100
        diff = latest_pct - prev_pct

        if diff < -10.0:
            indicators.append(f"Recent assessment dip ({round(diff, 1)}%)")
            recommendations.append({
                "title": "Analyze Recent Assessment Differences",
                "category": "Exam Prep",
                "urgency": "Medium",
                "reason": (
                    f"Your most recent result in {latest['subject_name']} ({round(latest_pct, 1)}%) "
                    f"was {abs(round(diff, 1))}% lower than your previous assessment ({round(prev_pct, 1)}%)."
                ),
                "evidence": f"Assessment '{latest['assessment_name']}' scored {latest['score']}/{latest['max_score']}.",
                "action": (
                    "Review graded feedback to identify which questions caused difficulty, and "
                    "clarify doubts during instructor office hours or peer study groups."
                ),
            })
        elif diff >= 8.0:
            strengths.append(f"Positive momentum: +{round(diff, 1)}% improvement on recent {latest['assessment_name']}")

    # 4. Multi-Indicator Supportive Advisory
    if len(indicators) >= 2:
        recommendations.append({
            "title": "Holistic Academic Mentoring Session",
            "category": "Mentorship",
            "urgency": "High",
            "reason": "Multiple areas (attendance and recent test marks) are currently experiencing pressure at the same time.",
            "evidence": "; ".join(indicators),
            "action": (
                "Take advantage of a 1-on-1 supportive counseling or faculty mentoring session. "
                "Faculty can help tailor coursework priorities and provide personalized study guides."
            ),
        })

    # 5. General Study Habits (if no major alerts)
    if not recommendations:
        recommendations.append({
            "title": "Maintain Steady Study Cadence",
            "category": "Habits",
            "urgency": "Low",
            "reason": "Your attendance and academic markers are steady across the board.",
            "evidence": f"Overall average is {overall_avg}% with {overall_attendance}% attendance.",
            "action": "Continue with your weekly study schedule and try teaching concepts to peers to deepen mastery.",
        })

    return {
        "recommendations": recommendations,
        "strengths": strengths if strengths else ["Active semester participation"],
        "needs_focus": needs_focus if needs_focus else ["All subjects currently meeting benchmarks"],
        "indicator_count": len(indicators),
        "indicators": indicators,
    }
