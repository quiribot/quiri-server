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
    ...


@router.route('/query/context')
async def context_query(event, params) -> Response:
    ...


@router.route('/search')
async def search(event, params) -> Response:
    ...


@router.route('/callback')
async def callback(event, params) -> Response:
    ...


kernel = curio.Kernel()
kernel.run(curio.tcp_server('0.0.0.0', 8080, server.tcp_handle))
