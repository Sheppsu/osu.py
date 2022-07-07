from dateutil import parser
from ..enums import GameModeStr


class Event:
    """
    The object has different attributes depending on its type. Following are attributes available to all types.

    **Attributes**

    created_at: :class:`datetime.datetime`

    id: :class:`int`

    type:
        All types and the additional attributes they provide are listed under 'Event Types'

    **Event Types**

    :class:`achievement`
        achievement: :class:`Achievement`
        user: :class:`EventUser`

    :class:`beatmapPlaycount`
        beatmap: :class:`EventBeatmap`
        count: :class:`int`

    :class:`beatmapsetApprove`
        approval: :class:`str`
        beatmapset: :class:`EventBeatmapset`
        user: :class:`EventUser`

    :class:`beatmapsetDelete`
        beatmapset: :class:`EventBeatmapset`

    :class:`beatmapsetRevive`
        beatmapset: :class:`EventBeatmapset`
        user: :class:`EventUser`

    :class:`beatmapsetUpdate`
        beatmapset: :class:`EventBeatmapset`
        user: :class:`EventUser`

    :class:`beatmapsetUpload`
        beatmapset: :class:`EventBeatmapset`
        user: :class:`EventUser`

    :class:`rank`
        score_rank: :class:`str`
        rank: :class:`int`
        mode: :class:`GameModeStr`
        beatmap: :class:`EventBeatmap`
        user: :class:`EventUser`

    :class:`rankLost`
        mode: :class:`GameModeStr`
        beatmap: :class:`EventBeatmap`
        user: :class:`EventUser`

    :class:`userSupportAgain`
        user: :class:`EventUser`

    :class:`userSupportFirst`
        user: :class:`EventUser`

    :class:`userSupportGift`
        user: :class:`EventUser`

    :class:`usernameChange`
        user: :class:`EventUser`
    """
    def __init__(self, data):
        self.created_at = parser.parse(data['created_at'])
        self.id = data['id']
        self.type = data['type']

        if self.type == 'achievement':
            self.achievement = data['achievement']
            self.user = EventUser(data['user'])
        elif self.type == 'beatmapPlaycount':
            self.beatmap = EventBeatmap(data['beatmap'])
            self.count = data['count']
        elif self.type == 'beatmapsetApprove':
            self.approval = data['approval']
            self.beatmapset = EventBeatmapset(data['beatmapset'])
            self.user = EventUser(data['user'])
        elif self.type == 'beatmapsetDelete':
            self.beatmapset = EventBeatmapset(data['beatmapset'])
        elif self.type in ("beatmapsetRevive", "beatmapsetUpdate", "beatmapsetUpload"):
            self.beatmapset = EventBeatmapset(data['beatmapset'])
            self.user = EventUser(data['user'])
        elif self.type == 'rank':
            self.score_rank = data['scoreRank']
            self.rank = data['rank']
            self.mode = GameModeStr(data['mode'])
            self.beatmap = EventBeatmap(data['beatmap'])
            self.user = EventUser(data['user'])
        elif self.type == 'rankLost':
            self.mode = GameModeStr(data['mode'])
            self.beatmap = EventBeatmap(data['beatmap'])
            self.user = EventUser(data['user'])
        elif self.type in ("userSupportAgain", "userSupportFirst", "userSupportGift", "usernameChange"):
            self.user = EventUser(data['user'])


class EventUser:
    """
    **Attributes**

    username: :class:`str`

    url: :class:`str`

    previous_username: :class:`str` or :class:`NoneType`
    """
    __slots__ = (
        "username", "url", "previous_username"
    )

    def __init__(self, data):
        self.username = data['username']
        self.url = data['url']
        self.previous_username = data['previousUsername']


class EventBeatmap:
    """
    **Attributes**

    title: :class:`str`

    url: :class:`str`
    """
    __slots__ = (
        "title", "url"
    )

    def __init__(self, data):
        self.title = data['title']
        self.url = data['url']


class EventBeatmapset:
    """
    **Attributes**

    title: :class:`str`

    url: :class:`str`
    """
    __slots__ = (
        "title", "url"
    )

    def __init__(self, data):
        self.title = data['title']
        self.url = data['url']
