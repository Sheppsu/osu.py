from typing import Optional, List, TYPE_CHECKING, Union, Dict

from .beatmap import BeatmapCompact, BeatmapsetCompact, Beatmap
from .user import UserCompact
from .current_user_attributes import ScoreUserAttributes
from ..enums import GameModeStr, GameModeInt, Mods, Mod, ObjectType, ScoreRank
from ..util import prettify, get_optional, get_required, fromisoformat

if TYPE_CHECKING:
    from datetime import datetime


class BeatmapScores:
    """
    Contains a list of scores as well as, possibly, a :class:`BeatmapUserScore` object.

    **Attributes**

    scores: List[Union[:class:`LegacyScore`, :class:`SoloScore`]]
        The list of top scores for the beatmap in descending order.

    user_score: Optional[:class:`BeatmapUserScore`]
        The score of the current user. This is not returned if the current user does not have a score.
    """

    __slots__ = ("scores", "user_score")

    def __init__(self, data):
        self.scores: List[Union[LegacyScore, SoloScore]] = list(map(get_score_object, get_required(data, "scores")))
        var_name = "userScore" if "userScore" in data else "user_score"
        self.user_score: Optional[BeatmapUserScore] = get_optional(data, var_name, BeatmapUserScore)

    def __repr__(self):
        return prettify(self, "user_score", "scores")

    def __len__(self):
        return len(self.scores)

    def __iter__(self):
        return iter(self.scores)


class LegacyScore:
    """
    Contains information about a score

    **Attributes**

    id: :class:`int`

    best_id: :class:`int`

    user_id: :class:`int`

    accuracy: :class:`float`

    mods: :class:`Mods`

    score: :class:`int`

    max_combo: :class:`int`

    perfect: :class:`bool`

    statistics: :class:`ScoreStatistics`

    passed :class:`bool`

    pp: :class:`float`

    rank: :class:`ScoreRank`

    created_at: :class:`datetime.datetime`

    mode: :class:`GameModeStr`

    mode_int: :class:`GameModeInt`

    has_replay: :class:`bool`
        is the replay is available

    beatmap: Optional[:class:`BeatmapCompact`]

    beatmapset: Optional[:class:`BeatmapsetCompact`]

    rank_country: Optional[:class:`int`]

    rank_global: Optional[:class:`int`]

    weight: Optional[:class:`PpWeight`]

    user: Optional[:class:`UserCompact`]

    match: Optional[:class:`MatchGameScoreInfo`]

    current_user_attributes: Optional[:class:`ScoreUserAttributes`]
    """

    __slots__ = (
        "id",
        "best_id",
        "user_id",
        "accuracy",
        "mods",
        "score",
        "max_combo",
        "perfect",
        "statistics",
        "passed",
        "pp",
        "rank",
        "created_at",
        "mode",
        "mode_int",
        "has_replay",
        "beatmap",
        "beatmapset",
        "rank_country",
        "rank_global",
        "weight",
        "user",
        "match",
        "type",
        "current_user_attributes",
    )

    def __init__(self, data):
        self.id: int = get_required(data, "id")
        self.best_id: int = get_required(data, "best_id")
        self.user_id: int = get_required(data, "user_id")
        self.accuracy: float = get_required(data, "accuracy")
        self.mods: Mods = Mods.parse_any_list(get_required(data, "mods"))
        self.score: int = get_required(data, "score")
        self.max_combo: int = get_required(data, "max_combo")
        self.perfect: bool = get_required(data, "perfect")
        self.statistics: ScoreStatistics = ScoreStatistics(get_required(data, "statistics"))
        self.passed: bool = get_required(data, "passed")
        self.pp: float = get_required(data, "pp")
        self.rank: ScoreRank = ScoreRank(get_required(data, "rank"))
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.mode: GameModeStr = GameModeStr(get_required(data, "mode"))
        self.mode_int: GameModeInt = GameModeInt(get_required(data, "mode_int"))
        self.has_replay: bool = get_required(data, "replay")
        self.type: ObjectType = ObjectType(get_required(data, "type"))

        from .match import MatchGameScoreInfo

        self.beatmap: Optional[BeatmapCompact] = get_optional(data, "beatmap", BeatmapCompact)
        self.beatmapset: Optional[BeatmapsetCompact] = get_optional(data, "beatmapset", BeatmapsetCompact)
        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)
        self.match: Optional[MatchGameScoreInfo] = get_optional(data, "match", MatchGameScoreInfo)
        self.rank_country: Optional[int] = data.get("rank_country")
        self.rank_global: Optional[int] = data.get("rank_global")
        self.weight: Optional[PpWeight] = get_optional(data, "weight", PpWeight)
        self.current_user_attributes: Optional[ScoreUserAttributes] = get_optional(
            data, "current_user_attributes", ScoreUserAttributes
        )

    # backwards compatibility
    @property
    def replay(self):
        return self.has_replay

    def __repr__(self):
        return prettify(self, "user_id", "accuracy")


