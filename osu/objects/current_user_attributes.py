from typing import Optional, Dict

from ..util import prettify, get_optional, get_required
from ..enums import ObjectType, GameModeStr


class BeatmapsetDiscussionPermissions:
    """
    A user's permissions in a beatmapset discussion

    **Attributes**

    can_destroy: :class:`bool`

    can_reopen: :class:`bool`

    can_moderate_kudosu: :class:`bool`

    can_resolve: :class:`bool`

    vote_score: :class:`int`
    """

    __slots__ = (
        "can_destroy",
        "can_reopen",
        "can_moderate_kudosu",
        "can_resolve",
        "vote_score",
    )

    def __init__(self, data):
        self.can_destroy: bool = get_required(data, "can_destroy")
        self.can_reopen: bool = get_required(data, "can_reopen")
        self.can_moderate_kudosu: bool = get_required(data, "can_moderate_kudosu")
        self.can_resolve: bool = get_required(data, "can_resolve")
        self.vote_score: int = get_required(data, "vote_score")

    def __repr__(self):
        return prettify(self, "vote_score")


class BeatmapsetPermissions:
    """
    User permissions on a beatmapset

    **Attributes**

    can_beatmap_update_owner: :class:`bool`

    can_delete: :class:`bool`

    can_edit_metadata: :class:`bool`

    can_edit_offset: :class:`bool`

    can_edit_tags: :class:`bool`

    can_hype: :class:`bool`

    can_hype_reason: :class:`str`

    can_love: :class:`bool`

    can_remove_from_loved: :class:`bool`

    is_watching: :class:`bool`

    new_hype_time: Optional[:class:`str`]

    nomination_modes: Dict[:class:`GameModeStr`, :class:`str`]
        Values are either "full" or "limited".

    remaining_hype: :class:`int`
    """

    __slots__ = (
        "can_beatmap_update_owner",
        "can_delete",
        "can_edit_metadata",
        "can_edit_offset",
        "can_edit_tags",
        "can_hype",
        "can_hype_reason",
        "can_love",
        "can_remove_from_loved",
        "is_watching",
        "new_hype_time",
        "nomination_modes",
        "remaining_hype",
    )

    def __init__(self, data):
        self.can_beatmap_update_owner: bool = get_required(data, "can_beatmap_update_owner")
        self.can_delete: bool = get_required(data, "can_delete")
        self.can_edit_metadata: bool = get_required(data, "can_edit_metadata")
        self.can_edit_offset: bool = get_required(data, "can_edit_offset")
        self.can_edit_tags: bool = get_required(data, "can_edit_tags")
        self.can_hype: bool = get_required(data, "can_hype")
        self.can_hype_reason: str = get_required(data, "can_hype_reason")
        self.can_love: bool = get_required(data, "can_love")
        self.can_remove_from_loved: bool = get_required(data, "can_remove_from_loved")
        self.is_watching: bool = get_required(data, "is_watching")
        self.new_hype_time: Optional[str] = get_required(data, "new_hype_time")
        self.nomination_modes: Dict[GameModeStr, str] = get_optional(
            data,
            "nomination_modes",
            lambda value: dict(map(lambda item: (GameModeStr(item[0]), item[1]), value.items())),
        )
        self.remaining_hype: int = get_required(data, "remaining_hype")


class ChatChannelUserAttributes:
    """
    Data about a user related to a chat channel.

    **Attributes**

    can_message: :class:`bool`

    can_message_error: Optional[:class:`str`]

    last_read_id: Optional[:class:`int`]
    """

    __slots__ = ("can_message", "can_message_error", "last_read_id")

    def __init__(self, data):
        self.can_message: bool = get_required(data, "can_message")
        self.can_message_error: Optional[str] = get_required(data, "can_message_error")
        self.last_read_id: Optional[int] = get_required(data, "last_read_id")

    def __repr__(self):
        return prettify(self, "can_message", "last_read_id")


class ScoreUserAttributes:
    """
    Gives info about a score related to the current user

    **Attributes**

    Optional[:class:`CurrentUserPin`]
    """

    __slots__ = ("pin",)

    def __init__(self, data):
        self.pin: Optional[CurrentUserPin] = get_optional(data, "pin", CurrentUserPin)


class CurrentUserPin:
    """
    Gives info about a score related to if it's pinned or not

    **Attributes**

    is_pinned: :class:`bool`

    score_id: :class:`int`

    score_type: Optional[:class:`ObjectType`]
    """

    __slots__ = ("is_pinned", "score_id", "score_type")

    def __init__(self, data):
        self.is_pinned: bool = get_required(data, "is_pinned")
        self.score_id: int = get_required(data, "score_id")
        self.score_type: Optional[ObjectType] = get_optional(data, "score_type", ObjectType)


class CommentableMetaAttributes:
    """
    User attributes for a :class:`CommentableMeta` object

    **Attributes**

    can_new_comment_reason: Optional[:class:`str`]
    """

    __slots__ = ("can_new_comment_reason",)

    def __init__(self, data):
        self.can_new_comment_reason = get_required(data, "can_new_comment_reason")
