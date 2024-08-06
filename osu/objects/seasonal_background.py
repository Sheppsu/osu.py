from dateutil import parser
from typing import TYPE_CHECKING, List

from .user import UserCompact
from ..util import prettify, get_required

if TYPE_CHECKING:
    from datetime import datetime


class SeasonalBackgrounds:
    """
    Contains data on the seasonal backgrounds.

    **Attributes**

    ends_at: :class:`datetime.datetime`
        The date when the seasonal backgrounds will end.

    backgrounds: List[:class:`SeasonalBackground`]
        A list of all the seasonal backgrounds.
    """

    __slots__ = ("ends_at", "backgrounds")

    def __init__(self, data):
        self.ends_at: datetime = parser.parse(get_required(data, "ends_at"))
        self.backgrounds: List[SeasonalBackground] = list(map(SeasonalBackground, get_required(data, "backgrounds")))

    def __repr__(self):
        return prettify(self, "ends_at", "backgrounds")


class SeasonalBackground:
    """
    Represents a seasonal background.

    **Attributes**

    url: :class:`str`
        The url of the background.

    user: :class:`UserCompact`
        The artist of the background.
    """

    __slots__ = ("url", "user")

    def __init__(self, data):
        self.url: str = get_required(data, "url")
        self.user: UserCompact = UserCompact(get_required(data, "user"))

    def __repr__(self):
        return prettify(self, "url", "user")
