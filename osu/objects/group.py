from ..util import prettify


class Group:
    """
    This object isn't returned by any endpoints yet, it is here purely as a reference for :class:`UserGroup`

    **Attributes**

    id: :class:`int`

    identifier: :class:`str`
        Unique string to identify the group.

    is_probationary: :class:`str`
        Whether members of this group are considered probationary.

    has_playmodes: :class:`bool`
        If this group associates GameModes with a user's membership, e.g. BN/NAT members

    has_listing: :class:`bool`
        Whether this group displays a listing at /groups/{id}

    name: :class:`str`

    short_name: :class:`str`
        Short name of the group for display.

    colour: :class:`str` or :class:`NoneType`

    **Optional Attributes**

    description: :class:`Description` or :class:`NoneType`
        A dictionary with keys html and markdown.
    """
    __slots__ = (
        "id", "identifier", "is_probationary", "has_playmodes", "has_listing",
        "name", "short_name", "colour", "description"
    )

    def __init__(self, data):
        self.id = data['id']
        self.identifier = data['identifier']
        self.is_probationary = data['is_probationary']
        self.has_playmodes = data['has_playmodes']
        self.name = data['name']
        self.short_name = data['short_name']
        self.colour = data['colour']
        self.description = Description(data['description']) if data.get('description') is not None else None

    def __repr__(self):
        return prettify(self, 'name')


class Description:
    """
    **Attributes**

    html: :class:`str`

    markdown: :class:`str`
    """

    def __init__(self, data):
        self.html = data['html']
        self.markdown = data['markdown']

    def __repr__(self):
        return prettify(self)


class UserGroup(Group):
    """
    Describes the :class:`Group` membership of a :class:`User`.
    It contains all of the attributes of the :class:`Group`, in addition to what is listed here.

    **Attributes**

    playmodes: Sequence[:class:`str`]
        GameModes associated with this membership (null if has_playmodes is unset).
    """
    __slots__ = (
        "playmodes",
    )

    def __init__(self, data):
        super().__init__(data)
        self.playmodes = data['playmodes']

    def __repr__(self):
        return super().__repr__()
