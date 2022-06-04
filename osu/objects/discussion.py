from .user import CurrentUserAttributes
from .beatmap import BeatmapCompact, BeatmapsetCompact


class BeatmapsetDiscussion:
    """
    Represents a Beatmapset modding discussion

    **Attributes**

    beatmap: :class:`BeatmapCompact`

    beatmap_id: :class:`int`

    beatmapset: :class:`BeatmapsetCompact`

    beatmapset_id: :class:`int`

    can_be_resolved: :class:`bool`

    can_grant_kudosu: :class:`bool`

    created_at: :ref:`Timestamp`

    current_user_attributes: :class:`CurrentUserAttributes`

    deleted_at: :ref:`Timestamp`

    deleted_by_id: :class:`int`

    id: :class:`int`

    kudosu_denied: :class:`bool`

    last_post_at: :ref:`Timestamp`

    message_type: :class:`MessageType`
        :class:`MessageType` can be one of the following, all of which being :class:`str`, hype, mapper_note, praise, review, suggestion

    parent_id: :class:`int`

    posts: :class:`list`
        list contains objects of type :class:`BeatmapsetDiscussionPost`

    resolved: :class:`bool`

    starting_post: :class:`BeatmapsetDiscussionPost`

    timestamp: :class:`int`

    updated_at: :ref:`Timestamp`

    user_id: :class:`int`

    votes: :class:`list`
        list containing objects of type :class:`BeatmapsetDiscussionVote`
    """
    __slots__ = (
        "beatmap", "beatmap_id", "beatmapset", "beatmapset_id", "can_be_resolved", "can_grant_kudosu",
        "created_at", "current_user_attributes", "deleted_at", "deleted_by_id", "id", "kudosu_denied",
        "last_post_at", "message_type", "parent_id", "posts", "resolved", "starting_post", "timestamp",
        "updated_at", "user_id", "votes"
    )

    def __init__(self, data):
        self.beatmap = BeatmapCompact(data['beatmap'])
        self.beatmap_id = data['beatmap_id']
        self.beatmapset = BeatmapsetCompact(data['beatmapset'])
        self.beatmapset_id = data['beatmapset_id']
        self.can_be_resolved = data['can_be_resolved']
        self.can_grant_kudosu = data['can_grant_kudosu']
        self.created_at = data['created_at']
        self.current_user_attributes = CurrentUserAttributes(data['current_user_attributes'], 'BeatmapsetDiscussionPermissions')
        self.deleted_at = data['deleted_at']
        self.deleted_by_id = data['deleted_by_id']
        self.id = data['id']
        self.kudosu_denied = data['kudosu_denied']
        self.last_post_at = data['last_post_at']
        self.message_type = MessageType(data['message_type'])
        self.parent_id = data['parent_id']
        self.posts = [BeatmapsetDiscussionPost(post) for post in data['posts']]
        self.resolved = data['resolved']
        self.starting_post = BeatmapsetDiscussionPost(data['starting_post'])
        self.timestamp = data['timestamp']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.votes = [BeatmapsetDiscussionVote(vote) for vote in data['votes']]


class BeatmapsetDiscussionPost:
    """
    Represents a post in a :class:`BeatmapsetDiscussion`.

    **Attributes**

    beatmapset_discussion_id: :class:`int`

    created_at: :ref:`Timestamp`

    deleted_at: :ref:`Timestamp`

    deleted_by_id: :class:`int`

    id: :class:`int`

    last_editor_id: :class:`int`

    message: :class:`str`

    system: :class:`bool`

    updated_at: :ref:`Timestamp`

    user_id: :class:`int`
    """
    __slots__ = (
        "beatmapset_discussion_id", "created_at", "deleted_at", "deleted_by_id", "id",
        "last_editor_id", "message", "system", "updated_at", "user_id"
    )

    def __init__(self, data):
        self.beatmapset_discussion_id = data['beatmapset_discussion_id']
        self.created_at = data['created_at']
        self.deleted_at = data['deleted_at']
        self.deleted_by_id = data['deleted_by_id']
        self.id = data['id']
        self.last_editor_id = data['last_editor_id']
        self.message = data['message']
        self.system = data['system']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


class BeatmapsetDiscussionVote:
    """
    Represents a vote on a :class:`BeatmapsetDiscussion`.

    **Attributes**

    beatmapset_discussion_id: :class:`int`

    created_at: :ref:`Timestamp`

    id: :class:`int`

    score: :class:`int`

    updated_at: :ref:`Timestamp`

    user_id: :class:`int`
    """
    __slots__ = (
        "beatmapset_discussion_id", "created_at", "id", "score",
        "updated_at", "user_id"
    )

    def __init__(self, data):
        self.beatmapset_discussion_id = data['beatmapset_discussion_id']
        self.created_at = data['created_at']
        self.id = data['id']
        self.score = data['score']
        self.updated_at = data['updated_at']
        self.user_id = data['user']


class MessageType:
    """
    **Attributes**

    hype

    mapper_note

    praise

    problem

    review

    suggestion
    """
    __slots__ = (
        "hype", "mapper_note", "praise", "problem", "review", "suggestion"
    )

    def __init__(self, data):
        self.hype = data['hype']
        self.mapper_note = data['mapper_note']
        self.praise = data['praise']
        self.problem = data['problem']
        self.review = data['review']
        self.suggestion = data['suggestion']
