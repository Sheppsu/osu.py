from dateutil import parser

from ..util import prettify


class NewsPost:
    """
    **Attributes**

    author: :class:`str`

    edit_url: :class:`str`
        Link to the file view on GitHub.

    first_image: :class:`str` or :class:`NoneType`
        Link to the first image in the document.

    id: :class:`int`

    published_at: :class:`datetime.datetime`

    slug: :class:`str`
        Filename without the extension, used in URLs.

    title: :class:`str`

    updated_at: :class:`datetime.datetime`

    **Optional Attributes**

    content: :class:`str`
        HTML post content.

    navigation: :class:`Navigation`
        Navigation metadata.

    preview: :class:`str`
        First paragraph of content with HTML markup stripped.
    """
    __slots__ = (
        "author", "edit_url", "first_image", "id",
        "published_at", "slug", "title", "updated_at",
        "content", "navigation", "preview"
    )

    def __init__(self, data):
        self.author = data['author']
        self.edit_url = data['edit_url']
        self.first_image = data['first_image']
        self.id = data['id']
        self.published_at = parser.parse(data['published_at'])
        self.slug = data['slug']
        self.title = data['title']
        self.updated_at = parser.parse(data['updated_at'])
        self.content = data.get("content", "")
        self.navigation = Navigation(data) if "navigation" in data else None
        self.preview = data.get("preview", "")

    def __repr__(self):
        return prettify(self, 'title')


class Navigation:
    """
    **Attributes**

    newer: :class:`NewsPost` or :class:`NoneType`
        null if the next post is not present.

    older: :class:`NewsPost` or :class:`NoneType`
        null if the previous post is not present.
    """
    __slots__ = ("newer", "older")

    def __init__(self, data):
        self.newer = NewsPost(data['newer']) if data["newer"] is not None else None
        self.older = NewsPost(data['older']) if data["older"] is not None else None

    def __repr__(self):
        return prettify(self, 'newer', 'older')