class SoloScore:
    """
    Contains information about a lazer score.

    **Attributes**

    accuracy: :class:`float`

    beatmap_id: Optional[:class:`int`]

    beatmap: Optional[:class:`Beatmap`]

    beatmapset: Optional[:class:`BeatmapsetCompact`]

    ended_at: :class:`datetime.datetime`

    max_combo: :class:`int`

    maximum_statistics: :class:`ScoreDataStatistics`

    mods: List[:class:`LazerMod`]

    passed: :class:`bool`

    rank: :class:`ScoreRank`

    ruleset_id: :class:`int`

    statistics: :class:`ScoreDataStatistics`

    total_score: :class:`int`

    user_id: :class:`int`

    best_id: Optional[:class:`int`]

    id: :class:`int`

    legacy_perfect: Optional[:class:`bool`]

    pp: Optional[:class:`float`]

    replay: :class:`bool`

    type: :class:`ObjectType`

    user: Optional[:class:`UserCompact`]

    build_id: Optional[:class:`int`]

    legacy_score_id: Optional[:class:`int`]

    legacy_total_score: Optional[:class:`int`]

    started_at: Optional[:class:`datetime.datetime`]

    current_user_attributes: Optional[:class:`ScoreUserAttributes`]

    weight: Optional[:class:`PpWeight`]
    """

    __slots__ = (
        "accuracy",
        "beatmap_id",
        "build_id",
        "ended_at",
        "legacy_score_id",
        "legacy_total_score",
        "max_combo",
        "maximum_statistics",
        "mods",
        "passed",
        "rank",
        "ruleset_id",
        "started_at",
        "statistics",
        "total_score",
        "user_id",
        "best_id",
        "id",
        "legacy_perfect",
        "pp",
        "replay",
        "type",
        "user",
        "current_user_attributes",
        "weight",
        "beatmap",
        "beatmapset",
    )

    def __init__(self, data):
        self.accuracy: float = get_required(data, "accuracy")
        self.beatmap_id: int = get_required(data, "beatmap_id")
        self.ended_at: datetime = fromisoformat(get_required(data, "ended_at"))
        self.max_combo: int = get_required(data, "max_combo")
        self.maximum_statistics: ScoreDataStatistics = ScoreDataStatistics(get_required(data, "maximum_statistics"))
        self.mods: List[LazerMod] = list(map(LazerMod, get_required(data, "mods")))
        self.passed: bool = get_required(data, "passed")
        self.rank: ScoreRank = ScoreRank(get_required(data, "rank"))
        self.ruleset_id: int = get_required(data, "ruleset_id")
        self.statistics: ScoreDataStatistics = ScoreDataStatistics(get_required(data, "statistics"))
        self.total_score: int = get_required(data, "total_score")
        self.user_id: int = get_required(data, "user_id")
        self.best_id: Optional[int] = get_required(data, "best_id")
        self.id: int = get_required(data, "id")
        self.legacy_perfect: Optional[bool] = get_required(data, "legacy_perfect")
        self.pp: Optional[float] = get_required(data, "pp")
        self.replay: bool = get_required(data, "replay")
        self.type: ObjectType = ObjectType(get_required(data, "type"))

        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)
        self.build_id: Optional[int] = data.get("build_id")
        self.legacy_score_id: Optional[int] = data.get("legacy_score_id")
        self.legacy_total_score: Optional[int] = data.get("legacy_total_score")
        self.started_at: Optional[datetime] = get_optional(data, "started_at", fromisoformat)
        self.current_user_attributes: Optional[ScoreUserAttributes] = get_optional(
            data, "current_user_attributes", ScoreUserAttributes
        )
        self.weight: Optional[PpWeight] = get_optional(data, "weight", PpWeight)
        self.beatmap: Optional[Beatmap] = get_optional(data, "beatmap", Beatmap)
        self.beatmapset: Optional[BeatmapsetCompact] = get_optional(data, "beatmapset", BeatmapsetCompact)

    def __repr__(self):
        return prettify(self, "beatmap_id", "statistics")


