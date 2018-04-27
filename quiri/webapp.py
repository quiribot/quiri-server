import sys
from argparse import ArgumentParser
from os import environ as env

import logbook

from responds.app import Application
from responds.backends.httptools_ import HTTPToolsBackend

from .api import ApiGroup

logbook.StreamHandler(sys.stdout).push_application()

_parse = ArgumentParser(description="start the quiri webserver")
_parse.add_argument("--bind-ip", dest="ip",
                    help="ip to bind to", default="0.0.0.0")
_parse.add_argument("--bind-port", dest="port",
                    help="port to bind to", type=int, default=8080)
_parse.add_argument("--skills", dest="skills_dir", help="skills directory")
args = _parse.parse_args()

app = Application("quiri_server", HTTPToolsBackend, level=logbook.WARNING)

app.add_group(ApiGroup(args.skills_dir))

ip = env.get("QUIRI_BIND_IP", args.ip)
port = int(env.get("QUIRI_BIND_PORT", args.port))
app.build()
app.run(ip, port)
