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

    name: :class:`str`

    short_name: :class:`str`
        Short name of the group for display.

    colour: :class:`str`

    **Optional Attributes**

    description: :class:`Description`
        A dictionary with keys html and markdown.
    """
    __slots__ = (
        "id", "identifier", "is_probationary", "has_playmodes", "name", "short_name",
        "colour", "description"
    )

    def __init__(self, data):
        self.id = data['id']
        self.identifier = data['identifier']
        self.is_probationary = data['is_probationary']
        self.has_playmodes = data['has_playmodes']
        self.name = data['name']
        self.short_name = data['short_name']
        self.colour = data['colour']
        self.description = data.get('description', None)


class UserGroup(Group):
    """
    Describes the :class:`Group` membership of a :class:`User`. It contains all of the attributes of the :class:`Group`, in addition to what is listed here.

    **Attributes**

    playmodes: :class:`list`
        list containing objects of type :class:`str`. GameModes associated with this membership (null if has_playmodes is unset).
    """
    __slots__ = (
        "playmodes",
    )

    def __init__(self, data):
        super().__init__(data)
        self.playmodes = data['playmodes']
