class WikiPage:
    """
    Represents a wiki article

    **Attributes**

    layout: :class:`str`
        The layout type for the page.

    locale: :class:`str`
        All lowercase BCP 47 language tag.

    markdown: :class:`str`
        Markdown content.

    path: :class:`str`
        Path of the article.

    subtitle: :class:`str`
        The article's subtitle.

    tags: :class:`list`
        list containing objects of type :class:`str`. Associated tags for the article.

    title: :class:`str`
        The article's title.
    """
    __slots__ = (
        "layout", "locale", "markdown", "path", "subtitle",
        "tags", "title"
    )

    def __init__(self, data):
        self.layout = data['layout']
        self.locale = data['locale']
        self.markdown = data['markdown']
        self.path = data['path']
        self.subtitle = data['subtitle']
        self.tags = data['tags']
        self.title = data['title']
