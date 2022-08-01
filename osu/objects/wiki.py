from ..util import prettify


class WikiPage:
    """
    Represents a wiki article

    **Attributes**

    available_locales: Sequence[:class:`str`]
        All available locales for the article.

    layout: :class:`str`
        The layout type for the page.

    locale: :class:`str`
        All lowercase BCP 47 language tag.

    markdown: :class:`str`
        Markdown content.

    path: :class:`str`
        Path of the article.

    subtitle: :class:`str` or :class:`NoneType`
        The article's subtitle.

    tags: Sequence[:class:`str`]
        Associated tags for the article.

    title: :class:`str`
        The article's title.
    """
    __slots__ = (
        'available_locales', 'layout', 'locale', 'markdown', 'path', 'subtitle',
        'tags', 'title'
    )

    def __init__(self, data):
        self.available_locales = data['available_locales']
        self.layout = data['layout']
        self.locale = data['locale']
        self.markdown = data['markdown']
        self.path = data['path']
        self.subtitle = data['subtitle']
        self.tags = data['tags']
        self.title = data['title']

    def __repr__(self):
        return prettify(self, 'title')
