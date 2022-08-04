from dateutil import parser

from ..util import prettify


class KudosuHistory:
    """
    **Attributes**

    id: :class:`int`

    action: :class:`str`
        One of give, vote.give, reset, vote.reset, revoke, or vote.revoke.

    amount: :class:`int`

    model: :class:`str`
        Object type which the exchange happened on (forum_post, etc).

    created_at: :class:`datetime.datetime`

    giver: :class:`Giver` or :class:`NoneType`
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
        self.created_at = parser.parse(data['created_at'])
        self.giver = Giver(data['giver']) if data.get('giver') else None
        self.post = Post(data['post'])

    def __repr__(self):
        return prettify(self, 'action', 'amount', 'giver')


class Post:
    """
    **Attributes**

    url: :class:`str` or :class:`NoneType`
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

    def __repr__(self):
        return prettify(self, 'title')


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

    def __repr__(self):
        return prettify(self, 'username')
