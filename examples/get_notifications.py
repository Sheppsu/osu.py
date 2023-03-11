from util_for_examples import get_lazer_client
from osu import (
    NotificationWebsocket as NotificationWebsocketBase,
    NotificationsUtil, AsynchronousClient
)
import asyncio


class NotificationWebsocket(NotificationWebsocketBase):
    client: AsynchronousClient
    notifications: list

    def __init__(self):
        loop = asyncio.get_event_loop()
        endpoint = loop.run_until_complete(self.setup())
        super().__init__(endpoint, self.client.auth, loop)

    async def setup(self):
        print("Setting up...")
        self.client = get_lazer_client(asynchronous=True)
        result = await self.client.get_notifications()
        self.notifications = result["notifications"]
        return result["notification_endpoint"]

    async def on_ready(self):
        print("Connected!")
        await ws.chat_start()
        unread = list(map(lambda n: NotificationsUtil(id=n.id), filter(lambda n: not n.is_read, self.notifications)))
        print(f"{len(unread)} unread notifications: {''.join(map(repr, unread))}")
        if len(unread) > 0:
            await self.client.mark_notifications_read(notifications=unread)

    async def on_logout(self):
        print("Server logged us out.")

    async def on_new(self, notification):
        print(f"New notification: {notification}")

    async def on_read(self, notifications, timestamp):
        print(f"Read {len(notifications)} notifications at {timestamp}: {', '.join(map(str, notifications))}")

    async def on_unplanned_disconnect(self):
        print("Unplanned disconnection occurred!")


ws = NotificationWebsocket()
ws.connect()
