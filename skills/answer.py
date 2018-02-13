"""Response Model"""


class Answer:
    """Answer sent back to server."""

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
