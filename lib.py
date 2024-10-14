import os
import requests
import ics
import arrow

# FIXME: this is kind of a hack, but it works
daylight_start = arrow.get("20230330T020000")
daylight_end = arrow.get("20231027T030000")


def fix_time(event: ics.Event):
    old_duration = event.duration

    if (
        event.begin.month > daylight_start.month
        or (
            event.begin.month == daylight_start.month
            and event.begin.day >= daylight_start.day
        )
    ) and (
        event.begin.month < daylight_end.month
        or (
            event.begin.month == daylight_end.month
            and event.begin.day <= daylight_end.day
        )
    ):
        event.begin = event.begin.shift(hours=-2)
    else:
        event.begin = event.begin.shift(hours=-1)

    event.duration = old_duration


def get_calendar(cache_path, url):
    # TODO: figure out caching in production
    if os.getenv("ENV") == "prod":
        cal_text = requests.get(url).text
        return ics.Calendar(cal_text)

    if not os.path.exists(cache_path):
        cal_text = requests.get(url).text
        with open(cache_path, "w") as f:
            f.write(cal_text)
        return ics.Calendar(cal_text)
    else:
        with open(cache_path, "rb") as f:
            return ics.Calendar(f.read().decode("utf-8"))


def get_calendar_lessons():
    return get_calendar("./cache-lessons.ics", os.getenv("LESSONS_CALENDAR_URL"))


def get_calendar_exams():
    return get_calendar("./cache-exams.ics", os.getenv("EXAMS_CALENDAR_URL"))


def make_nice_string(x: str) -> str:
    return (
        x.title()
        .replace("And", "and")
        .replace("Of", "of")
        .replace("In", "in")
        .replace("Ii", "II")
        .replace("Ai", "AI")
    )
