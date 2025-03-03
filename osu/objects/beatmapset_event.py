from typing import Optional, List, TYPE_CHECKING

from ..enums import GameModeStr, BeatmapsetEventType
from ..util import prettify, get_required, fromisoformat
from .discussion import BeatmapsetDiscussion
from .beatmap import BeatmapsetCompact


if TYPE_CHECKING:
    from datetime import datetime


__all__ = (
    "BeatmapsetEventComment",
    "BeatmapsetEvent",
    "BeatmapsetEventNominate",
    "BeatmapsetEventRemoveFromLoved",
    "BeatmapsetEventDisqualify",
    "BeatmapsetEventVote",
    "BeatmapsetEventKudosuChange",
    "BeatmapsetEventKudosuGain",
    "BeatmapsetEventKudosuLost",
    "BeatmapsetEventKudosuRecalculate",
    "BeatmapsetEventDiscussionLock",
    "BeatmapsetEventNominationReset",
    "BeatmapsetEventNominationResetReceived",
    "BeatmapsetEventEdit",
    "BeatmapsetEventGenreEdit",
    "BeatmapsetEventLanguageEdit",
    "BeatmapsetEventNsfwToggle",
    "BeatmapsetEventOffsetEdit",
    "BeatmapsetEventBeatmapOwnerChange",
)


class BeatmapsetEventComment:
    """
    This object holds some extra information of the event.

    **Attributes**

    beatmap_discussion_id: Optional[int]

    beatmap_discussion_post_id: Optional[int]

    event_data: Union[:class:`BeatmapsetEventNominate`, :class:`BeatmapsetEventRemoveFromLoved`,
    :class:`BeatmapsetEventDisqualify`, :class:`BeatmapsetEventKudosuGain`, :class:`BeatmapsetEventKudosuLost`,
    :class:`BeatmapsetEventKudosuRecalculate`, :class:`BeatmapsetEventDiscussionLock`,
    :class:`BeatmapsetEventNominationReset`, :class:`BeatmapsetEventNominationResetReceived`,
    :class:`BeatmapsetEventGenreEdit`, :class:`BeatmapsetEventLanguageEdit`, :class:`BeatmapsetEventNsfwToggle`,
    :class:`BeatmapsetEventOffsetEdit`, :class:`BeatmapsetEventBeatmapOwnerChange`]

        The type of this attribute depends on the type of the BeatmapsetEvent object.
    """

    __slots__ = ("beatmap_discussion_id", "beatmap_discussion_post_id", "event_data")

    def __init__(self, data, type: BeatmapsetEventType):
        self.beatmap_discussion_id: Optional[int] = data.get("beatmap_discussion_id")
        self.beatmap_discussion_post_id: Optional[int] = data.get("beatmap_discussion_post_id")
        self.event_data = _get_event_data_object(data, type)

    def __repr__(self):
        return prettify(self, "beatmap_discussion_id", "beatmap_discussion_post_id")


class BeatmapsetEvent:
    """
    Represent a beatmapset event. This object is relevant for the :func:`osu.Client.get_beatmapset_events` endpoint.

    **Attributes**

    id: int

    type: :class:`BeatmapsetEventType`

    comment: Optional[:class:`BeatmapsetEventComment`]
        Is None for the following types:
        - :class:`BeatmapsetEventType`.LOVE
        - :class:`BeatmapsetEventType`.QUALIFY
        - :class:`BeatmapsetEventType`.APPROVE
        - :class:`BeatmapsetEventType`.RANK

    created_at: :py:class:`datetime.datetime`

    user_id: Optional[int]

    beatmapset: Optional[:class:`BeatmapsetCompact`]

    discussion: Optional[:class:`BeatmapsetDiscussion`]
    """

    __slots__ = (
        "id",
        "type",
        "comment",
        "created_at",
        "user_id",
        "beatmapset",
        "discussion",
    )

    def __init__(self, data):
        self.id: int = get_required(data, "id")
        self.type: BeatmapsetEventType = BeatmapsetEventType(get_required(data, "type"))
        self.comment: Optional[BeatmapsetEventComment] = get_required(data, "comment")
        if self.comment is not None:
            self.comment = BeatmapsetEventComment(self.comment, self.type)  # type: ignore
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.user_id: Optional[int] = data.get("user_id")
        self.beatmapset: Optional[BeatmapsetCompact] = (
            BeatmapsetCompact(get_required(data, "beatmapset")) if data.get("beatmapset") is not None else None
        )
        self.discussion: Optional[BeatmapsetDiscussion] = (
            BeatmapsetDiscussion(get_required(data, "discussion")) if data.get("discussion") is not None else None
        )

    def __repr__(self):
        return prettify(self, "type", "beatmapset")


