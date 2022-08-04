from .score import ScoreStatistics
from ..enums import Mods
from ..util import prettify


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
        Can be one of the following: charts (Spotlight), country (Country), performance (Performance), score (Score)

    total_score: :class:`int`

    accuracy: :class:`int`

    max_combo: :class:`int`

    mods: Sequence[:class:`Mods`]

    statistics: :class:`ScoreStatistics`

    passed: :class:`bool`

    position: :class:`int` or :class:`NoneType`

    scores_around: :class:`MultiplayerScoresAround` or :class:`NoneType`
        Scores around the specified score.

    user: :class:`User`
    """
    __slots__ = (
        "id", "user_id", "room_id", "playlist_item_id", "beatmap_id", "rank",
        "total_score", "accuracy", "max_combo", "mods", "statistics", "passed",
        "position", "scores_around", "user"
    )

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.room_id = data['room_id']
        self.playlist_item_id = data['playlist_item_id']
        self.beatmap_id = data['beatmap_id']
        self.rank = data['rank']
        self.total_score = data['total_score']
        self.accuracy = data['accuracy']
        self.max_combo = data['max_combo']
        self.mods = list(map(Mods.get_from_abbreviation, data['mods']))
        self.statistics = ScoreStatistics(data['statistics'])
        self.passed = data['passed']
        self.position = data['position']
        self.scores_around = MultiplayerScoresAround(data['scores_around']) \
            if data['scores_around'] is not None else None
        self.user = data['user']

    def __repr__(self):
        return prettify(self, 'user', 'position')


class MultiplayerScores:
    """
    An object which contains scores and related data for fetching next page of the result.
    To fetch the next page, make request to scores index (Client.get_scores) with relevant
    room and playlist, use the data in attribute params and cursor to fill in the 3 other optional queries.

    **Attributes**

    cursor: :class:`dict`
        To be used to fetch the next page.

    params: :class:`dict`
        To be used to fetch the next page.

    scores: Sequence[:class:`MultiplayerScore`]

    total: :class:`int` or :class:`NoneType`
        Index only. Total scores of the specified playlist item.

    user_score: :class:`MultiplayerScore` or :class:`NoneType`
        Index only. Score of the accessing user if exists.
    """
    __slots__ = (
        "cursor", "params", "scores", "total", "user_score"
    )

    def __init__(self, data):
        self.cursor = data['cursor']
        self.params = data['params']
        self.scores = list(map(MultiplayerScore, data['scores'])) if data['scores'] is not None else None
        self.total = data['total']
        self.user_score = MultiplayerScore(data['user_score']) if data['user_score'] is not None else None

    def __repr__(self):
        return prettify(self, 'total', 'scores')


class MultiplayerScoresAround:
    """
    **Attributes**

    higher: :class:`MultiplayerScores`

    lower: :class:`MultiplayerScores`
    """
    __slots__ = (
        "higher", "lower"
    )

    def __init__(self, data):
        self.higher = MultiplayerScores(data['higher'])
        self.lower = MultiplayerScores(data['lower'])

    def __repr__(self):
        return prettify(self, 'higher', 'lower')
