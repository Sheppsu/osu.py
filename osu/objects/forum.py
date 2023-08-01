from dateutil import parser
from typing import Optional, List, TYPE_CHECKING

from ..util import prettify, get_optional
from ..enums import ForumTopicType


if TYPE_CHECKING:
    from datetime import datetime


class ForumPost:
    """
    **Attributes**

    created_at: :class:`datetime.datetime`

    deleted_at: Optional[:class:`datetime.datetime`]

    edited_at: Optional[:class:`datetime.datetime`]

    edited_by_id: Optional[:class:`int`]

    forum_id: :class:`int`

    id: :class:`int`

    topic_id: :class:`int`

    user_id: :class:`int`

    body: Optional[:class:`TextFormat`]
    """

    __slots__ = (
        "created_at",
        "deleted_at",
        "edited_at",
        "edited_by_id",
        "forum_id",
        "id",
        "topic_id",
        "user_id",
        "body",
    )

    def __init__(self, data):
        self.created_at: datetime = parser.parse(data["created_at"])
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", parser.parse)
        self.edited_at: Optional[datetime] = get_optional(data, "edited_at", parser.parse)
        self.edited_by_id: Optional[int] = data.get("edited_by_id")
        self.forum_id: int = data["forum_id"]
        self.id: int = data["id"]
        self.topic_id: int = data["topic_id"]
        self.user_id: int = data["user_id"]
        self.body: Optional[TextFormat] = get_optional(data, "body", TextFormat)

    def __repr__(self):
        return prettify(self, "user_id", "topic_id")


class TextFormat:
    """
    A page that has html and raw data

    **Attributes**

    html: :class:`str`

    raw: :class:`str`
    """

    __slots__ = ("html", "raw")

    def __init__(self, data):
        self.html: str = data["html"]
        for attr in ("raw", "bbcode", "markdown"):
            if attr in data:
                self.raw: str = data[attr]
                break
        if self.raw is None:
            raise KeyError("data did not contain a raw value")

    def __repr__(self):
        return prettify(self, "raw")


class ForumTopic:
    """
    **Attributes**

    created_at: :class:`datetime.datetime`

    deleted_at: Optional[:class:`datetime.datetime`]

    first_post_id: :class:`int`

    forum_id: :class:`int`

    id: :class:`int`

    is_locked: :class:`bool`

    last_post_id: :class:`int`

    poll: Optional[:class:`Poll`]

    post_count: :class:`int`

    title: :class:`str`

    type: :class:`ForumTopicType`

    updated_at: :class:`datetime.datetime`

    user_id: :class:`int`
    """

    __slots__ = (
        "created_at",
        "deleted_at",
        "first_post_id",
        "forum_id",
        "id",
        "is_locked",
        "last_post_id",
        "poll",
        "post_count",
        "title",
        "type",
        "updated_at",
        "user_id",
    )

    def __init__(self, data):
        self.created_at: datetime = parser.parse(data["created_at"])
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", parser.parse)
        self.first_post_id: int = data["first_post_id"]
        self.forum_id: int = data["forum_id"]
        self.id: int = data["id"]
        self.is_locked: bool = data["is_locked"]
        self.last_post_id: int = data["last_post_id"]
        self.poll: Optional[Poll] = get_optional(data, "poll", Poll)
        self.post_count: int = data["post_count"]
        self.title: str = data["title"]
        self.type: ForumTopicType = ForumTopicType(data["type"])
        self.updated_at: datetime = parser.parse(data["updated_at"])
        self.user_id: int = data["user_id"]

    def __repr__(self):
        return prettify(self, "user_id", "title")


class Poll:
    """
    **Attributes**

    allow_vote_change: :class:`bool`

    ended_at: Optional[:class:`datetime.datetime`]

    hide_incomplete_results: :class:`bool`

    last_vote_at: Optional[:class:`datetime.datetime`]

    max_votes: :class:`int`

    options: List[:class:`PollOption`]

    started_at: :class:`datetime.datetime`

    title: :class:`TextFormat`

    total_vote_count: :class:`int`
    """

    __slots__ = (
        "allow_vote_change",
        "ended_at",
        "hide_incomplete_results",
        "last_vote_at",
        "max_votes",
        "options",
        "started_at",
        "title",
        "total_vote_count",
    )

    def __init__(self, data):
        self.allow_vote_change: bool = data["allow_vote_change"]
        self.ended_at: Optional[datetime] = get_optional(data, "ended_at", parser.parse)
        self.hide_incomplete_results: bool = data["hide_incomplete_results"]
        self.last_vote_at: Optional[datetime] = get_optional(data, "last_vote_at", parser.parse)
        self.max_votes: int = data["max_votes"]
        self.options: List[PollOption] = list(map(PollOption, data["options"]))
        self.started_at: datetime = parser.parse(data["started_at"])
        self.title: TextFormat = TextFormat(data["title"])
        self.total_vote_count: int = data["total_vote_count"]

    def __repr__(self):
        return prettify(self, "title", "options")


class PollOption:
    """
    **Attributes**

    id: :class:`int`

    text: :class:`TextFormat`

    vote_count: Optional[:class:`int`]
        Not present if the poll is incomplete and results are hidden.
    """

    __slots__ = ("id", "text", "vote_count")

    def __init__(self, data):
        self.id: int = data["id"]
        self.text: TextFormat = TextFormat(data["text"])
        self.vote_count: Optional[int] = data["vote_count"]

    def __repr__(self):
        return prettify(self, "text", "vote_count")
