from .user import CurrentUserAttributes


class ChatChannel:
    """
    Represents an individual chat "channel" in the game.

    **Attributes**

    channel_id: :class:`int`

    current_user_attributes: :class:`CurrentUserAttributes`
        only present on some responses

    name: :class:`str`

    description: :class:`str`

    icon: :class:`str`
        display icon for the channel

    type: :class:`str`
        Below are the channel types and their permission checks for joining/messaging:
        PUBLIC
            None
        PRIVATE
            is player in the allowed groups? (channel.allowed_groups)
        MULTIPLAYER
            is player currently in the mp game?
        SPECTATOR
            None
        TEMPORARY
            deprecated
        PM
            Is either user blocking the other? If so, deny.
            Does the target only accept PMs from friends? Is the current user a friend? If not, deny.
        GROUP
            is player in channel? (user_channels)

    first_message_id: :class:`int`
        message_id of first message (only returned in presence responses)

    last_message_id: :class:`int`
        message_id of last known message (only returned in presence responses)

    recent_messages: class:`list`
        list containing objects of type :class:`ChatMessage`. Up to 50 most recent messages.

    moderated: :class:`bool`
        user can't send message when the value is true (only returned in presence responses)

    users: :class:`list`
        list of user_id that are in the channel (not included for PUBLIC channels)
    """
    __slots__ = (
        "channel_id", "current_user_attributes", "name", "description", "icon",
        "type", "first_message_id", "last_message_id", "recent_messages",
        "moderated", "users"
    )

    def __init__(self, data):
        self.channel_id = data['channel_id']
        self.current_user_attributes = CurrentUserAttributes(data['current_user_attributes'], "ChatChannelUserAttributes")
        self.name = data['name']
        self.description = data['description']
        self.icon = data['icon']
        self.type = data['type']
        self.first_message_id = data['first_message_id']
        self.last_message_id = data['last_message_id']
        self.recent_messages = [ChatMessage(message) for message in data['recent_messages']]
        self.moderated = data['moderated']
        self.users = data['users']


class ChatMessage:
    """
    Represents an individual Message within a :class:`ChatChannel`.

    **Attributes**

    message_id: :class:`int`
        unique identifier for message

    sender_id: :class:`int`
        user_id of the sender

    channel_id: :class:`int`
        channel_id of where the message was sent

    timestamp: :class:`str`
        when the message was sent, ISO-8601

    content: :class:`str`
        message content

    is_action: :class:`bool`
        was this an action? i.e. /me dances

    sender: :class:`UserCompact`
        embeded :class:`UserCompact` object to save additional api lookups
    """
    __slots__ = (
        "message_id", "sender_id", "channel_id", "timestamp", "content", "is_action",
        "sender"
    )

    def __init__(self, data):
        self.message_id = data['message_id']
        self.sender_id = data['sender_id']
        self.channel_id = data['channel_id']
        self.timestamp = data['timestamp']
        self.content = data['content']
        self.is_action = data['is_action']
        self.sender = UserCompact(data['sender'])
