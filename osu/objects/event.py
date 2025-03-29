from typing import Optional, TYPE_CHECKING, Union

from ..util import prettify, get_required, fromisoformat
from ..enums import GameModeStr, RankStatus
from .achievement import Achievement


if TYPE_CHECKING:
    from datetime import datetime


__all__ = (
    "Event",
    "AchievementEvent",
    "BeatmapPlaycountEvent",
    "BeatmapsetApproveEvent",
    "BeatmapsetDeleteEvent",
    "BeatmapsetReviveEvent",
    "BeatmapsetUpdateEvent",
    "BeatmapsetUploadEvent",
    "RankEvent",
    "RankLostEvent",
    "UserSupportAgainEvent",
    "UserSupportFirstEvent",
    "UserSupportGiftEvent",
    "UsernameChangeEvent",
    "EventUser",
    "EventBeatmap",
    "EventBeatmapset",
    "EVENT_TYPE",
    "get_event_object",
)


class Event:
    """
    Base class of an event

    **Attributes**

    created_at: :py:class:`datetime.datetime`

    id: int

    type:
        All types and the additional attributes they provide are listed under 'Event Types'
    """

    def __init__(self, data):
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.id: int = get_required(data, "id")


class AchievementEvent(Event):
    """
    **Attributes**

    achievement: :class:`Achievement`

    user: :class:`EventUser`
    """

    __slots__ = ("achievement", "user")

    def __init__(self, data):
        super().__init__(data)
        self.achievement: Achievement = Achievement(get_required(data, "achievement"))
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "achievement", "user")


class BeatmapPlaycountEvent(Event):
    """
    **Attributes**

    beatmap: :class:`EventBeatmap`

    count: int
    """

    __slots__ = ("beatmap", "count")

    def __init__(self, data):
        super().__init__(data)
        self.beatmap: EventBeatmap = EventBeatmap(get_required(data, "beatmap"))
        self.count: int = get_required(data, "count")

    def __repr__(self):
        return prettify(self, "beatmap", "count")


class BeatmapsetApproveEvent(Event):
    """
    **Attributes**

    approval: :class:`RankStatus`

    beatmapset: :class:`EventBeatmapset`

    user: :class:`EventUser`
    """

    __slots__ = ("approval", "beatmapset", "user")

    def __init__(self, data):
        super().__init__(data)
        self.approval: RankStatus = RankStatus[get_required(data, "approval").upper()]
        self.beatmapset: EventBeatmapset = EventBeatmapset(get_required(data, "beatmapset"))
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "beatmapset", "approval")


class BeatmapsetDeleteEvent(Event):
    """
    **Attributes**

    beatmapset: :class:`EventBeatmapset`
    """

    __slots__ = ("beatmapset",)

    def __init__(self, data):
        super().__init__(data)
        self.beatmapset: EventBeatmapset = EventBeatmapset(get_required(data, "beatmapset"))

    def __repr__(self):
        return prettify(self, "beatmapset")


class BeatmapsetReviveEvent(Event):
    """
    **Attributes**

    beatmapset: :class:`EventBeatmapset`

    user: :class:`EventUser`
    """

    __slots__ = ("beatmapset", "user")

    def __init__(self, data):
        super().__init__(data)
        self.beatmapset: EventBeatmapset = EventBeatmapset(get_required(data, "beatmapset"))
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "beatmapset", "user")


class BeatmapsetUpdateEvent(Event):
    """
    **Attributes**

    beatmapset: :class:`EventBeatmapset`

    user: :class:`EventUser`
    """

    __slots__ = ("beatmapset", "user")

    def __init__(self, data):
        super().__init__(data)
        self.beatmapset: EventBeatmapset = EventBeatmapset(get_required(data, "beatmapset"))
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "beatmapset", "user")


