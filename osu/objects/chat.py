from typing import Optional, List, TYPE_CHECKING

from ..util import prettify, get_optional, get_optional_list, get_required, fromisoformat
from ..enums import ChatChannelType, ChatMessageType
from .current_user_attributes import ChatChannelUserAttributes
from .user import UserCompact


if TYPE_CHECKING:
    from datetime import datetime


class ChatChannel:
    """
    Represents an individual chat "channel" in the game.

    **Attributes**

    channel_id: :class:`int`

    name: :class:`str`

    description: Optional[:class:`str`]

    icon: Optional[:class:`str`]
        display icon for the channel

    type: :class:`ChatChannelType`

    moderated: :class:`bool`
        user can't send message when the value is `True`

    uuid: Optional[:class:`str`]
        value from requests that is relayed back to the sender.

    current_user_attributes: Optional[:class:`ChatChannelUserAttributes`]
        only present on some responses

    last_message_id: Optional[:class:`int`]
        message_id of last known message (only returned in presence responses)

    recent_messages: Optional[List[:class:`ChatMessage`]]
        [DEPRECATED] up to 50 most recent messages

    users: Optional[List[:class:`int`]]
        list of user ids that are in the channel (not included for PUBLIC channels).
    """

    __slots__ = (
        "channel_id",
        "name",
        "description",
        "icon",
        "type",
        "moderated",
        "uuid",
        "current_user_attributes",
        "last_message_id",
        "recent_messages",
        "users",
    )

    def __init__(self, data):
        self.channel_id: int = get_required(data, "channel_id")
        self.name: str = get_required(data, "name")
        self.description: Optional[str] = data.get("description")
        self.icon: Optional[str] = data.get("icon")
        self.type: ChatChannelType = ChatChannelType(get_required(data, "type"))
        self.moderated: bool = get_required(data, "moderated")

        self.uuid: Optional[str] = data.get("uuid")
        self.current_user_attributes: Optional[ChatChannelUserAttributes] = get_optional(
            data, "current_user_attributes", ChatChannelUserAttributes
        )
        self.last_message_id: Optional[int] = data.get("last_message_id")
        self.recent_messages: Optional[List[ChatMessage]] = get_optional_list(data, "recent_messages", ChatMessage)
        self.users: Optional[List[int]] = data.get("users")

    def __repr__(self):
        return prettify(self, "name")


class ChatMessage:
    """
    Represents an individual Message within a :class:`ChatChannel`.

    **Attributes**

    channel_id: :class:`int`
        channel_id of where the message was sent

    content: :class:`str`
        message content

    is_action: :class:`bool`
        was this an action? i.e. /me dances

    message_id: :class:`int`
        unique identifier for message

    sender_id: :class:`int`
        user_id of the sender

    timestamp: :class:`datetime.datetime`
        when the message was sent

    type: :class:`ChatMessageType`

    uuid: Optional[:class:`str`]
        message identifier originally sent by client

    sender: Optional[:class:`UserCompact`]
        embedded :class:`UserCompact` object to save additional api lookups
    """

    __slots__ = (
        "channel_id",
        "content",
        "is_action",
        "message_id",
        "sender_id",
        "timestamp",
        "type",
        "uuid",
        "sender",
    )

    def __init__(self, data):
        self.channel_id: int = get_required(data, "channel_id")
        self.content: str = get_required(data, "content")
        self.is_action: bool = get_required(data, "is_action")
        self.message_id: int = get_required(data, "message_id")
        self.sender_id: int = get_required(data, "sender_id")
        self.timestamp: datetime = fromisoformat(get_required(data, "timestamp"))
        self.type: ChatMessageType = ChatMessageType(get_required(data, "type"))
        self.uuid: Optional[str] = data.get("uuid")
        self.sender: Optional[UserCompact] = get_optional(data, "sender", UserCompact)

    def __repr__(self):
        return prettify(self, "sender_id" if self.sender is None else "sender", "content")
