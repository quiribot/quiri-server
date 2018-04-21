import inspect
import json
from abc import ABC, abstractmethod
from typing import Callable

from adapt.engine import IntentDeterminationEngine


class Query:
    def __init__(self, raw, context, initial_data):
        self.raw = raw
        self.context = context
        self._initial_data = initial_data

    def __getattr__(self, name):
        try:
            return self._initial_data[name]
        except KeyError as e:
            raise AttributeError(e.args[0])


class Answer:
    def __init__(self):
        # TODO: modify defaults maybe
        self.meta = {
            "skill": None,
            "confidence": 0,
            "cache": {
                "last_miss": None,
                "hit": False
            },
            "engine": {
                "name": "Unknown",
                "url": None
            }
        }
        self.answer = {
            "title": "No answer",
            "content": "No answer content",
            "url": None,
            "image_url": None
        }
        self.links = []
        self.trivia = {}

    def set_cache(self, last_miss: int, hit: bool) -> 'Answer':
        self.meta["cache"] = {"last_miss": last_miss, "hit": hit}
        return self

    def set_engine(self, name: str, url: str = None) -> 'Answer':
        self.meta["engine"] = {"name": name, "url": url}
        return self

    def set_answer(self,
                   title: str,
                   content: str,
                   url: str = None,
                   image_url: str = None) -> 'Answer':
        self.answer = {
            "title": title,
            "content": content,
            "url": url,
            "image_url": image_url
        }
        return self

    def add_link(self,
                 title: str,
                 content: str,
                 url: str = None,
                 image_url: str = None) -> 'Answer':
        self.links.append({
            "title": title,
            "content": content,
            "url": url,
            "image_url": image_url
        })
        return self

    def add_trivia(self, name: str, link: str) -> 'Answer':
        self.trivia[name] = link
        return self

    def build(self, skill: str, confidence: int) -> dict:
        self.meta["skill"] = skill
        self.meta["confidence"] = confidence
        return json.dumps({
            "meta": self.meta,
            "answer": self.answer,
            "links": self.links,
            "trivia": self.trivia
        })


def intent_handler(intent):
    def __inner(func):
        if not hasattr(func, "_intents"):
            setattr(func, "_intents", [])
        func._intents.append(intent)
        return func

    return __inner


class QuiriSkill(ABC):
    def __init__(self, engine: IntentDeterminationEngine):
        self.engine = engine

    @abstractmethod
    async def run(self, query: Query) -> Answer:
        pass


class Core:
    def __init__(self):
        self.engine = IntentDeterminationEngine()
        self.skills = {}

    def add_skill(
            self,
            skill_class: Callable[[IntentDeterminationEngine], QuiriSkill]):
        skill = skill_class(self.engine)
        methods = inspect.getmembers(skill, predicate=inspect.ismethod)
        for (name, method) in methods:
            if not hasattr(method, "_intents"):
                continue
            for intent in method._intents:
                self.engine.register_intent_parser(intent)
                self.skills[intent.name] = method

    async def process(self, q, context) -> Answer:
        try:
            intent = next(self.engine.determine_intent(q))
        except StopIteration:
            return None
        query = Query(q, context, intent)
        intent_type = intent["intent_type"]
        skill = self.skills[intent_type]
        confidence = intent["confidence"]
        return (await skill(query)).build(intent_type, confidence)
