from dateutil import parser
from typing import Optional, List, TYPE_CHECKING

from ..enums import GameModeStr, BeatmapsetEventType
from ..util import prettify
from .discussion import BeatmapsetDiscussion
from .beatmap import BeatmapsetCompact


if TYPE_CHECKING:
    from datetime import datetime


class BeatmapsetEventComment:
    """
    This object holds some extra information of the event.

    **Attributes**

    beatmap_discussion_id: Optional[:class:`int`]

    beatmap_discussion_post_id: Optional[:class:`int`]

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

    id: :class:`int`

    type: :class:`BeatmapsetEventType`

    comment: Optional[:class:`BeatmapsetEventComment`]
        Is None for the following types:
        - :class:`BeatmapsetEventType`.LOVE
        - :class:`BeatmapsetEventType`.QUALIFY
        - :class:`BeatmapsetEventType`.APPROVE
        - :class:`BeatmapsetEventType`.RANK

    created_at: :class:`datetime.datetime`

    user_id: Optional[:class:`int`]

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
        self.id: int = data["id"]
        self.type: BeatmapsetEventType = BeatmapsetEventType(data["type"])
        self.comment: Optional[BeatmapsetEventComment] = data["comment"]
        if self.comment is not None:
            self.comment = BeatmapsetEventComment(self.comment, self.type)  # type: ignore
        self.created_at: datetime = parser.parse(data["created_at"])
        self.user_id: Optional[int] = data.get("user_id")
        self.beatmapset: Optional[BeatmapsetCompact] = (
            BeatmapsetCompact(data["beatmapset"]) if data.get("beatmapset") is not None else None
        )
        self.discussion: Optional[BeatmapsetDiscussion] = (
            BeatmapsetDiscussion(data["discussion"]) if data.get("discussion") is not None else None
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
        self.modes: List[GameModeStr] = list(map(GameModeStr, data["modes"]))

    def __repr__(self):
        return prettify(self, "modes")


class BeatmapsetEventRemoveFromLoved:
    """
    **Attributes**

    reason: :class:`str`
    """

    __slots__ = ("reason",)

    def __init__(self, data):
        self.reason: str = data["reason"]

    def __repr__(self):
        return prettify(self, "reason")


class BeatmapsetEventDisqualify:
    """
    **Attributes**

    nominator_ids: List[:class:`int`]
    """

    __slots__ = ("nominator_ids",)

    def __init__(self, data):
        self.nominator_ids: List[int] = data["nominator_ids"]

    def __repr__(self):
        return prettify(self, "nominator_ids")


class BeatmapsetEventVote:
    """
    **Attributes**

    user_id: :class:`int`

    score: :class:`int`
    """

    __slots__ = ("user_id", "score")

    def __init__(self, data):
        self.user_id: int = data["user_id"]
        self.score: int = data["score"]

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
            BeatmapsetEventVote(data["new_votes"]) if data.get("new_votes") is not None else None
        )
        self.votes: Optional[List[BeatmapsetEventVote]] = (
            list(map(BeatmapsetEventVote, data["votes"])) if data.get("votes") is not None else None
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
            BeatmapsetEventVote(data["new_votes"]) if data.get("new_votes") is not None else None
        )

    def __repr__(self):
        return prettify(self, "new_votes")


class BeatmapsetEventDiscussionLock:
    """
    **Attributes**

    reason: :class:`str`
    """

    __slots__ = ("reason",)

    def __init__(self, data):
        self.reason: str = data["reason"]

    def __repr__(self):
        return prettify(self, "reason")


class BeatmapsetEventNominationReset:
    """
    **Attributes**

    nominator_ids: List[:class:`int`]
    """

    __slots__ = ("nominator_ids",)

    def __init__(self, data):
        self.nominator_ids: List[int] = data["nominator_ids"]

    def __repr__(self):
        return prettify(self, "nominator_ids")


class BeatmapsetEventNominationResetReceived:
    """
    **Attributes**

    source_user_id: :class:`int`

    source_user_name: :class:`str`
    """

    __slots__ = ("source_user_id", "source_user_username")

    def __init__(self, data):
        self.source_user_id: int = data["source_user_id"]
        self.source_user_username: str = data["source_user_username"]

    def __repr__(self):
        return prettify(self, "source_user_id", "source_user_username")


class BeatmapsetEventEdit:
    """
    **Attributes**

    old: :class:`str`

    new: :class:`str`
    """

    __slots__ = ("old", "new")

    def __init__(self, data):
        self.old: str = data["old"]
        self.new: str = data["new"]

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

    beatmap_id: :class:`int`

    beatmap_version: :class:`str`

    new_user_id: :class:`int`

    new_user_username: :class:`str`
    """

    __slots__ = ("beatmap_id", "beatmap_version", "new_user_id", "new_user_username")

    def __init__(self, data):
        self.beatmap_id: int = data["beatmap_id"]
        self.beatmap_version: str = data["beatmap_version"]
        self.new_user_id: int = data["new_user_id"]
        self.new_user_username: str = data["new_user_username"]

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
