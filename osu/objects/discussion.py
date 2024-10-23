from typing import Optional, List, TYPE_CHECKING, Union

from ..util import prettify, get_optional, get_optional_list, get_required, fromisoformat
from ..enums import MessageType
from .current_user_attributes import BeatmapsetDiscussionPermissions
from .beatmap import BeatmapCompact, BeatmapsetCompact


if TYPE_CHECKING:
    from datetime import datetime


class BeatmapsetDiscussion:
    """
    Represents a Beatmapset modding discussion

    **Attributes**

    beatmap_id: Optional[:class:`int`]

    beatmapset_id: :class:`int`

    can_be_resolved: :class:`bool`

    can_grant_kudosu: :class:`bool`

    created_at: :class:`datetime.datetime`

    deleted_at: Optional[:class:`datetime.datetime`]

    deleted_by_id: Optional[:class:`int`]

    id: :class:`int`

    kudosu_denied: :class:`bool`

    last_post_at: :class:`datetime.datetime`

    message_type: :class:`MessageType`

    parent_id: Optional[:class:`int`]

    resolved: :class:`bool`

    timestamp: Optional[:class:`int`]

    updated_at: :class:`datetime.datetime`

    user_id: :class:`int`

    beatmap: Optional[:class:`BeatmapCompact`]

    beatmapset: Optional[:class:`BeatmapsetCompact`]

    current_user_attributes: Optional[:class:`BeatmapsetDiscussionPermissions`]

    posts: Optional[List[:class:`BeatmapsetDiscussionPost`]]

    starting_post: Optional[:class:`BeatmapsetDiscussionPost`]

    votes: Optional[:class:`VotesSummary`]
    """

    __slots__ = (
        "beatmap_id",
        "beatmapset_id",
        "can_be_resolved",
        "can_grant_kudosu",
        "created_at",
        "deleted_at",
        "deleted_by_id",
        "id",
        "kudosu_denied",
        "last_post_at",
        "message_type",
        "parent_id",
        "resolved",
        "timestamp",
        "updated_at",
        "user_id",
        "beatmap",
        "beatmapset",
        "current_user_attributes",
        "posts",
        "starting_post",
        "votes",
    )

    def __init__(self, data):
        self.beatmap_id: Optional[int] = get_required(data, "beatmap_id")
        self.beatmapset_id: int = get_required(data, "beatmapset_id")
        self.can_be_resolved: bool = get_required(data, "can_be_resolved")
        self.can_grant_kudosu: bool = get_required(data, "can_grant_kudosu")
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", fromisoformat)
        self.deleted_by_id: Optional[int] = get_required(data, "deleted_by_id")
        self.id: int = get_required(data, "id")
        self.kudosu_denied: bool = get_required(data, "kudosu_denied")
        self.last_post_at: datetime = fromisoformat(get_required(data, "last_post_at"))
        self.message_type: MessageType = MessageType(get_required(data, "message_type"))
        self.parent_id: Optional[int] = get_required(data, "parent_id")
        self.resolved: bool = get_required(data, "resolved")
        self.timestamp: Optional[int] = data.get("timestamp")
        self.updated_at: datetime = fromisoformat(get_required(data, "updated_at"))
        self.user_id: int = get_required(data, "user_id")

        self.beatmap: Optional[BeatmapCompact] = get_optional(data, "beatmap", BeatmapCompact)
        self.beatmapset: Optional[BeatmapsetCompact] = get_optional(data, "beatmapset", BeatmapsetCompact)
        self.current_user_attributes: Optional[BeatmapsetDiscussionPermissions] = get_optional(
            data, "current_user_attributes", BeatmapsetDiscussionPermissions
        )
        self.posts: Optional[List[BeatmapsetDiscussionPost]] = get_optional_list(
            data, "posts", BeatmapsetDiscussionPost
        )
        self.starting_post: Optional[BeatmapsetDiscussionPost] = get_optional(
            data, "starting_post", BeatmapsetDiscussionPost
        )
        self.votes: VotesSummary = get_optional(data, "votes", VotesSummary)

    def __repr__(self):
        return prettify(self, "beatmapset", "starting_post")


