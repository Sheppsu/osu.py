from util_for_examples import get_lazer_client
from osu import NotificationWebsocket


client = get_lazer_client()
notifications = client.get_notifications()
print(notifications["notifications"][0])

ws = NotificationWebsocket(notifications["notification_endpoint"], client.auth)


@ws.event
def on_logout():
    print("logout")


@ws.event
def on_new(data):
    print("new")
    print(data)


@ws.event
def on_read(notifications, timestamp):
    print("read")
    print(notifications, timestamp)


@ws.event
def on_unplanned_disconnect():
    print("aaaaaaa")


ws.connect()
