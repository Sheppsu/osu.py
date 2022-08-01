from .beatmap import Beatmapset
from .user import UserStatistics
from ..util import prettify


class Rankings:
    """
    **Attributes**

    beatmapsets: Sequence[:Beatmapset:] or :class:`NoneType`
        The list of beatmaps in the requested spotlight for the given mode;
        only available if type is charts

    cursor: :class:`dict`
        To be used to query the next page

    ranking: Sequence[:class:`UserStatistics`]
        Score details ordered by rank in descending order.

    spotlight: :class:`Spotlight` or :class:`NoneType`
        Spotlight details; only available if type is charts

    total: :class:`int`
        An approximate count of ranks available
    """
    __slots__ = (
        "beatmapsets", "cursor", "ranking", "spotlight", "total"
    )

    def __init__(self, data):
        self.cursor = data['cursor']
        self.ranking = list(map(UserStatistics, data['ranking']))
        self.total = data['total']
        self.spotlight = Spotlight(data['spotlight']) if data.get('spotlight') is not None else None
        self.beatmapsets = list(map(Beatmapset, data['beatmapsets'])) if data.get('beatmapsets') is not None else None

    def __repr__(self):
        return prettify(self, 'ranking')


class Spotlight:
    """
    The details of a spotlight.

    **Attributes**

    end_date: :class:`str`
        In DateTime format. The end date of the spotlight.

    id: :class:`int`
        The ID of this spotlight.

    mode_specific: :class:`bool`
        If the spotlight has different mades specific to each :ref:`GameMode`.

    participant_count: :class:`int` or :class:`NoneType`
        The number of users participating in this spotlight. This is only shown when viewing a single spotlight.

    name: :class:`str`
        The name of the spotlight.

    start_date: :class:`str`
        In DatTime format. The starting date of the spotlight.

    type: :class:`str`
        The type of spotlight.
    """
    __slots__ = (
        "end_date", "id", "mode_specific", "name", "start_date", "type", "participant_count"
    )

    def __init__(self, data):
        self.end_date = data['end_date']
        self.id = data['id']
        self.mode_specific = data['mode_specific']
        self.participant_count = data['participant_count']
        self.name = data['name']
        self.start_date = data['start_date']
        self.type = data['type']

    def __repr__(self):
        return prettify(self, 'name')


class Spotlights:
    """
    **Attributes**

    spotlights: Sequence[:class:`Spotlight`]
    """
    __slots__ = (
        "spotlights",
    )

    def __init__(self, data):
        self.spotlights = list(map(Spotlight, data['spotlights']))

    def __repr__(self):
        return prettify(self, 'spotlights')
