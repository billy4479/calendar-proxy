from http.server import BaseHTTPRequestHandler
import lib


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        cal = lib.get_calendar_exams()
        lib.process_exams(cal)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(cal.serialize().encode("utf-8"))
        return
