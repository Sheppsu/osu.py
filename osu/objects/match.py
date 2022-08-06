from dateutil import parser
from .user import UserCompact
from ..enums import MatchEventType
from ..util import prettify


class Match:
    __slots__ = ("id", "start_time", "end_time", "name")

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.start_time = parser.parse(data['start_time']) if data['start_time'] is not None else None
        self.end_time = parser.parse(data['end_time']) if data['end_time'] is not None else None

    def __repr__(self):
        return prettify(self, 'name', 'start_time')


class MatchExtended(Match):
    """
    Extended version of :class:`Match` that is relevant at the :func:`osu.Client.get_match` endpoint.

    **Attributes**

    events: Sequence[:class:`MatchEvent`]
        List of events that occurred in the match.

    users: Sequence[:class:`UserCompact`]

    first_event_id: :class:`int`

    latest_event_id: :class:`int`

    current_game_id: :class:`int`
    """
    __slots__ = Match.__slots__ + (
        "events", "users", "first_event_id", "latest_event_id", "current_game_id"
    )

    def __init__(self, data):
        super().__init__(data["match"])
        self.events = list(map(MatchEvent, data['events']))
        self.users = list(map(UserCompact, data['users']))
        self.first_event_id = data['first_event_id']
        self.latest_event_id = data['latest_event_id']
        self.current_game_id = data['current_game_id']


class MatchEvent:
    """
    An event that occurred in a match.

    **Attributes**

    id: :class:`int`

    timestamp: :class:`datetime.datetime`

    user_id: :class:`int`

    type: :class:`MatchEventType`

    text: Union[:class:`str`, :class:`NoneType`]
        None unless the event type is :class:`MatchEventType`.OTHER
    """
    __slots__ = ("id", "timestamp", "user_id", "type", "text")

    def __init__(self, data):
        self.id = data['id']
        self.timestamp = parser.parse(data['timestamp'])
        self.user_id = data['user_id']
        self.type = MatchEventType(data['detail']['type'])
        self.text = data['detail']['text'] if 'text' in data['detail'] else None

    def __repr__(self):
        attributes = ('type',) if self.type != MatchEventType.OTHER else ('type', 'text')
        return prettify(self, *attributes)
