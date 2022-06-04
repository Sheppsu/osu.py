from .score import ScoreStatistics


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

    mods: :class:`list`
        list containing objects of type :class:`str`

    statistics: :class:`ScoreStatistics`

    passed: :class:`bool`

    position: :class:`int`

    scores_around: :class:`MultiplayerScoresAround`
        Scores around the specified score.

    user: :class:`User`
    """
    __slots__ = (
        "id", "user_id", "room_id", "playlist_item_id", "beatmap_id", "rank",
        "total_score", "accuracy", "max_combo", "mods", "statistics", "passed",
        "position", "scores_around"
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
        self.mods = data['mods']
        self.statistics = ScoreStatistics(data['statistics'])
        self.passed = data['passed']
        self.position = data['position']
        self.scores_around = MultiplayerScoresAround(data['scores_around'])


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

    scores: :class:`list`
        list containing objects of type :class:`MultiplayerScore`

    total: :class:`int`
        Index only. Total scores of the specified playlist item.

    user_score: :class:`MultiplayerScore`
        Index only. Score of the accessing user if exists.
    """
    __slots__ = (
        "cursor", "params", "scores", "total", "user_score"
    )

    def __init__(self, data):
        self.cursor = data['cursor']
        self.params = data['params']
        self.scores = [MultiplayerScore(score) for score in data['scores']]

        self.total = data['total'] if 'total' in data else None
        self.user_score = MultiplayerScore(data['user_score']) if 'user_score' in data else None


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
