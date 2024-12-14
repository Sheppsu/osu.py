from typing import Optional, List, TYPE_CHECKING

from ..util import prettify, get_optional, get_required, fromisoformat
from ..enums import ForumTopicType


if TYPE_CHECKING:
    from datetime import datetime


__all__ = ("Forum", "ForumPost", "TextFormat", "ForumTopic", "Poll", "PollOption")


class Forum:
    __slots__ = ("id", "name", "description", "subforums")

    def __init__(self, data):
        self.id: int = get_required(data, "id")
        self.name: str = get_required(data, "name")
        self.description: str = get_required(data, "description")
        self.subforums: List[Forum] = list(map(Forum, get_required(data, "subforums")))

    def __repr__(self):
        return prettify(self, "id", "name", "subforums")


class ForumPost:
    """
    **Attributes**

    created_at: :py:class:`datetime.datetime`

    deleted_at: Optional[:py:class:`datetime.datetime`]

    edited_at: Optional[:py:class:`datetime.datetime`]

    edited_by_id: Optional[int]

    forum_id: int

    id: int

    topic_id: int

    user_id: int

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
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", fromisoformat)
        self.edited_at: Optional[datetime] = get_optional(data, "edited_at", fromisoformat)
        self.edited_by_id: Optional[int] = data.get("edited_by_id")
        self.forum_id: int = get_required(data, "forum_id")
        self.id: int = get_required(data, "id")
        self.topic_id: int = get_required(data, "topic_id")
        self.user_id: int = get_required(data, "user_id")
        self.body: Optional[TextFormat] = get_optional(data, "body", TextFormat)

    def __repr__(self):
        return prettify(self, "user_id", "topic_id")


class TextFormat:
    """
    A page that has html and raw data

    **Attributes**

    html: str

    raw: str
    """

    __slots__ = ("html", "raw")

    def __init__(self, data):
        self.html: str = get_required(data, "html")
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

    created_at: :py:class:`datetime.datetime`

    deleted_at: Optional[:py:class:`datetime.datetime`]

    first_post_id: int

    forum_id: int

    id: int

    is_locked: bool

    last_post_id: int

    poll: Optional[:class:`Poll`]

    post_count: int

    title: str

    type: :class:`ForumTopicType`

    updated_at: :py:class:`datetime.datetime`

    user_id: int
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
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", fromisoformat)
        self.first_post_id: int = get_required(data, "first_post_id")
        self.forum_id: int = get_required(data, "forum_id")
        self.id: int = get_required(data, "id")
        self.is_locked: bool = get_required(data, "is_locked")
        self.last_post_id: int = get_required(data, "last_post_id")
        self.poll: Optional[Poll] = get_optional(data, "poll", Poll)
        self.post_count: int = get_required(data, "post_count")
        self.title: str = get_required(data, "title")
        self.type: ForumTopicType = ForumTopicType(get_required(data, "type"))
        self.updated_at: datetime = fromisoformat(get_required(data, "updated_at"))
        self.user_id: int = get_required(data, "user_id")

    def __repr__(self):
        return prettify(self, "user_id", "title")


class Poll:
    """
    **Attributes**

    allow_vote_change: bool

    ended_at: Optional[:py:class:`datetime.datetime`]

    hide_incomplete_results: bool

    last_vote_at: Optional[:py:class:`datetime.datetime`]

    max_votes: int

    options: List[:class:`PollOption`]

    started_at: :py:class:`datetime.datetime`

    title: :class:`TextFormat`

    total_vote_count: int
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
        self.allow_vote_change: bool = get_required(data, "allow_vote_change")
        self.ended_at: Optional[datetime] = get_optional(data, "ended_at", fromisoformat)
        self.hide_incomplete_results: bool = get_required(data, "hide_incomplete_results")
        self.last_vote_at: Optional[datetime] = get_optional(data, "last_vote_at", fromisoformat)
        self.max_votes: int = get_required(data, "max_votes")
        self.options: List[PollOption] = list(map(PollOption, get_required(data, "options")))
        self.started_at: datetime = fromisoformat(get_required(data, "started_at"))
        self.title: TextFormat = TextFormat(get_required(data, "title"))
        self.total_vote_count: int = get_required(data, "total_vote_count")

    def __repr__(self):
        return prettify(self, "title", "options")


class PollOption:
    """
    **Attributes**

    id: int

    text: :class:`TextFormat`

    vote_count: Optional[int]
        Not present if the poll is incomplete and results are hidden.
    """

    __slots__ = ("id", "text", "vote_count")

    def __init__(self, data):
        self.id: int = get_required(data, "id")
        self.text: TextFormat = TextFormat(get_required(data, "text"))
        self.vote_count: Optional[int] = get_required(data, "vote_count")

    def __repr__(self):
        return prettify(self, "text", "vote_count")
