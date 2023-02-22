from .beatmap import BeatmapCompact, BeatmapsetCompact
from .user import UserCompact
from ..enums import GameModeStr, GameModeInt, Mods, Mod, ObjectType
from ..util import prettify
from dateutil import parser


class BeatmapScores:
    """
    Contains a list of scores as well as, possibly, a :class:`BeatmapUserScore` object.

    **Attributes**

    scores: Sequence[Union[:class:`Score`, :class:`SoloScore`]]
        Contains objects of type :class:`Score`. The list of top scores for the beatmap in descending order.

    user_score: :class:`BeatmapUserScore` or :class:`None`
        The score of the current user. This is not returned if the current user does not have a score.
    """
    __slots__ = (
        "scores", "user_score"
    )

    def __init__(self, data, score_type="legacy"):
        self.scores = list(map(LegacyScore if score_type == "legacy" else SoloScore, data['scores']))
        var_name = 'userScore' if 'userScore' in data else 'user_score'
        self.user_score = BeatmapUserScore(data[var_name]) if data.get(var_name) is not None else None

    def __repr__(self):
        return prettify(self, 'user_score', 'scores')


class Score:
    def __new__(cls, data):
        if data["type"] == "solo_score":
            return SoloScore(data)
        return LegacyScore(data)


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

    rank: :class:`int`

    created_at: :class:`datetime.datetime`

    mode: :class:`GameModeStr`

    mode_int: :ref:`GameModeInt`

    replay: :class:`bool`
        whether or not the replay is available

    **Optional Attributes**

    beatmap: :class:`BeatmapCompact`

    beatmapset: :class:`BeatmapsetCompact`

    rank_country

    rank_global

    weight

    user

    match
    """
    __slots__ = (
        "id", "best_id", "user_id", "accuracy", "mods", "score", "max_combo", "perfect", "statistics", "passed",
        "pp", "rank", "created_at", "mode", "mode_int", "replay", "beatmap", "beatmapset", "rank_country",
        "rank_global", "weight", "user", "match", "type", "current_user_attributes"
    )

    def __init__(self, data):
        self.id = data['id']
        self.best_id = data['best_id']
        self.user_id = data['user_id']
        self.accuracy = data['accuracy']
        self.mods = Mods.parse_any_list(data['mods'])
        self.score = data['score']
        self.max_combo = data['max_combo']
        self.perfect = data['perfect']
        self.statistics = ScoreStatistics(data['statistics'])
        self.passed = data['passed']
        self.pp = data['pp']
        self.rank = data['rank']
        self.created_at = parser.parse(data['created_at'])
        self.mode = GameModeStr(data['mode'])
        self.mode_int = GameModeInt(data['mode_int'])
        self.replay = data['replay']
        self.type = ObjectType(data['type'])

        self.beatmap = BeatmapCompact(data['beatmap']) if 'beatmap' in data else None
        self.beatmapset = BeatmapsetCompact(data['beatmapset']) if 'beatmapset' in data else None
        self.user = UserCompact(data['user']) if 'user' in data else None
        self.match = data['match'] if 'match' in data else None
        self.rank_country = data['rank_country'] if 'rank_country' in data else None
        self.rank_global = data['rank_global'] if 'rank_global' in data else None
        self.weight = data['weight'] if 'weight' in data else None

    def __repr__(self):
        return prettify(self, 'user_id', 'accuracy')


class SoloScore:
    """
    Contains information about a lazer score.

    **Attributes**

    accuracy: :class:`float`

    beatmap_id: :class:`int`

    build_id: :class:`int`

    ended_at: :class:`datetime.datetime`

    legacy_score_id: :class:`int`

    legacy_total_score: :class:`int`

    max_combo: :class:`int`

    maximum_statistics: :class:`ScoreDataStatistics`

    mods: Sequence[:class:`LazerMod`]

    passed: :class:`bool`

    rank: :class:`str`

    ruleset_id: :class:`int`

    started_at: :class:`datetime.datetime`

    statistics: :class:`ScoreDataStatistics`

    total_score: :class:`int`

    user_id: :class:`int`

    best_id: :class:`int`

    id: :class:`int`

    legacy_perfect: :class:`bool`

    pp: :class:`float`

    replay: :class:`bool`

    type: :class:`ObjectType`

    user: :class:`UserCompact`
    """
    __slots__ = (
        "accuracy", "beatmap_id", "build_id", "ended_at", "legacy_score_id",
        "legacy_total_score", "max_combo", "maximum_statistics", "mods",
        "passed", "rank", "ruleset_id", "started_at", "statistics", "total_score",
        "user_id", "best_id", "id", "legacy_perfect", "pp", "replay", "type", "user"
    )

    def __init__(self, data):
        self.accuracy = data["accuracy"]
        self.beatmap_id = data["beatmap_id"]
        self.ended_at = parser.parse(data["ended_at"])
        self.max_combo = data["max_combo"]
        self.maximum_statistics = ScoreDataStatistics(data["maximum_statistics"])
        self.mods = list(map(LazerMod, data["mods"]))
        self.passed = data["passed"]
        self.rank = data["rank"]
        self.ruleset_id = data["ruleset_id"]
        self.statistics = ScoreDataStatistics(data["statistics"])
        self.total_score = data["total_score"]
        self.user_id = data["user_id"]
        self.best_id = data["best_id"]
        self.id = data["id"]
        self.legacy_perfect = data["legacy_perfect"]
        self.pp = data["pp"]
        self.replay = data["replay"]
        self.type = ObjectType(data["type"])
        self.user = UserCompact(data['user'])

        self.build_id = data.get("build_id")
        self.legacy_score_id = data.get("legacy_score_id")
        self.legacy_total_score = data.get("legacy_total_score")
        self.started_at = parser.parse(data["started_at"]) if data.get("started_at") is not None else None

    def __repr__(self):
        return prettify(self, "beatmap_id", "statistics")


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
        "count_50", "count_100", "count_300", "count_geki",
        "count_katu", "count_miss"
    )

    def __init__(self, data):
        self.count_50 = data['count_50']
        self.count_100 = data['count_100']
        self.count_300 = data['count_300']
        self.count_geki = data['count_geki']
        self.count_katu = data['count_katu']
        self.count_miss = data['count_miss']

    def __repr__(self):
        return prettify(self, 'count_300', 'count_miss')


class ScoreDataStatistics:
    """
    **Attributes**

    ok: Union[:class:`int`, :class:`None`]

    meh: Union[:class:`int`, :class:`None`]

    good: Union[:class:`int`, :class:`None`]

    miss: Union[:class:`int`, :class:`None`]

    none: Union[:class:`int`, :class:`None`]

    great: Union[:class:`int`, :class:`None`]

    perfect: Union[:class:`int`, :class:`None`]

    ignore_hit: Union[:class:`int`, :class:`None`]

    ignore_miss: Union[:class:`int`, :class:`None`]

    large_bonus: Union[:class:`int`, :class:`None`]

    small_bonus: Union[:class:`int`, :class:`None`]

    large_tick_hit: Union[:class:`int`, :class:`None`]

    small_tick_hit: Union[:class:`int`, :class:`None`]

    large_tick_miss: Union[:class:`int`, :class:`None`]

    small_tick_miss: Union[:class:`int`, :class:`None`]
    """
    __slots__ = (
        'ok', "meh", 'good', 'miss', 'none', 'great', 'perfect', 'ignore_hit',
        'ignore_miss', 'large_bonus', 'small_bonus', 'large_tick_hit', 'small_tick_hit',
        'large_tick_miss', 'small_tick_miss'
    )

    def __init__(self, data):
        self.ok = data.get('ok')
        self.meh = data.get('meh')
        self.good = data.get('good')
        self.miss = data.get('miss')
        self.none = data.get('none')
        self.great = data.get('great')
        self.perfect = data.get('perfect')
        self.ignore_hit = data.get('ignore_hit')
        self.ignore_miss = data.get('ignore_miss')
        self.large_bonus = data.get('large_bonus')
        self.small_bonus = data.get('small_bonus')
        self.large_tick_hit = data.get('large_tick_hit')
        self.small_tick_hit = data.get('small_tick_hit')
        self.large_tick_miss = data.get('large_tick_miss')
        self.small_tick_miss = data.get('small_tick_miss')

    def __repr__(self):
        return prettify(self, 'perfect', 'miss')


class LazerMod:
    """
    **Attributes**

    mod: :class:`Mods`

    settings: :class:`dict` or :class:`None`
    """
    __slots__ = ("mod", "settings")

    def __init__(self, data):
        self.mod = Mod(data['acronym'])
        self.settings = data.get('settings')

    def __repr__(self):
        return prettify(self, 'mod', 'settings')


class BeatmapUserScore:
    """
    **Attributes**

    position: :class:`int`
        The position of the score within the requested beatmap ranking.

    score: :class:`LegacyScore`
        The details of the score.
    """
    __slots__ = (
        "position", "score"
    )

    def __init__(self, data):
        self.position = data.get('position')
        self.score = LegacyScore(data['score'])

    def __repr__(self):
        return prettify(self, 'position')
