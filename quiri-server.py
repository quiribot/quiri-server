import logbook
import sys
import curio
from h11 import Response
from responds.server import Server
from responds.router import Router

logbook.StreamHandler(sys.stdout).push_application()

router = Router()
server = Server(router)


@router.route('/parse')
async def parse(event, params):
    ...


@router.route('/search')
async def search(event, params):
    ...

kernel = curio.Kernel()
kernel.run(curio.tcp_server('0.0.0.0', 8080, server.tcp_handle))
