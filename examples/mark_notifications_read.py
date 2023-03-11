from util_for_examples import get_lazer_client
from osu import NotificationsUtil, NotificationCategory


client = get_lazer_client()

notifications = [
    NotificationsUtil(category=NotificationCategory.USER_BEATMAPSET_NEW)
]
client.mark_notifications_read(notifications=notifications)
