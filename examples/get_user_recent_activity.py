from osu import Client, AchievementEvent
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

events = client.get_user_recent_activity(14895608, limit=100)
print(f"Number of events fetched: {len(events)}")
print("List of achievement events:")
print(list(filter(lambda e: isinstance(e, AchievementEvent), events)))
