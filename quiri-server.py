import logbook
import sys
import curio
from h11 import Response
from responds.server import Server
from responds.router import Router

logbook.StreamHandler(sys.stdout).push_application()

router = Router()
server = Server(router)


@router.route('/query')
async def query(event, params) -> Response:
    """Parses intent and runs a skill."""
    ...


@router.route('/query/context')
async def context_query(event, params) -> Response:
    """Parses context, then intent, then runs a skill.

    Looks at a dict of messages and their userids, strips all fluff,
    then makes a judgement on what to pass to the skill.
    """
    ...


@router.route('/search')
async def search(event, params) -> Response:
    """Runs the search skull with the given text."""

    ...


@router.route('/checkback')
async def checkback(event, params) -> Response:
    """Parses checkback requests from previous responses.

    Skills can set a checkback duration, after which the client will
    send the original request back on the /checkback endpoint, for
    further data.
    """
    ...


kernel = curio.Kernel()
kernel.run(curio.tcp_server('0.0.0.0', 8080, server.tcp_handle))
