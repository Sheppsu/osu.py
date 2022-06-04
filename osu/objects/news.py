class NewsPost:
    """
    **Attributes**

    author: :class:`str`

    edit_url: :class:`str`
        Link to the file view on GitHub.

    first_image: :class:`str`
        Link to the first image in the document.

    id: :class:`int`

    published_at: :ref:`Timestamp`

    slug: :class:`str`
        Filename without the extension, used in URLs.

    title: :class:`str`

    updated_at: :ref:`Timestamp`

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
        self.published_at = data['published_at']
        self.slug = data['slug']
        self.title = data['title']
        self.updated_at = data['updated_at']
        self.content = data.get("content", "")
        self.navigation = Navigation(data) if "navigation" in data else None
        self.preview = data.get("preview", "")


class Navigation:
    """
    **Attributes**

    newer: :class:`NewsPost`
        null if the next post is not present.

    older: :class:`NewsPost`
        null if the previous post is not present.
    """
    __slots__ = ("newer", "older")

    def __init__(self, data):
        self.newer = NewsPost(data['newer']) if "newer" in data else None
        self.older = NewsPost(data['older']) if "newer" in data else None