class PpWeight:
    """
    Weighted pp info

    **Attributes**

    percentage: :class:`int`
        number (0-100) that tells percentage weighed

    pp: :class:`float`
        amount of pp after being weighted
    """

    __slots__ = ("percentage", "pp")

    def __init__(self, data):
        self.percentage: float = get_required(data, "percentage")
        self.pp: float = get_required(data, "pp")


def get_score_object(data) -> Union[SoloScore, LegacyScore]:
    if data["type"] == "solo_score":
        return SoloScore(data)

    return LegacyScore(data)


class ScoreStatistics:
    """
    **Attributes**

    count_50: :class:`int`

    count_100: :class:`int`

    count_300: :class:`int`

    count_geki: :class:`int`

    count_katu: :class:`int`

    count_miss: :class:`int`
    """

    __slots__ = (
        "count_50",
        "count_100",
        "count_300",
        "count_geki",
        "count_katu",
        "count_miss",
    )

    def __init__(self, data):
        self.count_50: int = get_required(data, "count_50")
        self.count_100: int = get_required(data, "count_100")
        self.count_300: int = get_required(data, "count_300")
        self.count_geki: int = get_required(data, "count_geki")
        self.count_katu: int = get_required(data, "count_katu")
        self.count_miss: int = get_required(data, "count_miss")

    def __repr__(self):
        return prettify(self, "count_300", "count_miss")


class ScoreDataStatistics:
    """
    **Attributes**

    ok: Optional[:class:`int`]

    meh: Optional[:class:`int`]

    good: Optional[:class:`int`]

    miss: Optional[:class:`int`]

    none: Optional[:class:`int`]

    great: Optional[:class:`int`]

    perfect: Optional[:class:`int`]

    ignore_hit: Optional[:class:`int`]

    ignore_miss: Optional[:class:`int`]

    large_bonus: Optional[:class:`int`]

    small_bonus: Optional[:class:`int`]

    large_tick_hit: Optional[:class:`int`]

    small_tick_hit: Optional[:class:`int`]

    large_tick_miss: Optional[:class:`int`]

    small_tick_miss: Optional[:class:`int`]
    """

    __slots__ = (
        "ok",
        "meh",
        "good",
        "miss",
        "none",
        "great",
        "perfect",
        "ignore_hit",
        "ignore_miss",
        "large_bonus",
        "small_bonus",
        "large_tick_hit",
        "small_tick_hit",
        "large_tick_miss",
        "small_tick_miss",
    )

    def __init__(self, data):
        self.ok: Optional[int] = data.get("ok")
        self.meh: Optional[int] = data.get("meh")
        self.good: Optional[int] = data.get("good")
        self.miss: Optional[int] = data.get("miss")
        self.none: Optional[int] = data.get("none")
        self.great: Optional[int] = data.get("great")
        self.perfect: Optional[int] = data.get("perfect")
        self.ignore_hit: Optional[int] = data.get("ignore_hit")
        self.ignore_miss: Optional[int] = data.get("ignore_miss")
        self.large_bonus: Optional[int] = data.get("large_bonus")
        self.small_bonus: Optional[int] = data.get("small_bonus")
        self.large_tick_hit: Optional[int] = data.get("large_tick_hit")
        self.small_tick_hit: Optional[int] = data.get("small_tick_hit")
        self.large_tick_miss: Optional[int] = data.get("large_tick_miss")
        self.small_tick_miss: Optional[int] = data.get("small_tick_miss")

    def __repr__(self):
        attrs = tuple(filter(lambda attr: getattr(self, attr) is not None, self.__slots__))
        return prettify(self, *attrs[:2])


class LazerMod:
    """
    **Attributes**

    mod: Union[:class:`Mod`]

    settings: Optional[Dict]
    """

    __slots__ = ("mod", "settings")

    def __init__(self, data):
        self.mod: Union[Mod] = Mod(get_required(data, "acronym"))
        self.settings: Optional[Dict] = data.get("settings")

    def __repr__(self):
        return prettify(self, "mod", "settings")


class BeatmapUserScore:
    """
    **Attributes**

    position: :class:`int`
        The position of the score within the requested beatmap ranking.

    score: :class:`LegacyScore`
        The details of the score.
    """

    __slots__ = ("position", "score")

    def __init__(self, data):
        self.position: int = get_required(data, "position")
        self.score: Union[LegacyScore, SoloScore] = get_score_object(get_required(data, "score"))

    def __repr__(self):
        return prettify(self, "position")