class BeatmapsetEventNominate:
    """
    **Attributes**

    modes: List[:class:`GameModeStr`]
    """

    __slots__ = ("modes",)

    def __init__(self, data):
        self.modes: List[GameModeStr] = list(map(GameModeStr, get_required(data, "modes")))

    def __repr__(self):
        return prettify(self, "modes")


class BeatmapsetEventRemoveFromLoved:
    """
    **Attributes**

    reason: str
    """

    __slots__ = ("reason",)

    def __init__(self, data):
        self.reason: str = get_required(data, "reason")

    def __repr__(self):
        return prettify(self, "reason")


class BeatmapsetEventDisqualify:
    """
    **Attributes**

    nominator_ids: List[int]
    """

    __slots__ = ("nominator_ids",)

    def __init__(self, data):
        self.nominator_ids: List[int] = get_required(data, "nominator_ids")

    def __repr__(self):
        return prettify(self, "nominator_ids")


class BeatmapsetEventVote:
    """
    **Attributes**

    user_id: int

    score: int
    """

    __slots__ = ("user_id", "score")

    def __init__(self, data):
        self.user_id: int = get_required(data, "user_id")
        self.score: int = get_required(data, "score")

    def __repr__(self):
        return prettify(self, "user_id", "score")


class BeatmapsetEventKudosuChange:
    """
    **Attributes**

    new_votes: Optional[:class:`BeatmapsetEventVote`]

    votes: Optional[List[:class:`BeatmapsetEventVote`]]
    """

    __slots__ = ("new_votes", "votes")

    def __init__(self, data):
        self.new_votes: Optional[BeatmapsetEventVote] = (
            BeatmapsetEventVote(get_required(data, "new_votes")) if data.get("new_votes") is not None else None
        )
        self.votes: Optional[List[BeatmapsetEventVote]] = (
            list(map(BeatmapsetEventVote, get_required(data, "votes"))) if data.get("votes") is not None else None
        )

    def __repr__(self):
        return prettify(self, "new_votes", "votes")


class BeatmapsetEventKudosuGain(BeatmapsetEventKudosuChange):
    __doc__ = BeatmapsetEventKudosuChange.__doc__


class BeatmapsetEventKudosuLost(BeatmapsetEventKudosuChange):
    __doc__ = BeatmapsetEventKudosuChange.__doc__


class BeatmapsetEventKudosuRecalculate:
    """
    **Attributes**

    new_votes: Optional[:class:`BeatmapsetEventVote`]
    """

    __slots__ = ("new_votes",)

    def __init__(self, data):
        self.new_votes: Optional[BeatmapsetEventVote] = (
            BeatmapsetEventVote(get_required(data, "new_votes")) if data.get("new_votes") is not None else None
        )

    def __repr__(self):
        return prettify(self, "new_votes")


class BeatmapsetEventDiscussionLock:
    """
    **Attributes**

    reason: str
    """

    __slots__ = ("reason",)

    def __init__(self, data):
        self.reason: str = get_required(data, "reason")

    def __repr__(self):
        return prettify(self, "reason")


