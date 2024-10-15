from api.app import app
import lib
import flask
import arrow


@app.route("/lessons")
def rewrite_lessons():
    daylight_start = arrow.get("20230330T020000")
    daylight_end = arrow.get("20231027T030000")  # What? it should be 27/10

    cal = lib.get_calendar_lessons()

    for event in cal.events:
        description = event.description
        desc_split = list(filter(lambda x: len(x) != 0, description.split(" ")))

        code = desc_split[4][1:-1]

        i = 5
        for part in desc_split[5:]:
            if part.startswith("("):
                break
            i += 1

        class_name = lib.make_nice_string(" ".join(desc_split[5:i]))

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

        lib.fix_time(event, daylight_start, daylight_end)

    return flask.Response(response=cal.serialize(), mimetype="text/calendar")
