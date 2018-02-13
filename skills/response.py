"""Response Model"""

import h11


class Response(h11.Response):
    """Response sent by API to platform instances."""

    def __init__(self, body: str, title: str=None, url: str=None,
                 icon: str=None, related: list=None, is_object: bool=False,
                 wait_for: int=0, after_wait: str=None,
                 provider: str="search"):
        self.title = title
        self.body = body
        self.url = url
        self.icon = icon
        self.related = related
        self.is_object = is_object
        self.wait_for = wait_for
        self.provider = provider
