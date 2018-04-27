import inspect
import json
from abc import ABC, abstractmethod
from typing import Callable

from adapt.engine import IntentDeterminationEngine
from adapt.intent import Intent


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
            "engine": None
        }
        self.answer = {
            "title": "No answer",
            "content": "No answer content",
            "url": None,
            "image_url": None
        }
        self.links = []
        self.trivia = {}
        self.error = None

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

    def set_error(self, message: str, code: int = None) -> 'Answer':
        self.error = {"message": message, "code": code}
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
        if self.error:
            return json.dumps({
                "meta": {
                    "skill": skill,
                    "confidence": confidence,
                    "cache": {
                        "last_miss": None,
                        "hit": False
                    },
                    "engine": None
                },
                "answer": None,
                "links": [],
                "trivia": {},
                "error": self.error
            })
        self.meta["skill"] = skill
        self.meta["confidence"] = confidence
        return json.dumps({
            "meta": self.meta,
            "answer": self.answer,
            "links": self.links,
            "trivia": self.trivia,
            "error": None
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
        self._intents = {}

    def register_intent(self, intent: Intent,
                        method: Callable[[Query], Answer]) -> 'QuiriSkill':
        self.engine.register_intent_parser(intent)
        self._intents[intent.name] = method
        return self

    @abstractmethod
    async def run(self, query: Query) -> Answer:
        pass


class Core:
    def __init__(self):
        self.engine = IntentDeterminationEngine()
        self._intents = {}

    def add_skill(
            self,
            skill_class: Callable[[IntentDeterminationEngine], QuiriSkill]):
        skill = skill_class(self.engine)
        methods = inspect.getmembers(skill, predicate=inspect.ismethod)
        for (name, method) in methods:
            if not hasattr(method, "_intents"):
                continue
            for intent in method._intents:
                skill.register_intent(intent, method)
        self._intents.update(skill._intents)

    async def process(self, q, context) -> str:
        try:
            intent = next(self.engine.determine_intent(q))
        except StopIteration:
            return None
        query = Query(q, context, intent)
        intent_type = intent["intent_type"]
        skill = self._intents[intent_type]
        confidence = intent["confidence"]
        return (await skill(query)).build(intent_type, confidence)
