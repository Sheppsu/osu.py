from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

ID = 1031991
beatmap = client.get_beatmap(ID)
print(beatmap.beatmapset.title)