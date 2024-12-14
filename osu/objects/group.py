from typing import Optional, List

from ..util import prettify, get_optional, get_optional_list, get_required
from ..enums import GameModeStr
from .forum import TextFormat


__all__ = ("Group", "UserGroup")


class Group:
    """
    This object isn't returned by any endpoints yet, it is here purely as a reference for :class:`UserGroup`

    **Attributes**

    id: int

    identifier: str
        Unique string to identify the group.

    is_probationary: bool
        Whether members of this group are considered probationary.

    has_playmodes: bool
        If this group associates GameModes with a user's membership, e.g. BN/NAT members

    has_listing: bool
        Whether this group displays a listing at /groups/{id}

    name: str

    short_name: str
        Short name of the group for display.

    colour: Optional[str]

    description: Optional[:class:`TextFormat`]
        A dictionary with keys html and markdown.
    """

    __slots__ = (
        "id",
        "identifier",
        "is_probationary",
        "has_playmodes",
        "has_listing",
        "name",
        "short_name",
        "colour",
        "description",
    )

    def __init__(self, data):
        self.id: int = get_required(data, "id")
        self.identifier: str = get_required(data, "identifier")
        self.is_probationary: bool = get_required(data, "is_probationary")
        self.has_playmodes: bool = get_required(data, "has_playmodes")
        self.name: str = get_required(data, "name")
        self.short_name: str = get_required(data, "short_name")
        self.colour: Optional[str] = get_required(data, "colour")
        self.description: Optional[TextFormat] = get_optional(data, "description", TextFormat)

    def __repr__(self):
        return prettify(self, "name")


class UserGroup(Group):
    """
    Describes the :class:`Group` membership of a :class:`User`.
    It contains all of the attributes of the :class:`Group`, in addition to what is listed here.

    **Attributes**

    playmodes: Optional[List[:class:`GameModeStr`]]
        GameModes associated with this membership (None if `has_playmodes` is false).
    """

    __slots__ = ("playmodes",)

    def __init__(self, data):
        super().__init__(data)
        self.playmodes: Optional[List[GameModeStr]] = get_optional_list(data, "playmodes", GameModeStr)

    def __repr__(self):
        return super().__repr__()
