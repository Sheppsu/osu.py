from util_for_examples import get_lazer_client
from osu import NotificationsUtil, NotificationCategory


client = get_lazer_client()

ret = client.get_notifications()
if len(ret.notifications) == 0:
    print("No notifications to mark read")
notification = ret.notifications[0]
notifications = [
    NotificationsUtil(
        category=notification.name.name,
        id=notification.id,
        object_id=notification.object_id,
        object_type=notification.object_type.name
    )
]
client.mark_notifications_read(notifications=notifications)
print("Marked most recent notification as read")
