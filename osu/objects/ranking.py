from .beatmap import Beatmapset
from .user import UserStatistics


class Rankings:
    """
    **Attributes**

    beatmapsets: :class:`list`
        list containing objects of type :class:`Beatmapset`. The list of beatmaps in the requested spotlight for the given mode; only available if type is charts

    cursor: :class:`dict`
        To be used to query the next page

    ranking: :class:`list`
        list containing objects of type :class:`UserStatistics`. Score details ordered by rank in descending order.

    spotlight: :class:`Spotlight`
        Spotlight details; only available if type is charts

    total: :class:`int`
        An approximate count of ranks available
    """
    __slots__ = (
        "beatmapsets", "cursor", "ranking", "spotlight", "total"
    )

    def __init__(self, data):
        self.cursor = data['cursor']
        self.ranking = [UserStatistics(ranking) for ranking in data['ranking']]
        self.total = data['total']

        self.spotlight = Spotlight(data['spotlight']) if 'spotlight' in data else None
        self.beatmapsets = list(map(Beatmapset, data['beatmapsets'])) if 'beatmapsets' in data else None


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

    name: :class:`str`
        The name of the spotlight.

    start_date: :class:`str`
        In DatTime format. The starting date of the spotlight.

    type: :class:`str`
        The type of spotlight.

    **Possible Attributes**

    participant_count: :class:`int`
        The number of users participating in this spotlight. This is only shown when viewing a single spotlight.
    """
    __slots__ = (
        "end_date", "id", "mode_specific", "name", "start_date", "type", "participant_count"
    )

    def __init__(self, data):
        self.end_date = data['end_date']
        self.id = data['id']
        self.mode_specific = data['mode_specific']
        self.name = data['name']
        self.start_date = data['start_date']
        self.type = data['type']

        self.participant_count = data.get('participant_count', None)


class Spotlights:
    """
    **Attributes**

    spotlights: :class:`list`
        list containing objects of type :class:`Spotlight`
    """
    __slots__ = (
        "spotlights",
    )

    def __init__(self, data):
        self.spotlights = [Spotlight(spotlight) for spotlight in data['spotlights']]
