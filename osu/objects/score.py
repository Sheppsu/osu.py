from .beatmap import BeatmapCompact, BeatmapsetCompact
from .user import UserCompact


class BeatmapScores:
    """
    Contains a list of scores as well as, possibly, a :class:`BeatmapUserScore` object.

    **Attributes**

    scores: :class:`list`
        Contains objects of type :class:`Score`. The list of top scores for the beatmap in descending order.

    **Possible Attributes**

    user_score: :class:`BeatmapUserScore`
        The score of the current user. This is not returned if the current user does not have a score.
    """
    __slots__ = (
        "scores", "user_score"
    )

    def __init__(self, data):
        self.scores = [Score(score) for score in data['scores']]
        if 'userScore' in data:
            self.user_score = BeatmapUserScore(data['userScore'])
        elif 'user_score' in data:  # Is being renamed to this in the future
            self.user_score = BeatmapUserScore(data['user_score'])
        else:
            self.user_score = None


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

    created_at: :ref:`Timestamp`

    mode: :class:`str`

    mode_int: :class:`int`

    replay

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
        "id", "best_id", "user_id", "accuracy", "mods", "score", "max_combo", "perfect", "statistics",
        "pp", "rank", "created_at", "mode", "mode_int", "replay", "beatmap", "beatmapset", "rank_country",
        "rank_global", "weight", "user", "match", "passed"
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
        self.created_at = data['created_at']
        self.mode = data['mode']
        self.mode_int = data['mode_int']
        self.replay = data['replay']

        # Optional Attributes
        self.beatmap = BeatmapCompact(data['beatmap']) if 'beatmap' in data else None
        self.beatmapset = BeatmapsetCompact(data['beatmapset']) if 'beatmapset' in data else None
        self.user = UserCompact(data['user']) if 'user' in data else None  # Doesn't say exactly what type it should be under so I assume UserCompact
        for attribute in ('rank_country', 'rank_global', 'weight', 'match'):
            setattr(self, attribute, data.get(attribute))


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
