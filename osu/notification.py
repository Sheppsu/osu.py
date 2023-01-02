import websockets
import asyncio
import json
from dateutil import parser

from .objects import Notification, ReadNotification


class NotificationWebsocket:
    """
    This class allows you to receive notifications without constantly polling the server.
    To utilize it you should do either of:
        - Make a class inheriting this one and redefine the event functions (on_logout, on_new, ...).
        - Use the event function as a decorator, read more on its use under its docs.

    **Event types**

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

    on_unplanned_disconnect
        Event fired by NotificationWebsocket object when there's a disconnection
        without having been sent a logout event.
    """
    valid_events = [
        'logout', 'new', 'read', 'unplanned_disconnect'
    ]
    valid_event_functions = ["on_" + event for event in valid_events]

    def __init__(self, notification_uri, auth):
        """
        **Arguments**

        notification_url: :class:`str`
            url endpoint to connect to. Can obtain one via get_notifications

        auth: :class:`AuthHandler`
            The same auth handler used for Client
        """

        self.auth = auth
        self.uri = notification_uri
        self.loop = asyncio.get_event_loop()
        self.ws = None
        self.connected = False

    async def _run(self):
        headers = {
            "Authorization": f"Bearer {self.auth.token}"
        }
        async with websockets.connect(self.uri, extra_headers=headers) as ws:
            self.ws = ws
            self.connected = True
            while self.connected:
                print("beep boop")
                try:
                    event = await self.ws.recv()
                except websockets.exceptions.ConnectionClosed:
                    self.ws = None
                    self.connected = False
                    self._on_unplanned_disconnect()
                    return

                event = json.loads(event)
                if 'error' in event:
                    print(f"Error received: {event['error']}")
                    continue
                event_type = event['event']
                del event['event']

                getattr(self, "_on_"+event_type, event_type)(event)

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
            raise NameError(f"This is not a valid event name. Valid events consist of "
                            f"{', '.join(self.valid_event_functions)}")
        setattr(self, func.__name__, func)

    # Default events

    def _on_logout(self, event):
        self.connected = False
        if hasattr(self, 'on_logout'):
            self.on_logout()

    def _on_new(self, event):
        data = Notification(event["data"])
        if hasattr(self, 'on_new'):
            self.on_new(data)

    def _on_read(self, event):
        data = event["data"]
        notifications = list(map(ReadNotification, data["notifications"]))
        timestamp = parser.parse(data["timestamp"])
        if hasattr(self, 'on_read'):
            self.on_read(notifications, timestamp)

    # Event fired by NotificationWebsocket object when connection without having been sent a logout event.
    def _on_unplanned_disconnect(self):
        if hasattr(self, 'on_unplanned_disconnect'):
            self.on_unplanned_disconnect()
