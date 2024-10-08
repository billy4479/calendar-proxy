import os
import requests
import ics


def get_calendar_lessons():
    cache_path = "./cache-lessons.ics"
    if not os.path.exists(cache_path):
        cal_text = requests.get(os.getenv("LESSONS_CALENDAR_URL")).text
        with open(cache_path, "w") as f:
            f.write(cal_text)
        return ics.Calendar(cal_text)
    else:
        with open(cache_path, "rb") as f:
            return ics.Calendar(f.read().decode("utf-8"))


def get_calendar_exams():
    cache_path = "./cache-exams.ics"
    if not os.path.exists(cache_path):
        cal_text = requests.get(os.getenv("EXAMS_CALENDAR_URL")).text
        with open(cache_path, "w") as f:
            f.write(cal_text)
        return ics.Calendar(cal_text)
    else:
        with open(cache_path, "rb") as f:
            return ics.Calendar(f.read().decode("utf-8"))


def make_nice_string(x: str) -> str:
    return (
        x.title()
        .replace("And", "and")
        .replace("Of", "of")
        .replace("In", "in")
        .replace("Ii", "II")
        .replace("Ai", "AI")
    )


