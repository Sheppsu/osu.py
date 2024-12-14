from typing import List, Optional, Union, TYPE_CHECKING

from ..util import prettify, get_required

if TYPE_CHECKING:
    from .user import UserCompact


__all__ = ("WikiPage", "SearchResults")


class WikiPage:
    """
    Represents a wiki article

    **Attributes**

    available_locales: List[str]
        All available locales for the article.

    layout: str
        The layout type for the page.

    locale: str
        All lowercase BCP 47 language tag.

    markdown: str
        Markdown content.

    path: str
        Path of the article.

    subtitle: Optional[str]
        The article's subtitle.

    tags: List[str]
        Associated tags for the article.

    title: str
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
        self.available_locales: List[str] = get_required(data, "available_locales")
        self.layout: str = get_required(data, "layout")
        self.locale: str = get_required(data, "locale")
        self.markdown: str = get_required(data, "markdown")
        self.path: str = get_required(data, "path")
        self.subtitle: Optional[str] = get_required(data, "subtitle")
        self.tags: List[str] = get_required(data, "tags")
        self.title: str = get_required(data, "title")

    def __repr__(self):
        return prettify(self, "title")


class SearchResults:
    """
    Represents the results of a search.

    **Attributes**

    results: List[Union[:class:`UserCompact`, :class:`WikiPage`]]
        type depends on search type

    total: int
    """

    __slots__ = ("results", "total")

    def __init__(self, data, data_type):
        self.results: List[Union[UserCompact, WikiPage]] = list(map(data_type, get_required(data, "data")))
        self.total: int = get_required(data, "total")

    def __repr__(self):
        return prettify(self, "results", "total")
