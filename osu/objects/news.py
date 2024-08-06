from dateutil import parser
from typing import Optional, TYPE_CHECKING

from ..util import prettify, get_optional, get_required

if TYPE_CHECKING:
    from datetime import datetime


class NewsPost:
    """
    **Attributes**

    author: :class:`str`

    edit_url: :class:`str`
        Link to the file view on GitHub.

    first_image: Optional[:class:`str`]
        Link to the first image in the document.

    id: :class:`int`

    published_at: :class:`datetime.datetime`

    slug: :class:`str`
        Filename without the extension, used in URLs.

    title: :class:`str`

    updated_at: :class:`datetime.datetime`

    content: Optional[:class:`str`]
        HTML post content.

    navigation: Optional[:class:`Navigation`]
        Navigation metadata.

    preview: Optional[:class:`str`]
        First paragraph of content with HTML markup stripped.
    """

    __slots__ = (
        "author",
        "edit_url",
        "first_image",
        "id",
        "published_at",
        "slug",
        "title",
        "updated_at",
        "content",
        "navigation",
        "preview",
    )

    def __init__(self, data):
        self.author: str = get_required(data, "author")
        self.edit_url: str = get_required(data, "edit_url")
        self.first_image: Optional[str] = get_required(data, "first_image")
        self.id: int = get_required(data, "id")
        self.published_at: datetime = parser.parse(get_required(data, "published_at"))
        self.slug: str = get_required(data, "slug")
        self.title: str = get_required(data, "title")
        self.updated_at: datetime = parser.parse(get_required(data, "updated_at"))
        self.content: Optional[str] = data.get("content")
        self.navigation: Optional[Navigation] = get_optional(data, "navigation", Navigation)
        self.preview: Optional[str] = data.get("preview")

    def __repr__(self):
        return prettify(self, "title")


class Navigation:
    """
    **Attributes**

    newer: Optional[:class:`NewsPost`]
        null if the next post is not present.

    older: Optional[:class:`NewsPost`]
        null if the previous post is not present.
    """

    __slots__ = ("newer", "older")

    def __init__(self, data):
        self.newer: Optional[NewsPost] = get_optional(data, "newer", NewsPost)
        self.older: Optional[NewsPost] = get_optional(data, "older", NewsPost)

    def __repr__(self):
        return prettify(self, "newer", "older")
