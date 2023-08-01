from dateutil import parser
from typing import Dict, Optional, List, TYPE_CHECKING, Union

from ..enums import (
    GameModeInt,
    PlaylistQueueMode,
    RealTimeQueueMode,
    RoomCategory,
    RoomType,
)
from ..util import prettify, get_optional, get_optional_list
from .user import UserCompact
from .beatmap import BeatmapCompact
from .score import ScoreDataStatistics, LazerMod


if TYPE_CHECKING:
    from datetime import datetime


class MultiplayerScore:
    """
    Score data.

    **Attributes**

    id: :class:`int`

    user_id: :class:`int`

    room_id: :class:`int`

    playlist_item_id: :class:`int`

    beatmap_id: :class:`int`

    rank: :class:`str`

    total_score: :class:`int`

    accuracy: :class:`float`

    max_combo: :class:`int`

    mods: List[:class:`LazerMod`]

    statistics: :class:`ScoreDataStatistics`

    passed: :class:`bool`

    position: Optional[:class:`int`]

    scores_around: Optional[:class:`MultiplayerScoresAround`]
        Scores around the specified score.

    user: :class:`User`
    """

    __slots__ = (
        "id",
        "user_id",
        "room_id",
        "playlist_item_id",
        "beatmap_id",
        "rank",
        "total_score",
        "accuracy",
        "max_combo",
        "mods",
        "statistics",
        "passed",
        "position",
        "scores_around",
        "user",
    )

    def __init__(self, data):
        self.id: int = data["id"]
        self.user_id: int = data["user_id"]
        self.room_id: int = data["room_id"]
        self.playlist_item_id: int = data["playlist_item_id"]
        self.beatmap_id: int = data["beatmap_id"]
        self.rank: str = data["rank"]
        self.total_score: int = data["total_score"]
        self.accuracy: float = data["accuracy"]
        self.max_combo: int = data["max_combo"]
        self.mods: Optional[List[LazerMod]] = get_optional_list(data, "mods", LazerMod)
        self.statistics: ScoreDataStatistics = ScoreDataStatistics(data["statistics"])
        self.passed: bool = data["passed"]
        self.position: Optional[int] = data.get("position")
        self.scores_around: Optional[MultiplayerScoresAround] = get_optional(
            data, "scores_around", MultiplayerScoresAround
        )
        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)

    def __repr__(self):
        return prettify(self, "user", "position")


class MultiplayerScores:
    """
    An object which contains scores and related data for fetching next page of the result.

    **Attributes**

    cursor: :class:`str`
        To be used to fetch the next page.

    params: :class:`dict`
        To be used to fetch the next page.

    scores: List[:class:`MultiplayerScore`]

    total: Optional[:class:`int`]
        Index only. Total scores of the specified playlist item.

    user_score: Optional[:class:`MultiplayerScore`]
        Index only. Score of the accessing user if exists.
    """

    __slots__ = ("cursor", "params", "scores", "total", "user_score")

    def __init__(self, data):
        self.cursor: str = data["cursor"]
        self.params: Dict = data["params"]
        self.scores: List[MultiplayerScore] = list(map(MultiplayerScore, data["scores"]))
        self.total: Optional[int] = data.get("total")
        self.user_score: Optional[MultiplayerScore] = get_optional(data, "user_score", MultiplayerScore)

    def __repr__(self):
        return prettify(self, "total", "scores")


class MultiplayerScoresAround:
    """
    **Attributes**

    higher: :class:`MultiplayerScores`

    lower: :class:`MultiplayerScores`
    """

    __slots__ = ("higher", "lower")

    def __init__(self, data):
        self.higher: MultiplayerScores = MultiplayerScores(data["higher"])
        self.lower: MultiplayerScores = MultiplayerScores(data["lower"])

    def __repr__(self):
        return prettify(self, "higher", "lower")


