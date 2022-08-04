from dateutil import parser

from ..util import prettify


class ForumPost:
    """
    **Attributes**

    created_at: :class:`datetime.datetime`

    deleted_at: :class:`datetime.datetime` or :class:`NoneType`

    edited_at: :class:`datetime.datetime` or :class:`NoneType`

    edited_by_id: :class:`int` or :class:`NoneType`

    forum_id: :class:`int`

    id: :class:`int`

    topic_id: :class:`int`

    user_id: :class:`int`

    **Possible Attributes**

    body: :class:`dict`
        dictionary containing keys html and raw. html: Post content in HTML format. raw: content in BBCode format.
    """
    __slots__ = (
        "created_at", "deleted_at", "edited_at", "edited_by_id", "forum_id",
        "id", "topic_id", "user_id", "body"
    )

    def __init__(self, data):
        self.created_at = parser.parse(data["created_at"])
        self.deleted_at = parser.parse(data["deleted_at"]) if data["deleted_at"] is not None else None
        self.edited_at = parser.parse(data["edited_at"]) if data["edited_at"] is not None else None
        self.edited_by_id = data['edited_by_id']
        self.forum_id = data['forum_id']
        self.id = data['id']
        self.topic_id = data['topic_id']
        self.user_id = data['user_id']
        self.body = data.get('body', None)

    def __repr__(self):
        return prettify(self, 'user_id', 'topic_id')


class ForumTopic:
    """
    **Attributes**

    created_at: :class:`datetime.datetime`

    deleted_at: :class:`datetime.datetime` or :class:`NoneType`

    first_post_id: :class:`int`

    forum_id: :class:`int`

    id: :class:`int`

    is_locked: :class:`bool`

    last_post_id: :class:`int`

    poll: :class:`Poll` or :class:`NoneType`

    post_count: :class:`int`

    title: :class:`str`

    type: :class:`str`
        normal, sticky, or announcement

    updated_at: :class:`datetime.datetime`

    user_id: :class:`int`
    """
    __slots__ = (
        "created_at", "deleted_at", "first_post_id", "forum_id", "id", "is_locked",
        "last_post_id", "poll", "post_count", "title", "type", "updated_at", "user_id"
    )

    def __init__(self, data):
        self.created_at = parser.parse(data["created_at"])
        self.deleted_at = parser.parse(data["deleted_at"]) if data["deleted_at"] is not None else None
        self.first_post_id = data['first_post_id']
        self.forum_id = data['forum_id']
        self.id = data['id']
        self.is_locked = data['is_locked']
        self.last_post_id = data['last_post_id']
        self.post_count = data['post_count']
        self.title = data['title']
        self.type = data['type']
        self.updated_at = parser.parse(data["updated_at"])
        self.user_id = data['user_id']

    def __repr__(self):
        return prettify(self, 'user_id', 'title')


class Poll:
    """
    **Attributes**

    allow_vote_change: :class:`bool`

    ended_at: :class:`datetime.datetime` or :class:`NoneType`

    hide_incomplete_results: :class:`bool`

    last_vote_at: :class:`datetime.datetime` or :class:`NoneType`

    max_votes: :class:`int`

    options: Sequence[:class:`PollOption`]

    started_at: :class:`datetime.datetime`

    title: :class:`dict`[:class:`str`, :class:`str`]
        Has two items bbcode: :class:`str` and html: :class:`str`

    total_vote_count: :class:`int`
    """

    __slots__ = (
        "allow_vote_change", "ended_at", "hide_incomplete_results", "last_vote_at",
        "max_votes", "options", "started_at", "title", "total_vote_count"
    )

    def __init__(self, data):
        self.allow_vote_change = data['allow_vote_change']
        self.ended_at = parser.parse(data["ended_at"]) if data["ended_at"] is not None else None
        self.hide_incomplete_results = data['hide_incomplete_results']
        self.last_vote_at = parser.parse(data["last_vote_at"]) if data["last_vote_at"] is not None else None
        self.max_votes = data['max_votes']
        self.options = list(map(PollOption, data['options']))
        self.started_at = parser.parse(data["started_at"])
        self.title = data['title']
        self.total_vote_count = data['total_vote_count']

    def __repr__(self):
        return prettify(self, 'title', 'options')


class PollOption:
    """
    **Attributes**

    id: :class:`int`

    text: :class:`dict`[:class:`str`, :class:`str`]
        Has two items bbcode: :class:`str` and html: :class:`str`

    vote_count: :class:`int` or :class:`NoneType`
    """

    __slots__ = ("id", "text", "vote_count")

    def __init__(self, data):
        self.id = data['id']
        self.text = data['text']
        self.vote_count = data['vote_count']

    def __repr__(self):
        return prettify(self, 'text', 'vote_count')
