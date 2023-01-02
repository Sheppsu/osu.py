from .user import CurrentUserAttributes, UserCompact
from dateutil import parser

from ..util import prettify
from ..enums import ChatChannelType


class ChatChannel:
    """
    Represents an individual chat "channel" in the game.

    **Attributes**

    Some attributes will be :class:`NoneType`

    channel_id: :class:`int`

    current_user_attributes: :class:`CurrentUserAttributes`
        only present on some responses

    name: :class:`str`

    description: :class:`str` or :class:`NoneType`

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
        "type", "last_read_id", "last_message_id", "recent_messages",
        "moderated", "users"
    )

    def __init__(self, data):
        self.channel_id = data.get('channel_id')
        self.current_user_attributes = CurrentUserAttributes(data['current_user_attributes'],
                                                             "ChatChannelUserAttributes") \
            if data.get("current_user_attributes") is not None else None
        self.name = data.get("name")
        self.description = data.get("description")
        self.icon = data.get("icon")
        self.type = ChatChannelType(data["type"]) if data.get("type") is not None else None
        self.last_read_id = data.get("last_read_id")
        self.last_message_id = data.get("last_message_id")
        self.recent_messages = list(map(ChatMessage, data.get('recent_messages', [])))
        self.moderated = data.get("moderated")
        self.users = data.get("users")

    def __repr__(self):
        return prettify(self, 'name')


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

    timestamp: :class:`datetime.datetime`
        when the message was sent

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
        self.timestamp = parser.parse(data['timestamp'])
        self.content = data['content']
        self.is_action = data['is_action']
        self.sender = UserCompact(data['sender'])

    def __repr__(self):
        return prettify(self, 'content')
