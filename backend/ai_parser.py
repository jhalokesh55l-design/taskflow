import re
from datetime import date, timedelta


def parse_quick_add(text: str):
    text = text.strip()

    if not text:
        raise ValueError("Text cannot be blank")

    # Default values
    priority = "medium"
    due_date = None
    project = None

    # Priority
    priority_match = re.search(
        r"\b(high|medium|low)\s+priority\b",
        text,
        re.IGNORECASE
    )

    if priority_match:
        priority = priority_match.group(1).lower()

    # Due date: today
    if re.search(r"\btoday\b", text, re.IGNORECASE):
        due_date = date.today().isoformat()

    # Due date: tomorrow
    elif re.search(r"\btomorrow\b", text, re.IGNORECASE):
        due_date = (date.today() + timedelta(days=1)).isoformat()

    # Due date: in N days
    else:
        days_match = re.search(
            r"\bin\s+(\d+)\s+days?\b",
            text,
            re.IGNORECASE
        )

        if days_match:
            days = int(days_match.group(1))
            due_date = (
                date.today() + timedelta(days=days)
            ).isoformat()

    # Project
    project_match = re.search(
        r"\bproject\s*[:=]\s*([A-Za-z0-9 _-]+)",
        text,
        re.IGNORECASE
    )

    if project_match:
        project = project_match.group(1).strip()

    # Remove recognized metadata to get title
    title = text

    title = re.sub(
        r"\b(high|medium|low)\s+priority\b",
        "",
        title,
        flags=re.IGNORECASE
    )

    title = re.sub(
        r"\btoday\b|\btomorrow\b",
        "",
        title,
        flags=re.IGNORECASE
    )

    title = re.sub(
        r"\bin\s+\d+\s+days?\b",
        "",
        title,
        flags=re.IGNORECASE
    )

    title = re.sub(
        r"\bproject\s*[:=]\s*[A-Za-z0-9 _-]+",
        "",
        title,
        flags=re.IGNORECASE
    )

    title = re.sub(r"\s+", " ", title).strip()

    if not title:
        raise ValueError("Could not determine task title")

    return {
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "project": project
    }