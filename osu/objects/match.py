from dateutil import parser
from typing import Optional, List, TYPE_CHECKING

from ..enums import (
    MatchEventType,
    GameModeStr,
    GameModeInt,
    ScoringType,
    TeamType,
    Mods,
)
from ..util import prettify, get_optional
from .user import UserCompact
from .beatmap import BeatmapCompact
from .score import LegacyScore


if TYPE_CHECKING:
    from datetime import datetime


class Match:
    """
    Info of a match, relevant at :func:`osu.Client.get_matches`.

    **Attributes**

    id: :class:`int`

    name: :class:`str`

    start_time: Optional[:class:`datetime.datetime`]

    end_time: Optional[:class:`datetime.datetime`]
    """

    __slots__ = ("id", "start_time", "end_time", "name")

    def __init__(self, data):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.start_time: Optional[datetime] = get_optional(data, "start_time", parser.parse)
        self.end_time: Optional[datetime] = get_optional(data, "end_time", parser.parse)

    def __repr__(self):
        return prettify(self, "name", "start_time")


class MatchExtended(Match):
    """
    Extended version of :class:`Match` that is relevant at the :func:`osu.Client.get_match` endpoint.

    **Attributes**

    events: List[:class:`MatchEvent`]
        List of events that occurred in the match.

    users: List[:class:`UserCompact`]

    first_event_id: :class:`int`

    latest_event_id: :class:`int`

    current_game_id: :class:`int`
    """

    __slots__ = (
        "events",
        "users",
        "first_event_id",
        "latest_event_id",
        "current_game_id",
    )

    def __init__(self, data):
        super().__init__(data["match"])
        self.events: List[MatchEvent] = list(map(MatchEvent, data["events"]))
        self.users: List[UserCompact] = list(map(UserCompact, data["users"]))
        self.first_event_id: int = data["first_event_id"]
        self.latest_event_id: int = data["latest_event_id"]
        self.current_game_id: int = data["current_game_id"]


class MatchEvent:
    """
    An event that occurred in a match.

    **Attributes**

    id: :class:`int`

    timestamp: :class:`datetime.datetime`

    user_id: :class:`int`

    type: :class:`MatchEventType`

    text: Optional[:class:`str`]
        None unless the event type is :class:`MatchEventType`.OTHER

    game: Optional[:class:`MatchGame`]
        None unless the event type is :class:`MatchEventType`.OTHER
    """

    __slots__ = ("id", "timestamp", "user_id", "type", "text", "game")

    def __init__(self, data):
        self.id: int = data["id"]
        self.timestamp: datetime = parser.parse(data["timestamp"])
        self.user_id: int = data["user_id"]
        self.type: MatchEventType = MatchEventType(data["detail"]["type"])
        self.text: Optional[str] = data["detail"]["text"] if "text" in data["detail"] else None
        self.game: Optional[MatchGame] = get_optional(data, "game", MatchGame)

    def __repr__(self):
        attributes = ("type",) if self.type != MatchEventType.OTHER else ("type", "game")
        return prettify(self, *attributes)


class MatchGame:
    """
    Represents a map played in a match and contains all the info about the game

    **Attributes**

    beatmap_id: :class:`int`

    id: :class:`int`

    start_time: Optional[:class:`datetime.datetime`]

    end_time: Optional[:class:`datetime.datetime`]

    mode: :class:`GameModeStr`

    mode_int: :class:`GameModeInt`

    scoring_type: :class:`ScoringType`

    team_type: :class:`TeamType`

    mods: :class:`Mods`

    beatmap: Optional[:class:`BeatmapCompact`]

    scores: List[:class:`LegacyScore`]
    """

    __slots__ = (
        "beatmap_id",
        "id",
        "start_time",
        "end_time",
        "mode",
        "mode_int",
        "scoring_type",
        "team_type",
        "mods",
        "beatmap",
        "scores",
    )

    def __init__(self, data):
        self.beatmap_id: int = data["beatmap_id"]
        self.id: int = data["id"]
        self.start_time: datetime = parser.parse(data["start_time"])
        self.end_time: Optional[datetime] = get_optional(data, "end_time", parser.parse)
        self.mode: GameModeStr = GameModeStr(data["mode"])
        self.mode_int: GameModeInt = GameModeInt(data["mode_int"])
        self.scoring_type: ScoringType = ScoringType(data["scoring_type"])
        self.team_type: TeamType = TeamType(data["team_type"])
        self.mods: Mods = Mods.parse_any_list(data["mods"])
        self.beatmap: Optional[BeatmapCompact] = get_optional(data, "beatmap", BeatmapCompact)
        self.scores: List[LegacyScore] = list(map(LegacyScore, data["scores"]))

    def __repr__(self):
        return prettify(self, "beatmap", "scores")


class MatchGameScoreInfo:
    """
    Says info about a score set in a match. Is an attribute of :class:`LegacyScore`

    **Attributes**

    slot: :class:`int`

    team: :class:`str`

    passed: :class:`bool`
    """

    __slots__ = ("slot", "team", "passed")

    def __init__(self, data):
        self.slot: int = data["slot"]
        self.team: str = data["team"]
        self.passed: bool = data["pass"]

    def __repr__(self):
        return prettify(self, "slot", "team")
