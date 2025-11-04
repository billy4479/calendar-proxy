import datetime
import os

import arrow
import flask
from flask import Flask, request

import utils

app = Flask(__name__)


@app.route("/exams")
def process_exams():
    if request.args.get("t") != os.getenv("TOKEN"):
        return flask.Response(response="Unauthorized", status=401)

    daylight_start = arrow.get("20230330T020000")
    daylight_end = arrow.get("20231027T030000")

    cal = utils.get_calendar_exams()

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
        exam_name = utils.make_nice_string(
            description.split(")")[1].split("  ")[0].strip()
        )

        event.name = f"Exam: {exam_name}"
        event.description = f"{exam_type} exam"

        utils.fix_time(event, daylight_start, daylight_end)

    t = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    print(
        f'[{t}] {request.path} -> {len(cal.events)} events for "{request.user_agent}"@{request.remote_addr}'
    )

    return flask.Response(response=cal.serialize(), mimetype="text/calendar")


@app.route("/lessons")
def rewrite_lessons():
    if request.args.get("t") != os.getenv("TOKEN"):
        return flask.Response(response="Unauthorized", status=401)

    daylight_start = arrow.get("20230330T020000")
    daylight_end = arrow.get("20231027T030000")  # What? it should be 27/10

    cal = utils.get_calendar_lessons()

    for event in cal.events:
        description = event.description
        desc_split = list(filter(lambda x: len(x) != 0, description.split(" ")))

        code = desc_split[4][1:-1]

        i = 5
        for part in desc_split[5:]:
            if part.startswith("("):
                break
            i += 1

        class_name = utils.make_nice_string(" ".join(desc_split[5:i]))

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

        utils.fix_time(event, daylight_start, daylight_end)

    t = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    print(
        f'[{t}] {request.path} -> {len(cal.events)} for "{request.user_agent}"@{request.remote_addr}'
    )
    return flask.Response(response=cal.serialize(), mimetype="text/calendar")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT")))
