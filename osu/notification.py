import asyncio
import json
from dateutil import parser
import traceback

from .objects import Notification, ChatChannel, UserCompact, ChatMessage

try:
    import websockets
    has_websockets = True
except ImportError:
    has_websockets = False


class NotificationWebsocket:
    """
    Requires osu.py is installed with the 'notifications' feature

    This class allows you to receive notifications without constantly polling the server.
    To utilize it you should do either of:
    - Make a class inheriting this one and redefine the event functions (on_logout, on_new, ...).
    - Use the event function as a decorator, read more on its use under its docs.

    **Event types**

    on_ready
        Fired when the websocket establishes connection.

    on_logout
        Server will disconnect session after sending this event so don't try to reconnect.

    on_new
        New notification. See :class:`Notification` object for notification types.

        **Arguments**

        notification: :class:`Notification`

    on_read
        Notification has been read.

        **Arguments**

        notifications: Sequence[:class:`ReadNotification`]
            list of notifications that were read

        timestamp: :class:`datetime.datetime`
            time at which the notifications were read

    on_chat_channel_join
        Broadcast to the user when the user joins a chat channel.

        **Arguments**

        channel: :class:`ChatChannel`
            Has the `current_user_attributes`, `last_message_id`, and `users` attributes.

    on_chat_channel_part
        Broadcast to the user when the user leaves a chat channel.

        **Arguments**

        channel: :class:`ChatChannel`
            Has the `current_user_attributes`, `last_message_id`, and `users` attributes.

    on_chat_message_new
        Sent to the user when the user receives a chat message.

        Messages intented for a user are always sent even if the user does not
        currently have the channel open. Such messages include PM and Announcement messages.

        Other messages, e.g. public channel messages are not sent if the user
        is no longer present in the channel.

        **Arguments**

        messages: Sequence[:class:`ChatMessage`]
            The message received

        users: Sequence[:class:`UserCompact`]
            The related uesrs who sent the messages.

    on_unplanned_disconnect
        Event fired by NotificationWebsocket object when there's a disconnection
        without having been sent a logout event.
    """

    valid_events = [
        "ready",
        "logout",
        "new",
        "read",
        "unplanned_disconnect",
        "chat_channel_join",
        "chat_channel_part",
        "chat_message_new",
    ]
    valid_event_functions = ["on_" + event for event in valid_events]

    def __init__(self, notification_uri, auth, loop=None):
        """
        **Arguments**

        notification_url: :class:`str`
            url endpoint to connect to. Can obtain one via get_notifications

        auth: :class:`AuthHandler`
            The same auth handler used for Client
        """
        if not has_websockets:
            raise RuntimeError(
                "websockets is required to use NotificationWebsocket. "
                "Install osu.py with the 'notifications' feature to use it."
            )

        self.auth = auth
        self.uri = notification_uri
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.ws = None
        self.connected = False

    async def _run(self):
        headers = {"Authorization": f"Bearer {self.auth.token}"}
        async with websockets.connect(self.uri, extra_headers=headers) as ws:
            self.ws = ws
            await self._on_ready()
            while self.connected:
                try:
                    event = await self.ws.recv()
                except websockets.exceptions.ConnectionClosed:
                    self.ws = None
                    self.connected = False
                    await self._on_unplanned_disconnect()
                    return

                event = json.loads(event)
                if "error" in event:
                    print(f"Notification websocket received error: {event['error']}")
                    continue
                event_type = event["event"].replace(".", "_")
                del event["event"]

                # TODO: run event funcs using run_coroutine_threadsafe

                func = getattr(self, "_on_" + event_type)
                if func is None:
                    return print(f"Received {event_type} event but cannot parse it.")
                try:
                    await func(event)
                except:
                    traceback.print_exc()

    def connect(self):
        """
        Connect to the uri and start receiving events.
        This function does not return until the websocket disconnects.
        """
        self.loop.run_until_complete(self._run())

    def event(self, func):
        """
        Decorator for adding event functions. Example:

        .. code-block:: Python

            notification_websocket = NotificationWebsocket(notif_uri, auth)

            @notification_websocket.event()
            def new(notification):
                print(notification.name)
        """
        if func.__name__ not in self.valid_event_functions:
            raise ValueError(
                f"This is not a valid event name. Valid events consist of " f"{', '.join(self.valid_event_functions)}"
            )
        setattr(self, func.__name__, func)

    # Default events

    # Fired by NotificationSocket when websocket establishes connection.
    async def _on_ready(self):
        self.connected = True
        if hasattr(self, "on_ready"):
            await self.on_ready()

    async def _on_logout(self, event):
        self.connected = False
        if hasattr(self, "on_logout"):
            await self.on_logout()

    async def _on_new(self, event):
        if hasattr(self, "on_new"):
            data = Notification(event["data"])
            await self.on_new(data)

    async def _on_read(self, event):
        if hasattr(self, "on_read"):
            data = event["data"]
            notifications = list(map(lambda notification: notification["id"], data["notifications"]))
            timestamp = parser.parse(data["timestamp"])
            await self.on_read(notifications, timestamp)

    async def _on_chat_channel_join(self, event):
        if hasattr(self, "on_chat_channel_join"):
            await self.on_chat_channel_join(ChatChannel(event["data"]))

    async def _on_chat_channel_part(self, event):
        if hasattr(self, "on_chat_channel_part"):
            await self.on_chat_channel_part(ChatChannel(event["data"]))

    async def _on_chat_message_new(self, event):
        if hasattr(self, "on_chat_message_new"):
            data = event["data"]
            messages = list(map(ChatMessage, data["messages"]))
            users = list(map(UserCompact, data["users"]))
            await self.on_chat_message_new(messages, users)

    # Event fired by NotificationWebsocket object when connection without having been sent a logout event.
    async def _on_unplanned_disconnect(self):
        if hasattr(self, "on_unplanned_disconnect"):
            await self.on_unplanned_disconnect()

    # Commands

    async def send_json(self, event):
        await self.ws.send(json.dumps({"event": event}))

    async def chat_start(self):
        await self.send_json("chat.start")

    async def chat_end(self):
        await self.send_json("chat.end")
