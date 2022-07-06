from .beatmap import BeatmapCompact, BeatmapsetCompact
from .user import UserCompact
from dateutil import parser


class BeatmapScores:
    """
    Contains a list of scores as well as, possibly, a :class:`BeatmapUserScore` object.

    **Attributes**

    scores: :class:`list`
        Contains objects of type :class:`Score`. The list of top scores for the beatmap in descending order.

    user_score: :class:`BeatmapUserScore` or :class:`NoneType`
        The score of the current user. This is not returned if the current user does not have a score.
    """
    __slots__ = (
        "scores", "user_score"
    )

    def __init__(self, data):
        self.scores = [Score(score) for score in data['scores']]
        var_name = 'userScore' if 'userScore' in data else 'user_score'
        self.user_score = BeatmapUserScore(data[var_name]) if data.get(var_name) is not None else None


class Score:
    """
    Contains information about a score

    **Attributes**

    id: :class:`int`

    best_id: :class:`int`

    user_id: :class:`int`

    accuracy: :class:`float`

    mods: :class:`list`

    score: :class:`int`

    max_combo: :class:`int`

    perfect: :class:`bool`

    statistics: :class:`ScoreStatistics`

    passed :class:`bool`

    pp: :class:`float`

    rank: :class:`int`

    created_at: :class:`datetime.datetime`

    mode: :class:`str`

    mode_int: :ref:`GameMode`

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
        "rank_global", "weight", "user", "match"
    )

    def __init__(self, data):
        self.id = data['id']
        self.best_id = data['best_id']
        self.user_id = data['user_id']
        self.accuracy = data['accuracy']
        self.mods = data['mods']
        self.score = data['score']
        self.max_combo = data['max_combo']
        self.perfect = data['perfect']
        self.statistics = ScoreStatistics(data['statistics'])
        self.passed = data['passed']
        self.pp = data['pp']
        self.rank = data['rank']
        self.created_at = parser.parse(data['created_at'])
        self.mode = data['mode']
        self.mode_int = data['mode_int']
        self.replay = data['replay']

        # Optional Attributes
        # Doesn't specify types, so I'll assume Compact
        self.beatmap = BeatmapCompact(data['beatmap']) if 'beatmap' in data else None
        self.beatmapset = BeatmapsetCompact(data['beatmapset']) if 'beatmapset' in data else None
        self.user = UserCompact(data['user']) if 'user' in data else None
        self.match = data['match'] if 'match' in data else None
        self.rank_country = data['rank_country'] if 'rank_country' in data else None
        self.rank_global = data['rank_global'] if 'rank_global' in data else None
        self.weight = data['weight'] if 'weight' in data else None


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


class BeatmapUserScore:
    """
    **Attributes**

    position: :class:`int`
        The position of the score within the requested beatmap ranking.

    score: :class:`Score`
        The details of the score.
    """
    __slots__ = (
        "position", "score"
    )

    def __init__(self, data):
        self.position = data['position']
        self.score = Score(data['score'])
