from typing import Dict, Optional, List, TYPE_CHECKING, Generic, TypeVar, Type

from .beatmap import Beatmapset
from .user import UserStatistics, Country
from ..util import prettify, get_required, fromisoformat

if TYPE_CHECKING:
    from datetime import datetime


__all__ = ("Rankings", "Spotlight", "Spotlights", "SpotlightRankings", "CountryStatistics")


_RankingT = TypeVar("_RankingT")


class Rankings(Generic[_RankingT]):
    """
    A generic ranking object with statistic type being denoted by `_RankingT`

    **Attributes**

    cursor: Dict
        To be used to query the next page

    ranking: List[_RankingT]
        Statistics ordered by rank in descending order.
        Type depends on `_RankingT` (determined during construction)

    total: int
        An approximate count of ranks available
    """

    __slots__ = ("cursor", "ranking", "total")

    def __init__(self, data, ranking_cls: Type[_RankingT]):
        self.cursor: Dict = get_required(data, "cursor")
        self.ranking: List[_RankingT] = list(map(ranking_cls, get_required(data, "ranking")))
        self.total: int = get_required(data, "total")

    def __repr__(self):
        return prettify(self, "ranking")


class SpotlightRankings:
    """
    **Attributes**

    beatmapsets: List[:class:`Beatmapset`]

    ranking: List[:class:`UserStatistics`]

    spotlight: :class:`Spotlight`
    """

    __slots__ = ("beatmapsets", "ranking", "spotlight")

    def __init__(self, data):
        self.beatmapsets: List[Beatmapset] = list(map(Beatmapset, get_required(data, "beatmapsets")))
        self.ranking: List[UserStatistics] = list(map(UserStatistics, get_required(data, "ranking")))
        self.spotlight: Spotlight = Spotlight(get_required(data, "spotlight"))

    def __repr__(self):
        return prettify(self, "ranking")


class Spotlight:
    """
    The details of a spotlight.

    **Attributes**

    end_date: :py:class:`datetime.datetime`
        In DateTime format. The end date of the spotlight.

    id: int
        The ID of this spotlight.

    mode_specific: bool
        If the spotlight has different modes specific to each game mode.

    participant_count: Optional[int]
        The number of users participating in this spotlight. This is only shown when viewing a single spotlight.

    name: str
        The name of the spotlight.

    start_date: :py:class:`datetime.datetime`
        In DatTime format. The starting date of the spotlight.

    type: str
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


class CountryStatistics:
    """
    **Attributes**

    code: str

    active_users: int

    play_count: int

    ranked_score: int

    performance: int

    country: :class:`Country`
    """

    __slots__ = ("code", "active_users", "play_count", "ranked_score", "performance", "country")

    def __init__(self, data):
        self.code: str = get_required(data, "code")
        self.active_users: int = get_required(data, "active_users")
        self.play_count: int = get_required(data, "play_count")
        self.ranked_score: int = get_required(data, "ranked_score")
        self.performance: int = get_required(data, "performance")
        self.country: Country = Country(get_required(data, "country"))

    def __repr__(self):
        return prettify(self, "code", "performance")