class BeatmapsetUploadEvent(Event):
    """
    **Attributes**

    beatmapset: :class:`EventBeatmapset`

    user: :class:`EventUser`
    """

    __slots__ = ("beatmapset", "user")

    def __init__(self, data):
        super().__init__(data)
        self.beatmapset: EventBeatmapset = EventBeatmapset(get_required(data, "beatmapset"))
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "beatmapset", "user")


class RankEvent(Event):
    """
    **Attributes**

    score_rank: str

    rank: int

    mode: :class:`GameModeStr`

    beatmap: :class:`EventBeatmap`

    user: :class:`EventUser`
    """

    __slots__ = ("score_rank", "rank", "mode", "beatmap", "user")

    def __init__(self, data):
        super().__init__(data)
        self.score_rank: str = get_required(data, "scoreRank")
        self.rank: int = get_required(data, "rank")
        self.mode: GameModeStr = GameModeStr(get_required(data, "mode"))
        self.beatmap: EventBeatmap = EventBeatmap(get_required(data, "beatmap"))
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "rank", "beatmap")


class RankLostEvent(Event):
    """
    **Attributes**

    mode: :class:`GameModeStr`

    beatmap: :class:`EventBeatmap`

    user: :class:`EventUser`
    """

    __slots__ = ("mode", "beatmap", "user")

    def __init__(self, data):
        super().__init__(data)
        self.mode: GameModeStr = GameModeStr(get_required(data, "mode"))
        self.beatmap: EventBeatmap = EventBeatmap(get_required(data, "beatmap"))
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "beatmap", "user")


class UserSupportAgainEvent(Event):
    """
    **Attributes**

    user: :class:`EventUser`
    """

    __slots__ = ("user",)

    def __init__(self, data):
        super().__init__(data)
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "user")


class UserSupportFirstEvent(Event):
    """
    **Attributes**

    user: :class:`EventUser`
    """

    __slots__ = ("user",)

    def __init__(self, data):
        super().__init__(data)
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "user")


class UserSupportGiftEvent(Event):
    """
    **Attributes**

    user: :class:`EventUser`
    """

    __slots__ = ("user",)

    def __init__(self, data):
        super().__init__(data)
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "user")


class UsernameChangeEvent(Event):
    """
    **Attributes**

    user: :class:`EventUser`
    """

    __slots__ = ("user",)

    def __init__(self, data):
        super().__init__(data)
        self.user: EventUser = EventUser(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "user")


class EventUser:
    """
    **Attributes**

    username: str

    url: str

    previous_username: Optional[str]
        Only for UsernameChangeEvent.
    """

    __slots__ = ("username", "url", "previous_username")

    def __init__(self, data):
        self.username: str = get_required(data, "username")
        self.url: str = get_required(data, "url")
        self.previous_username: Optional[str] = data.get("previousUsername")

    def __repr__(self):
        return prettify(self, "username")


class EventBeatmap:
    """
    **Attributes**

    title: str

    url: str
    """

    __slots__ = ("title", "url")

    def __init__(self, data):
        self.title: str = get_required(data, "title")
        self.url: str = get_required(data, "url")

    def __repr__(self):
        return prettify(self, "title")


class EventBeatmapset:
    """
    **Attributes**

    title: str

    url: str
    """

    __slots__ = ("title", "url")

    def __init__(self, data):
        self.title: str = get_required(data, "title")
        self.url: str = get_required(data, "url")

    def __repr__(self):
        return prettify(self, "title")


EVENT_TYPE = Union[
    AchievementEvent,
    BeatmapPlaycountEvent,
    BeatmapsetApproveEvent,
    BeatmapsetDeleteEvent,
    BeatmapsetReviveEvent,
    BeatmapsetUpdateEvent,
    BeatmapsetUploadEvent,
    RankEvent,
    RankLostEvent,
    UserSupportAgainEvent,
    UserSupportFirstEvent,
    UserSupportGiftEvent,
    UsernameChangeEvent,
]


def get_event_object(data) -> EVENT_TYPE:
    t = get_required(data, "type")
    cls = globals().get(t[0].upper() + t[1:] + "Event", data)
    return cls(data)