class VotesSummary:
    """
    Summarizes the votes of a discussion

    **Attributes**

    down: :class:`int`
        Number of downvotes

    up: :class:`int`
        Number of upvotes

    voters: :class:`VotersSummary`
        summarizes who voted up and down
    """

    __slots__ = ("down", "up", "voters")

    def __init__(self, data):
        self.down: int = get_required(data, "down")
        self.up: int = get_required(data, "up")
        self.voters: VotersSummary = VotersSummary(get_required(data, "voters"))


class VotersSummary:
    """
    Gives a summary of players who voted up and down on a discussion

    **Attributes**

    down: List[:class:`int`]
        List of user IDs of users that downvoted

    up: List[:class:`int`]
        List of user IDs of users that upvoted
    """

    __slots__ = ("down", "up")

    def __init__(self, data):
        self.down: List[int] = get_required(data, "down")
        self.up: List[int] = get_required(data, "up")


class BeatmapsetDiscussionPost:
    """
    Represents a post in a :class:`BeatmapsetDiscussion`.

    **Attributes**

    beatmapset_discussion_id: :class:`int`

    created_at: :class:`datetime.datetime`

    deleted_at: Optional[:class:`datetime.datetime`]

    deleted_by_id: Optional[:class:`int`]

    id: :class:`int`

    last_editor_id: Optional[:class:`int`]

    updated_at: :class:`datetime.datetime`

    user_id: :class:`int`

    message: Union[:class:`str`, :class:`SystemDiscussionPostMessage`]
        String when `system` is false and :class:`SystemDiscussionPostMessage` otherwise.

    system: :class:`bool`

    beatmap_discussion: Optional[:class:`BeatmapsetDiscussion`]
    """

    __slots__ = (
        "beatmapset_discussion_id",
        "created_at",
        "deleted_at",
        "deleted_by_id",
        "id",
        "last_editor_id",
        "updated_at",
        "user_id",
        "message",
        "system",
        "beatmap_discussion",
    )

    def __init__(self, data):
        self.beatmapset_discussion_id: int = get_required(data, "beatmapset_discussion_id")
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", fromisoformat)
        self.deleted_by_id: Optional[int] = data.get("deleted_by_id")
        self.id: int = get_required(data, "id")
        self.last_editor_id: Optional[int] = data.get("last_editor_id")
        self.updated_at: datetime = fromisoformat(get_required(data, "updated_at"))
        self.user_id: int = get_required(data, "user_id")

        self.system: bool = get_required(data, "system")
        self.message: Union[str, SystemDiscussionPostMessage] = (
            SystemDiscussionPostMessage(get_required(data, "message")) if self.system else get_required(data, "message")
        )

        self.beatmap_discussion: Optional[BeatmapsetDiscussion] = get_optional(
            data, "beatmap_discussion", BeatmapsetDiscussion
        )

    def __repr__(self):
        return prettify(self, "user_id", "message")


class SystemDiscussionPostMessage:
    """
    System message of :class:`BeatmapsetDiscussionPost`

    **Attributes**

    type: :class:`str`

    value: :class:`bool`
    """

    __slots__ = ("type", "value")

    def __init__(self, data):
        self.type: str = get_required(data, "type")
        self.value: bool = get_required(data, "value")


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
        "beatmapset_discussion_id",
        "created_at",
        "id",
        "score",
        "updated_at",
        "user_id",
    )

    def __init__(self, data):
        self.beatmapset_discussion_id: int = get_required(data, "beatmapset_discussion_id")
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.id: int = get_required(data, "id")
        self.score: int = get_required(data, "score")
        self.updated_at: datetime = fromisoformat(get_required(data, "updated_at"))
        self.user_id: int = get_required(data, "user_id")

    def __repr__(self):
        return prettify(self, "user_id", "score")


class Review:
    """
    **Attributes**

    max_blocks: :class:`int`
    """

    __slots__ = ("max_blocks",)

    def __init__(self, data):
        self.max_blocks: int = get_required(data, "max_blocks")
