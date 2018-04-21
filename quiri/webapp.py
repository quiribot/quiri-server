import sys
from os import environ as env

import logbook

from responds.app import Application
from responds.backends.httptools_ import HTTPToolsBackend

from .api import ApiGroup

logbook.StreamHandler(sys.stdout).push_application()

app = Application("quiri_server", HTTPToolsBackend, level=logbook.WARNING)

app.add_group(ApiGroup())

ip = env.get("QUIRI_BIND_IP", "0.0.0.0")
port = int(env.get("QUIRI_BIND_PORT", "8080"))
app.build()
app.run(ip, port)
