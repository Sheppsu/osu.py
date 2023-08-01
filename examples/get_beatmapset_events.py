from osu import Client, BeatmapsetEventType, BeatmapsetEventSort
from datetime import datetime
import os


client_id = int(os.getenv('CLIENT_ID'))
client_secret = os.getenv('CLIENT_SECRET')
redirect_url = None

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

result = client.get_beatmapset_events(type=BeatmapsetEventType.LOVE, sort=BeatmapsetEventSort.ASC,
                                      min_date=datetime(2020, 1, 1))
for event in result.events:
    print(event)
