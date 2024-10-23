from typing import Dict, Optional, List, TYPE_CHECKING

from .beatmap import Beatmapset
from .user import UserStatistics
from ..util import prettify, get_optional, get_optional_list, get_required, fromisoformat

if TYPE_CHECKING:
    from datetime import datetime


class Rankings:
    """
    **Attributes**

    beatmapsets: Optional[List[:class:`Beatmapset`]]
        The list of beatmaps in the requested spotlight for the given mode;
        only available if type is charts

    cursor: Dict
        To be used to query the next page

    ranking: List[:class:`UserStatistics`]
        Score details ordered by rank in descending order.

    spotlight: Optional[:class:`Spotlight`]
        Spotlight details; only available if type is charts

    total: :class:`int`
        An approximate count of ranks available
    """

    __slots__ = ("beatmapsets", "cursor", "ranking", "spotlight", "total")

    def __init__(self, data):
        self.cursor: Dict = get_required(data, "cursor")
        self.ranking: List[UserStatistics] = list(map(UserStatistics, get_required(data, "ranking")))
        self.total: int = get_required(data, "total")
        self.spotlight: Optional[Spotlight] = get_optional(data, "spotlight", Spotlight)
        self.beatmapsets: Optional[List[Beatmapset]] = get_optional_list(data, "beatmapsets", Beatmapset)

    def __repr__(self):
        return prettify(self, "ranking")


class Spotlight:
    """
    The details of a spotlight.

    **Attributes**

    end_date: :class:`datetime.datetime`
        In DateTime format. The end date of the spotlight.

    id: :class:`int`
        The ID of this spotlight.

    mode_specific: :class:`bool`
        If the spotlight has different modes specific to each game mode.

    participant_count: Optional[:class:`int`]
        The number of users participating in this spotlight. This is only shown when viewing a single spotlight.

    name: :class:`str`
        The name of the spotlight.

    start_date: :class:`datetime.datetime`
        In DatTime format. The starting date of the spotlight.

    type: :class:`str`
        The type of spotlight.
    """

    __slots__ = (
        "end_date",
        "id",
        "mode_specific",
        "name",
        "start_date",
        "type",
        "participant_count",
    )

    def __init__(self, data):
        self.end_date: datetime = fromisoformat(get_required(data, "end_date"))
        self.id: int = get_required(data, "id")
        self.mode_specific: bool = get_required(data, "mode_specific")
        self.participant_count: Optional[int] = data.get("participant_count")
        self.name: str = get_required(data, "name")
        self.start_date: datetime = fromisoformat(get_required(data, "start_date"))
        self.type: str = get_required(data, "type")

    def __repr__(self):
        return prettify(self, "name")


class Spotlights:
    """
    **Attributes**

    spotlights: List[:class:`Spotlight`]
    """

    __slots__ = ("spotlights",)

    def __init__(self, data):
        self.spotlights: List[Spotlight] = list(map(Spotlight, get_required(data, "spotlights")))

    def __repr__(self):
        return prettify(self, "spotlights")
