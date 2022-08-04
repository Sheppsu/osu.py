from .user import CurrentUserAttributes
from .beatmap import BeatmapCompact, BeatmapsetCompact
from dateutil import parser

from ..util import prettify


class BeatmapsetDiscussion:
    """
    Represents a Beatmapset modding discussion

    **Attributes**

    beatmap: :class:`BeatmapCompact` or :class:`NoneType`

    beatmap_id: :class:`int` or :class:`NoneType`

    beatmapset: :class:`BeatmapsetCompact` or :class:`NoneType`

    beatmapset_id: :class:`int`

    can_be_resolved: :class:`bool`

    can_grant_kudosu: :class:`bool`

    created_at: :class:`datetime.datetime`

    current_user_attributes: :class:`CurrentUserAttributes`

    deleted_at: :class:`datetime.datetime` or :class:`NoneType`

    deleted_by_id: :class:`int`

    id: :class:`int`

    kudosu_denied: :class:`bool`

    last_post_at: :class:`datetime.datetime`

    message_type: :class:`str`
        can be any of the following: hype, mapper_note, praise, problem, review, suggestion

    parent_id: :class:`int` or :class:`NoneType`

    posts: :class:`list`
        list contains objects of type :class:`BeatmapsetDiscussionPost`

    resolved: :class:`bool`

    starting_post: :class:`BeatmapsetDiscussionPost`

    timestamp: :class:`int` or :class:`NoneType`

    updated_at: :class:`datetime.datetime`

    user_id: :class:`int`
    """
    __slots__ = (
        "beatmap", "beatmap_id", "beatmapset", "beatmapset_id", "can_be_resolved", "can_grant_kudosu",
        "created_at", "current_user_attributes", "deleted_at", "deleted_by_id", "id", "kudosu_denied",
        "last_post_at", "message_type", "parent_id", "posts", "resolved", "starting_post", "timestamp",
        "updated_at", "user_id", "votes"
    )

    def __init__(self, data):
        self.beatmap = BeatmapCompact(data['beatmap']) if data.get('beatmap') is not None else None
        self.beatmap_id = data['beatmap_id']
        self.beatmapset = BeatmapsetCompact(data['beatmapset']) if data.get('beatmapset') is not None else None
        self.beatmapset_id = data['beatmapset_id']
        self.can_be_resolved = data['can_be_resolved']
        self.can_grant_kudosu = data['can_grant_kudosu']
        self.created_at = parser.parse(data['created_at'])
        self.current_user_attributes = CurrentUserAttributes(data['current_user_attributes'],
                                                             'BeatmapsetDiscussionPermissions') \
            if 'current_user_attributes' in data else None
        self.deleted_at = parser.parse(data['deleted_at']) if data['deleted_at'] is not None else None
        self.deleted_by_id = data['deleted_by_id'] if 'deleted_by_id' in data else None
        self.id = data['id']
        self.kudosu_denied = data['kudosu_denied']
        self.last_post_at = parser.parse(data['last_post_at'])
        self.message_type = data['message_type']
        self.parent_id = data['parent_id'] if 'parent_id' in data else None
        self.posts = list(map(BeatmapsetDiscussionPost, data['posts'])) if 'posts' in data else None
        self.resolved = data['resolved']
        self.starting_post = BeatmapsetDiscussionPost(data['starting_post']) if 'starting_post' in data else None
        self.timestamp = data['timestamp'] if 'timestamp' in data else None
        self.updated_at = parser.parse(data['updated_at'])
        self.user_id = data['user_id']

    def __repr__(self):
        return prettify(self, 'beatmapset', 'starting_post')


class BeatmapsetDiscussionPost:
    """
    Represents a post in a :class:`BeatmapsetDiscussion`.

    **Attributes**

    beatmapset_discussion_id: :class:`int`

    created_at: :class:`datetime.datetime`

    deleted_at: :class:`datetime.datetime` or :class:`NoneType`

    deleted_by_id: :class:`int` or :class:`NoneType`

    id: :class:`int`

    last_editor_id: :class:`int` or :class:`NoneType`

    message: :class:`str`

    system: :class:`bool`

    updated_at: :class:`datetime.datetime`

    user_id: :class:`int`
    """
    __slots__ = (
        "beatmapset_discussion_id", "created_at", "deleted_at", "deleted_by_id", "id",
        "last_editor_id", "message", "system", "updated_at", "user_id"
    )

    def __init__(self, data):
        self.beatmapset_discussion_id = data['beatmapset_discussion_id']
        self.created_at = parser.parse(data['created_at'])
        self.deleted_at = parser.parse(data['deleted_at']) if data['deleted_at'] is not None else None
        self.deleted_by_id = data['deleted_by_id']
        self.id = data['id']
        self.last_editor_id = data['last_editor_id']
        self.message = data['message']
        self.system = data['system']
        self.updated_at = parser.parse(data['updated_at'])
        self.user_id = data['user_id']

    def __repr__(self):
        return prettify(self, 'user_id', 'message', 'beatmapset_discussion_id')


class BeatmapsetDiscussionVote:
    """
    Represents a vote on a :class:`BeatmapsetDiscussion`.

    **Attributes**

    beatmapset_discussion_id: :class:`int`

    created_at: :class:`datetime.datetime`

    id: :class:`int`

    score: :class:`int`

    updated_at: :class:`datetime.datetime`

    user_id: :class:`int`
    """
    __slots__ = (
        "beatmapset_discussion_id", "created_at", "id", "score",
        "updated_at", "user_id"
    )

    def __init__(self, data):
        self.beatmapset_discussion_id = data['beatmapset_discussion_id']
        self.created_at = parser.parse(data['created_at'])
        self.id = data['id']
        self.score = data['score']
        self.updated_at = parser.parse(data['updated_at'])
        self.user_id = data['user_id']

    def __repr__(self):
        return prettify(self, 'beatmapset_discussion_id', 'score', 'user_id')