class Room:
    """
    :func:`osu.Client.get_rooms` and :func:`osu.Client.get_room` endpoints include host, playlist,
    and recent_participants attributes. In addition, the :class:`PlaylistItem` objects in playlist
    include the beatmap attribute and the beatmap attribute has the beatmapset, checksum, and
    max_combo attributes.

    **Attributes**

    id: :class:`int`

    name: :class:`str`

    category: :class:`RoomCategory`

    type: :class:`RoomType`

    realtime_type: :class:`RealTimeType`
        Only applicable when type is RoomType.REALTIME

    user_id: :class:`int`

    starts_at: Optional[:class:`datetime.datetime`]

    ends_at: Optional[:class:`datetime.datetime`]

    max_attempts: :class:`int`

    participant_count: :class:`int`

    channel_id: :class:`int`

    active: :class:`bool`

    has_password: :class:`bool`

    queue_mode: Union[:class:`RealTimeQueueMode`, :class:`PlaylistQueueMode`]
        Type depends on the room type. :class:`PlaylistQueueMode` for type :class:`RoomType`.PLAYLIST
        and :class:`RealTimeQueueMode` otherwise.

    current_playlist_item: Optional[:class:`PlaylistItem`]

    current_user_score: Optional[:class:`UserScoreAggregate`]

    difficulty_range: Optional[Dict[:class:`str`, :class:`int`]]
        When not none, is a dictionary containing keys "max" and "min"

    host: Optional[:class:`UserCompact`]

    playlist: Optional[List[:class:`PlaylistItem`]]

    playlist_item_stats: Optional[:class:`PlaylistItemStats`]

    recent_participants: Optional[List[:class:`UserCompact`]]

    scores: Optional[:class:`MultiplayerScore`]
    """

    __slots__ = (
        "id",
        "name",
        "category",
        "type",
        "user_id",
        "starts_at",
        "ends_at",
        "max_attempts",
        "participant_count",
        "channel_id",
        "active",
        "has_password",
        "queue_mode",
        "current_playlist_item",
        "current_user_score",
        "difficulty_range",
        "host",
        "playlist",
        "playlist_item_stats",
        "recent_participants",
        "scores",
    )

    def __init__(self, data):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.category: RoomCategory = RoomCategory(data["category"])
        self.type: RoomType = RoomType(data["type"])
        self.user_id: int = data["user_id"]
        self.starts_at: datetime = parser.parse(data["starts_at"])
        self.ends_at: Optional[datetime] = get_optional(data, "ends_at", parser.parse)
        self.max_attempts: Optional[int] = data["max_attempts"]
        self.participant_count: int = data["participant_count"]
        self.channel_id: Optional[int] = data["channel_id"]
        self.active: bool = data["active"]
        self.has_password: bool = data["has_password"]
        self.queue_mode: Union[RealTimeQueueMode, PlaylistQueueMode] = (
            RealTimeQueueMode if self.type != RoomType.PLAYLISTS else PlaylistQueueMode
        )(data["queue_mode"])

        self.current_playlist_item: Optional[PlaylistItem] = get_optional(data, "current_playlist_item", PlaylistItem)
        self.current_user_score: Optional[UserScoreAggregate] = get_optional(
            data, "current_user_score", UserScoreAggregate
        )
        self.difficulty_range: Optional[Dict[str, int]] = data.get("difficulty_range")  # {min: int, max: int}
        self.host: Optional[UserCompact] = get_optional(data, "host", UserCompact)
        self.playlist: Optional[List[PlaylistItem]] = get_optional_list(data, "playlist", PlaylistItem)
        self.playlist_item_stats: Optional[PlaylistItemStats] = get_optional(
            data, "playlist_item_stats", PlaylistItemStats
        )
        self.recent_participants: Optional[List[UserCompact]] = get_optional_list(
            data, "recent_participants", UserCompact
        )
        self.scores: Optional[List[MultiplayerScore]] = get_optional_list(data, "scores", MultiplayerScore)

    def __repr__(self):
        return prettify(self, "name", "type")


class UserScoreAggregate:
    """
    **Attributes**

    accuracy: :class:`float`

    attempts: :class:`int`

    completed: :class:`int`

    pp: :class:`float`

    room_id: :class:`int`

    total_score: :class:`int`

    user_id: :class:`int`

    playlist_item_attempts: Optional[Dict[:class:`str`, :class:`int`]]
        contains keys "attempts" and "id".

    position: Optional[:class:`int`]
        user rank

    user: Optional[:class:`UserCompact`]
    """

    __slots__ = (
        "accuracy",
        "attempts",
        "completed",
        "pp",
        "room_id",
        "total_score",
        "user_id",
        "playlist_item_attempts",
        "position",
        "user",
    )

    def __init__(self, data):
        self.accuracy: float = data["accuracy"]
        self.attempts: int = data["attempts"]
        self.completed: int = data["completed"]
        self.pp: float = data["pp"]
        self.room_id: int = data["room_id"]
        self.total_score: int = data["total_score"]
        self.user_id: int = data["user_id"]
        self.playlist_item_attempts: Optional[Dict[str, int]] = data.get(
            "playlist_item_attempts"
        )  # {attempts: int, id: int}
        self.position: Optional[int] = data.get("position")
        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)

    def __repr__(self):
        attributes = ("total_score", "user" if self.user is not None else "user_id")
        return prettify(self, *attributes)


class PlaylistItemStats:
    """
    **Attributes**

    count_active: :class:`int`

    count_total: :class:`int`

    ruleset_ids: List[:class:`GameModeInt`]
    """

    __slots__ = ("count_active", "count_total", "ruleset_ids")

    def __init__(self, data):
        self.count_active: int = data["count_active"]
        self.count_total: int = data["count_total"]
        self.ruleset_ids: List[GameModeInt] = list(map(GameModeInt, data["ruleset_ids"]))

    def __repr__(self):
        return prettify(self, "count_active", "count_total")


class PlaylistItem:
    """
    **Attributes**

    id: :class:`int`

    room_id: :class:`int`

    beatmap_id: :class:`int`

    ruleset_id: :class:`GameModeInt`

    allowed_mods: List[:class:`LazerMod`]

    required_mods: List[:class:`LazerMod`]

    expired: :class:`bool`

    owner_id: :class:`int`

    playlist_order: Optional[:class:`int`]

    played_at: Optional[:class:`datetime.datetime`]

    beatmap: Optional[:class:`BeatmapCompact`]
    """

    __slots__ = (
        "id",
        "room_id",
        "beatmap_id",
        "ruleset_id",
        "allowed_mods",
        "required_mods",
        "expired",
        "owner_id",
        "playlist_order",
        "played_at",
        "beatmap",
    )

    def __init__(self, data):
        self.id: int = data["id"]
        self.room_id: int = data["room_id"]
        self.beatmap_id: int = data["beatmap_id"]
        self.ruleset_id: int = GameModeInt(data["ruleset_id"])
        self.allowed_mods: List[LazerMod] = list(map(LazerMod, data["allowed_mods"]))
        self.required_mods: List[LazerMod] = list(map(LazerMod, data["required_mods"]))
        self.expired: bool = data["expired"]
        self.owner_id: int = data["owner_id"]
        self.playlist_order: Optional[int] = data["playlist_order"]
        self.played_at: Optional[datetime] = get_optional(data, "played_at", parser.parse)
        self.beatmap: Optional[BeatmapCompact] = get_optional(data, "beatmap", BeatmapCompact)

    def __repr__(self):
        attributes = ("id", "beatmap" if self.beatmap is not None else "beatmap_id")
        return prettify(self, *attributes)
