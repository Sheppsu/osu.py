from .score import ScoreStatistics
from .user import UserCompact
from .beatmap import BeatmapCompact
from ..enums import Mod, RoomCategory, RoomType, RealTimeQueueMode, PlaylistQueueMode, GameModeInt
from ..util import prettify
from dateutil import parser


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

    mods: Sequence[:class:`Mod`]

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
        self.mods = list(map(Mod, data['mods']))
        self.statistics = ScoreStatistics(data['statistics'])
        self.passed = data['passed']
        self.position = data.get('position')
        self.scores_around = MultiplayerScoresAround(data['scores_around']) \
            if data.get('scores_around') is not None else None
        self.user = UserCompact(data['user']) if data.get('user') is not None else None

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


class Room:
    """
    :func:`osu.Client.get_rooms` endpoint includes host, playlist, and recent_participants attributes.
    In addition, the :class:`PlaylistItem` objects in playlist include the beatmap attribute and the
    beatmap attribute has the beatmapset, checksum, and max_combo attributes.

    **Attributes**

    id: :class:`int`

    name: :class:`str`

    category: :class:`RoomCategory`

    type: :class:`RoomType`

    user_id: :class:`int`

    start_at: Union[:class:`datetime.datetime`, :class:`NoneType`]

    ends_at: Union[:class:`datetime.datetime`, :class:`NoneType`]

    max_attempts: :class:`int`

    participant_count: :class:`int`

    channel_id: :class:`int`

    active: :class:`bool`

    has_password: :class:`bool`

    queue_mode: Union[:class:`RealTimeQueueMode`, :class:`PlaylistQueueMode`]
        type depends on the room type. :class:`RealTimeQueueMode` for type :class:`RoomType`.REALTIME and
        :class:`PlaylistQueueMode` for type :class:`RoomType`.PLAYLIST.

    current_playlist_item: Union[:class:`PlaylistItem`, :class:`NoneType`]

    current_user_score: Union[:class:`UserScoreAggregate`, :class:`NoneType`]

    difficulty_range: Union[Dict[:class:`str`, :class:`int`], :class:`NoneType`]
        When not none, is a dictionary containing keys "max" and "min."

    host: Union[:class:`UserCompact`, :class:`NoneType`]

    playlist: Union[Sequence[:class:`PlaylistItem`], :class:`NoneType`]

    playlist_item_stats: Union[:class:`PlaylistItemStats`, :class:`NoneType`]

    recent_participants: Union[Sequence[:class:`UserCompact`], :class:`NoneType`]

    scores: Union[:class:`MultiplayerScore`, :class:`NoneType`]
    """
    __slots__ = (
        "id", "name", "category", "type", "user_id", "start_at", "ends_at", "max_attempts",
        "participant_count", "channel_id", "active", "has_password", "queue_mode",
        "current_playlist_item", "current_user_score", "difficulty_range", "host",
        "playlist", "playlist_item_stats", "recent_participants", "scores"
    )

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.category = RoomCategory(data['category'])
        self.type = RoomType(data['type'])
        self.user_id = data['user_id']
        self.start_at = parser.parse(data['start_at']) if data.get('start_at') is not None else None
        self.ends_at = parser.parse(data['ends_at']) if data.get('ends_at') is not None else None
        self.max_attempts = data['max_attempts']
        self.participant_count = data['participant_count']
        self.channel_id = data['channel_id']
        self.active = data['active']
        self.has_password = data['has_password']
        self.queue_mode = (PlaylistQueueMode if self.type == RoomType.PLAYLISTS
                           else RealTimeQueueMode)(data['queue_mode'])

        self.current_playlist_item = PlaylistItem(data['current_playlist_item']) \
            if data.get('current_playlist_item') is not None else None
        self.current_user_score = UserScoreAggregate(data['current_user_score']) \
            if data.get('current_user_score') is not None else None
        self.difficulty_range = data.get('difficulty_range')  # {min, max}
        self.host = UserCompact(data['host']) if data.get('host') is not None else None
        self.playlist = list(map(PlaylistItem, data['playlist'])) if data.get('playlist') is not None else None
        self.playlist_item_stats = PlaylistItemStats(data['playlist_item_stats']) \
            if data.get('playlist_item_stats') is not None else None
        self.recent_participants = list(map(UserCompact, data['recent_participants'])) \
            if data.get('recent_participants') is not None else None
        self.scores = list(map(MultiplayerScore, data['scores'])) if data.get('scores') is not None else None

    def __repr__(self):
        return prettify(self, 'name', 'type')


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

    playlist_item_attempts: Union[Dict[:class:`str`, :class:`int`], :class:`NoneType`]
        contains keys "attempts" and "id."

    position: Union[:class:`int`, :class:`NoneType`]
        user rank

    user: Union[:class:`UserCompact`, :class:`NoneType`]
    """
    __slots__ = (
        "accuracy", "attempts", "completed", "pp", "room_id", "total_score",
        "user_id", "playlist_item_attempts", "position", "user"
    )

    def __init__(self, data):
        self.accuracy = data['accuracy']
        self.attempts = data['attempts']
        self.completed = data['completed']
        self.pp = data['pp']
        self.room_id = data['room_id']
        self.total_score = data['total_score']
        self.user_id = data['user_id']
        self.playlist_item_attempts = data.get('playlist_item_attempts')  # {attempts, id}
        self.position = data.get('position')
        self.user = UserCompact(data['user']) if data.get('user') is not None else None

    def __repr__(self):
        attributes = ('total_score', 'user' if self.user is not None else 'user_id')
        return prettify(self, *attributes)


class PlaylistItemStats:
    """
    **Attributes**

    count_active: :class:`int`

    count_total: :class:`int`

    ruleset_ids: :class:`Sequence[:class:`GameModeInt`]
    """
    __slots__ = ("count_active", "count_total", "ruleset_ids")

    def __init__(self, data):
        self.count_active = data['count_active']
        self.count_total = data['count_total']
        self.ruleset_ids = list(map(GameModeInt, data['ruleset_ids']))

    def __repr__(self):
        return prettify(self, 'count_active', 'count_total')


class PlaylistItem:
    """
    **Attributes**

    id: :class:`int`

    room_id: :class:`int`

    beatmap_id: :class:`int`

    ruleset_id: :class:`GameModeInt`

    allowed_mods: Sequence[:class:`PlaylistMod`]

    required_mods: Sequence[:class:`PlaylistMod`]

    expired: :class:`bool`

    owner_id: :class:`int`

    playlist_order: Union[:class:`int`, :class:`NoneType`]

    played_at: Union[:class:`datetime.datetime`, :class:`NoneType`]

    beatmap: Union[:class:`BeatmapCompact`, :class:`NoneType`]
    """
    __slots__ = (
        "id", "room_id", "beatmap_id", "ruleset_id", "allowed_mods", "required_mods",
        "expired", "owner_id", "playlist_order", "played_at", "beatmap"
    )

    def __init__(self, data):
        self.id = data['id']
        self.room_id = data['room_id']
        self.beatmap_id = data['beatmap_id']
        self.ruleset_id = GameModeInt(data['ruleset_id'])
        self.allowed_mods = list(map(PlaylistMod, data['allowed_mods']))
        self.required_mods = list(map(PlaylistMod, data['required_mods']))
        self.expired = data['expired']
        self.owner_id = data['owner_id']
        self.playlist_order = data['playlist_order']
        self.played_at = parser.parse(data['played_at']) if data['played_at'] is not None else None
        self.beatmap = BeatmapCompact(data['beatmap']) if data.get('beatmap') is not None else None

    def __repr__(self):
        attributes = ('id', 'beatmap' if self.beatmap is not None else 'beatmap_id')
        return prettify(self, *attributes)


class PlaylistMod:
    """
    **Attributes**

    mod: :class:`Mods`

    settings: :class:`dict`
    """
    __slots__ = ("mod", "settings")

    def __init__(self, data):
        self.mod = Mod(data['acronym'])
        self.settings = data['settings']

    def __repr__(self):
        return prettify(self, 'mod', 'settings')
