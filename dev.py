from http.server import HTTPServer
from api.lol import handler
import os
from dotenv import load_dotenv

load_dotenv()

port = os.getenv("PORT")
server_address = ("", int(port))
httpd = HTTPServer(server_address, handler)
print(f"serving on :{port}")
httpd.serve_forever()
