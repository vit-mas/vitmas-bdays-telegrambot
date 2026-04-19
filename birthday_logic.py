"""Birthday calculation and logic operations."""
from datetime import datetime, timedelta
from sheets_service import get_all_birthdays

def get_tomorrow_birthdays():
    """Get all people with birthdays tomorrow."""
    data = get_all_birthdays()
    tomorrow = datetime.now() + timedelta(days=1)
    target = tomorrow.strftime("%d/%m")
    return [p for p in data if p["DOB"] == target]

def get_upcoming_birthdays(limit=3):
    """Get the next upcoming birthdays (default: 3 soonest)."""
    data = get_all_birthdays()
    today = datetime.now()
    upcoming = []

    for p in data:
        day, month = map(int, p["DOB"].split("/"))
        next_bday = datetime(today.year, month, day)

        if next_bday < today:
            next_bday = datetime(today.year + 1, month, day)

        upcoming.append((next_bday, p))

    upcoming.sort(key=lambda x: x[0])
    return upcoming[:limit]
