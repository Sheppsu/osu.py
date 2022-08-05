from osu import Client, BeatmapsetEventType, BeatmapsetEventSort
from datetime import datetime
import os


__all__ = [
    "client", "data"
]


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

data = client.get_beatmapset_events(type=BeatmapsetEventType.LOVE, sort=BeatmapsetEventSort.ASC,
                                    min_date=datetime(2020, 1, 1))
for event in data["events"]:
    print(event.discussion)
