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


def process_lessons(cal: ics.Calendar):
    for event in cal.events:
        description = event.description
        desc_split = list(filter(lambda x: len(x) != 0, description.split(" ")))

        code = desc_split[4][1:-1]

        i = 5
        for part in desc_split[5:]:
            if part.startswith("("):
                break
            i += 1

        class_name = make_nice_string(" ".join(desc_split[5:i]))

        i += 3
        old_i = i
        for part in desc_split[old_i:]:
            if part == "Aule:":
                break
            i += 1
        teachers = " ".join(desc_split[old_i:i]).split("-")

        room = desc_split[i + 2]

        event.name = f"{class_name} ({code})"
        event.description = f"Room {room}\nProfessor{'' if len(teachers) == 1 else 's'}: {', '.join(teachers)}"

    return cal


def process_exams(cal: ics.Calendar):
    for event in cal.events:
        description = event.description
        name = event.name

        code = name.split("-")[1].strip()[1:-1]

        exam_type = (
            "General"
            if code == "S"
            else "Partial"
            if code == "I"
            else "Oral"
            if code == "O"
            else f"??? - Code: {code}"
        )
        exam_name = make_nice_string(description.split(")")[1].split("  ")[0].strip())

        event.name = f"Exam: {exam_name}"
        event.description = f"{exam_type} exam"
