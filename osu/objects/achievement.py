from typing import Optional

from ..util import prettify, get_optional
from ..enums import GameModeStr


class Achievement:
    """
    **Attributes**

    icon_url: :class:`str`

    id: :class:`int`

    name: :class:`str`

    grouping: :class:`str`

    ordering: :class:`int`

    slug: :class:`str`

    description: :class:`str`

    mode: Optional[:class:`GameModeStr`]

    instructions: Optional[:class:`str`]
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
        self.icon_url: str = data["icon_url"]
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.grouping: str = data["grouping"]
        self.ordering: int = data["ordering"]
        self.slug: str = data["slug"]
        self.description: str = data["description"]
        self.mode: GameModeStr = get_optional(data, "mode", GameModeStr)
        self.instructions: Optional[str] = data["instructions"]

    def __repr__(self):
        return prettify(self, "name", "description")
