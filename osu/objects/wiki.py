from typing import List, Optional, Union, TYPE_CHECKING

from ..util import prettify


if TYPE_CHECKING:
    from .user import UserCompact


class WikiPage:
    """
    Represents a wiki article

    **Attributes**

    available_locales: List[:class:`str`]
        All available locales for the article.

    layout: :class:`str`
        The layout type for the page.

    locale: :class:`str`
        All lowercase BCP 47 language tag.

    markdown: :class:`str`
        Markdown content.

    path: :class:`str`
        Path of the article.

    subtitle: Optional[:class:`str`]
        The article's subtitle.

    tags: List[:class:`str`]
        Associated tags for the article.

    title: :class:`str`
        The article's title.
    """

    __slots__ = (
        "available_locales",
        "layout",
        "locale",
        "markdown",
        "path",
        "subtitle",
        "tags",
        "title",
    )

    def __init__(self, data):
        self.available_locales: List[str] = data["available_locales"]
        self.layout: str = data["layout"]
        self.locale: str = data["locale"]
        self.markdown: str = data["markdown"]
        self.path: str = data["path"]
        self.subtitle: Optional[str] = data["subtitle"]
        self.tags: List[str] = data["tags"]
        self.title: str = data["title"]

    def __repr__(self):
        return prettify(self, "title")


class SearchResults:
    """
    Represents the results of a search.

    **Attributes**

    results: List[Union[:class:`UserCompact`, :class:`WikiPage`]]
        type depends on search type

    total: :class:`int`
    """

    __slots__ = ("results", "total")

    def __init__(self, data, data_type):
        self.results: List[Union[UserCompact, WikiPage]] = list(map(data_type, data["data"]))
        self.total: int = data["total"]

    def __repr__(self):
        return prettify(self, "results", "total")
