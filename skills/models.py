"""Object Models"""

from typing import List, Optional, Union

AdditionalData = Union[str, int, bool, List[str, int, bool]]
"""Typing of all acceptable data types for **additional kwargs."""


class Answer:
    """Answer sent back to server by skill.

    Represents a base outline for all data a skill can return. Allows
    optional keyword-based data, which implementations can choose to
    ignore or format how they see fit.

    Attributes:
        reply (str): The basic conversational answer provided by the
            skill.
        title (str, optional): The heading for the information.
        body (str, optional): In-depth description of the information.
        url (str, optional): Website attached to the information.
        icon (str, optional): Visual for the information.
        related (List[str], optional): A list of related topics or info.
        is_object (bool, optional): Is information a card/embed/etc.
        checkback (Optional[int], optional): /checkback after x long.
        provider (str, optional): What skill provided the information.
        **additional (AdditionalData): Any necessary additonal content.
    """

    def __init__(self, reply: str, title: str=None, body: str=None,
                 url: str=None, icon: str=None, related: List[str]=[],
                 is_object: bool=False, checkback: Optional[int]=None,
                 provider: str="search", **additional: AdditionalData):
        self.reply = reply
        self.title = title
        self.body = body
        self.url = url
        self.icon = icon
        self.related = related
        self.is_object = is_object
        self.checkback = checkback
        self.provider = provider
        self.additional = dict(additional)
