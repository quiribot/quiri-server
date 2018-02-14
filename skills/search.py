import duckduckgo as ddg
import bing
from models import Answer


class Search:

    def __init__(self, client):
        self.client = client  # TODO asks.Session(connections=20)
        self.answer = Answer(reply=None)

    async def run(self, req) -> Answer:
        self.ddg_search(req.whatever)
        self.bing_search(req.whatever)
        return self.answer

    async def ddg_search(self, query: str):
        """Searches DuckDuckGo for an instant answer."""

        ia = await ddg.query(query)

        if ia.redirect.url != "":
            self.answer.reply = ia.redirect.url
        elif ia.answer.text != "":
            self.answer.body = ia.answer.text
        elif ia.abstract.text != "":
            self.answer.body = ia.abstract.text
            self.answer.url = ia.abstract.url
            self.answer.icon = ia.image.url
            self.answer.related = ia.related
        elif len(ia.related) is not 0:
            self.answer.title = "Did you mean..."
            self.answer.related = ia.related
        else:
            # XXX Find where it gets its data from
            self.answer.reply = ddg.get_zci

    async def bing_search(self, query: str):
        ...
