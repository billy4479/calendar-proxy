from api.app import app
import flask
import lib
import arrow


@app.route("/exams")
def process_exams():
    daylight_start = arrow.get("20230330T020000")
    daylight_end = arrow.get("20231027T030000")

    cal = lib.get_calendar_exams()

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
        exam_name = lib.make_nice_string(
            description.split(")")[1].split("  ")[0].strip()
        )

        event.name = f"Exam: {exam_name}"
        event.description = f"{exam_type} exam"

        lib.fix_time(event, daylight_start, daylight_end)

    return flask.Response(response=cal.serialize(), mimetype="text/calendar")