class BeatmapsetEventNominationReset:
    """
    **Attributes**

    nominator_ids: List[int]
    """

    __slots__ = ("nominator_ids",)

    def __init__(self, data):
        self.nominator_ids: List[int] = get_required(data, "nominator_ids")

    def __repr__(self):
        return prettify(self, "nominator_ids")


class BeatmapsetEventNominationResetReceived:
    """
    **Attributes**

    source_user_id: int

    source_user_name: str
    """

    __slots__ = ("source_user_id", "source_user_username")

    def __init__(self, data):
        self.source_user_id: int = get_required(data, "source_user_id")
        self.source_user_username: str = get_required(data, "source_user_username")

    def __repr__(self):
        return prettify(self, "source_user_id", "source_user_username")


class BeatmapsetEventEdit:
    """
    **Attributes**

    old: str

    new: str
    """

    __slots__ = ("old", "new")

    def __init__(self, data):
        self.old: str = get_required(data, "old")
        self.new: str = get_required(data, "new")

    def __repr__(self):
        return prettify(self, "old", "new")


class BeatmapsetEventGenreEdit(BeatmapsetEventEdit):
    __doc__ = BeatmapsetEventEdit.__doc__


class BeatmapsetEventLanguageEdit(BeatmapsetEventEdit):
    __doc__ = BeatmapsetEventEdit.__doc__


class BeatmapsetEventNsfwToggle(BeatmapsetEventEdit):
    __doc__ = BeatmapsetEventEdit.__doc__


class BeatmapsetEventOffsetEdit(BeatmapsetEventEdit):
    __doc__ = BeatmapsetEventEdit.__doc__


class BeatmapsetEventBeatmapOwnerChange:
    """
    **Attributes**

    beatmap_id: int

    beatmap_version: str

    new_user_id: int

    new_user_username: str
    """

    __slots__ = ("beatmap_id", "beatmap_version", "new_user_id", "new_user_username")

    def __init__(self, data):
        self.beatmap_id: int = get_required(data, "beatmap_id")
        self.beatmap_version: str = get_required(data, "beatmap_version")
        self.new_user_id: int = get_required(data, "new_user_id")
        self.new_user_username: str = get_required(data, "new_user_username")

    def __repr__(self):
        return prettify(self, "beatmap_id", "new_user_username")


_EVENT_TYPES = {
    BeatmapsetEventType.NOMINATE: BeatmapsetEventNominate,
    BeatmapsetEventType.REMOVE_FROM_LOVED: BeatmapsetEventRemoveFromLoved,
    BeatmapsetEventType.DISQUALIFY: BeatmapsetEventDisqualify,
    BeatmapsetEventType.KUDOSU_GAIN: BeatmapsetEventKudosuGain,
    BeatmapsetEventType.KUDOSU_LOST: BeatmapsetEventKudosuLost,
    BeatmapsetEventType.KUDOSU_RECALCULATE: BeatmapsetEventKudosuRecalculate,
    BeatmapsetEventType.DISCUSSION_LOCK: BeatmapsetEventDiscussionLock,
    BeatmapsetEventType.NOMINATION_RESET: BeatmapsetEventNominationReset,
    BeatmapsetEventType.NOMINATION_RESET_RECEIVED: BeatmapsetEventNominationResetReceived,
    BeatmapsetEventType.GENRE_EDIT: BeatmapsetEventGenreEdit,
    BeatmapsetEventType.LANGUAGE_EDIT: BeatmapsetEventLanguageEdit,
    BeatmapsetEventType.NSFW_TOGGLE: BeatmapsetEventNsfwToggle,
    BeatmapsetEventType.OFFSET_EDIT: BeatmapsetEventOffsetEdit,
    BeatmapsetEventType.BEATMAP_OWNER_CHANGE: BeatmapsetEventBeatmapOwnerChange,
}


def _get_event_data_object(data, type):
    return _EVENT_TYPES[type](data) if type in _EVENT_TYPES else None
