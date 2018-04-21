from abc import ABC, abstractmethod
from logbook import Logger, DEBUG
from ..skills import Answer
import asks


class SearchError(Exception):
    def __init__(self, body, *args, status_code, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = body
        self.status_code = status_code


class SearchEngine(ABC):
    LOG = Logger("Searcher", level=DEBUG)

    def __init__(self, session: asks.Session):
        self.session = session

    @property
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    async def search(self, query: str, options) -> Answer:
        pass
