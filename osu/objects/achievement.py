from typing import Optional

from ..util import prettify, get_optional, get_required
from ..enums import GameModeStr


__all__ = ("Achievement",)


class Achievement:
    """
    **Attributes**

    icon_url: str

    id: int

    name: str

    grouping: str

    ordering: int

    slug: str

    description: str

    mode: Optional[:class:`GameModeStr`]

    instructions: Optional[str]
    """

    __slots__ = (
        "icon_url",
        "id",
        "name",
        "grouping",
        "ordering",
        "slug",
        "description",
        "mode",
        "instructions",
    )

    def __init__(self, data):
        self.icon_url: str = get_required(data, "icon_url")
        self.id: int = get_required(data, "id")
        self.name: str = get_required(data, "name")
        self.grouping: str = get_required(data, "grouping")
        self.ordering: int = get_required(data, "ordering")
        self.slug: str = get_required(data, "slug")
        self.description: str = get_required(data, "description")
        self.mode: GameModeStr = get_optional(data, "mode", GameModeStr)
        self.instructions: Optional[str] = get_required(data, "instructions")

    def __repr__(self):
        return prettify(self, "name", "description")
