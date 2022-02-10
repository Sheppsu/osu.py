import websockets
import asyncio
import json
import threading

from .objects import Notification


class NotificationWebsocket:
    """
    This class allows you to receive notifications without constantly polling the server.
    To utilize it you should do either of:
        - Make a class inheriting this one and redefine the event functions (logout, new, ...).
        - Use the event function as a decorator, read more on its use under its docs.

    **Init Parameters**

    notification_url: :class:`str`
        url endpoint to connect to. Can obtain one via get_notifications

    auth: :class:`AuthHandler`
        The same auth handler used for Client

    **Event types**

    logout
        Server will disconnect session after sending this event so don't try to reconnect.

    new
        New notification. See :class:`Notification` object for notification types.

        **Arguments**

        notification: :class:`Notification`

    read
        Notification has been read.

        **Arguments**

        ids: :class:`int`
            list of ids of Notifications which are read.

    unplanned_disconnect
        Event fired by NotificationWebsocket object when connection without having been sent a logout event.
        Default function fires connect to try and reconnect.
    """
    valid_events = [
        'logout', 'new', 'read', 'unplanned_disconnect'
    ]

    def __init__(self, notification_uri, auth):
        self.auth = auth
        self.uri = notification_uri
        self.loop = asyncio.get_event_loop()
        self.ws = None
        self.connected = False

    async def _run(self):
        headers = {
            "Authorization": f"Bearer {self.auth.token}"
        }
        async with websockets.connect(self.uri, headers=headers) as ws:
            self.ws = ws
            self.connected = True
            while self.connected:
                try:
                    event = await self.ws.recv()
                except websockets.exceptions.ConnectionClosed:
                    self.ws = None
                    self.connected = False
                    self._on_unplanned_disconnect()
                    return

                event = json.loads(event)
                event_type = event['event']

                getattr(self, "_"+event_type, event_type)(*list(event.values()))

    def connect(self):
        """
        Connect to the uri and start receiving events.
        Runs in a thread.
        """
        run = threading.Thread(target=self.loop.run_until_complete, args=(self._run,))
        run.start()

    def event(self, func):
        """
        Decorator for adding event functions. Example:

        .. code-block:: Python

            notification_websocket = NotificationWebsocket(notif_uri, auth)

            @notification_websocket.event()
            def new(notification):
                print(notification.name)
        """
        if func.__name__ not in self.valid_events:
            raise NameError(f"This is not a valid event name. Valid events consist of {', '.join(self.valid_events)}")
        setattr(self, func.__name__, func)

    # Events

    def _on_logout(self):
        self.connected = False
        if hasattr(self, 'on_logout'):
            self.on_logout()

    def _on_new(self, data):
        data = Notification(data)
        if hasattr(self, 'on_new'):
            self.on_new(data)

    def _on_read(self, data):
        if hasattr(self, 'on_read'):
            self.on_read(data)

    def _on_unplanned_disconnect(self):
        """
        Event fired by NotificationWebsocket object when connection without having been sent a logout event.
        Default function fires connect to try and reconnect.
        """
        self.connect()
        if hasattr(self, 'on_unplanned_disconnect'):
            self.on_unplanned_disconnect()
