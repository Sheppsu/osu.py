class KudosuHistory:
    """
    **Attributes**

    id: :class:`int`

    action: :class:`str`
        Either give, reset, or revoke.

    amount: :class:`int`

    model: :class:`str`
        Object type which the exchange happened on (forum_post, etc).

    created_at: :ref:`Timestamp`

    giver: :class:`Giver`
        Simple detail of the user who started the exchange.

    post: :class:`Post`
        Simple detail of the object for display.
    """
    __slots__ = (
        "id", "action", "amount", "model", "created_at", "giver", "post"
    )

    def __init__(self, data):
        self.id = data['id']
        self.action = data['action']
        self.amount = data['amount']
        self.model = data['model']
        self.created_at = data['created_at']
        self.giver = Giver(data['giver'])
        self.post = Post(data['post'])


class Post:
    """
    **Attributes**

    url: :class:`str`
        Url of the object.

    title: :class:`str`
        Title of the object. It'll be "[deleted beatmap]" for deleted beatmaps.
    """
    __slots__ = (
        "url", "title"
    )

    def __init__(self, data):
        self.url = data['url']
        self.title = data['title']


class Giver:
    """
    **Attributes**

    url: :class:`str`

    username: :class:`str`
    """
    __slots__ = (
        "url", "username"
    )

    def __init__(self, data):
        self.url = data['url']
        self.username = data['username']
