from dateutil import parser
from typing import Optional, TYPE_CHECKING

from ..util import prettify, get_optional
from ..enums import KudosuAction, ObjectType


if TYPE_CHECKING:
    from datetime import datetime


class KudosuHistory:
    """
    **Attributes**

    id: :class:`int`

    action: :class:`KudosuAction`

    amount: :class:`int`

    model: :class:`ObjectType`
        Object type which the exchange happened on (forum_post, etc).

    created_at: :class:`datetime.datetime`

    giver: Optional[:class:`KudosuGiver`]
        Simple detail of the user who started the exchange.

    post: :class:`KudosuPost`
        Simple detail of the object for display.
    """

    __slots__ = ("id", "action", "amount", "model", "created_at", "giver", "post")

    def __init__(self, data):
        self.id: int = data["id"]
        self.action: KudosuAction = KudosuAction(data["action"])
        self.amount: int = data["amount"]
        self.model: ObjectType = ObjectType(data["model"])
        self.created_at: datetime = parser.parse(data["created_at"])
        self.giver: Optional[KudosuGiver] = get_optional(data, "giver", KudosuGiver)
        self.post: KudosuPost = KudosuPost(data["post"])

    def __repr__(self):
        return prettify(self, "action", "amount", "giver")


class KudosuPost:
    """
    **Attributes**

    url: Optional[:class:`str`]
        Url of the object.

    title: :class:`str`
        Title of the object. It'll be "[deleted beatmap]" for deleted beatmaps.
    """

    __slots__ = ("url", "title")

    def __init__(self, data):
        self.url: Optional[str] = data["url"]
        self.title: str = data["title"]

    def __repr__(self):
        return prettify(self, "title")


class KudosuGiver:
    """
    **Attributes**

    url: :class:`str`

    username: :class:`str`
    """

    __slots__ = ("url", "username")

    def __init__(self, data):
        self.url: str = data["url"]
        self.username: str = data["username"]

    def __repr__(self):
        return prettify(self, "username")
