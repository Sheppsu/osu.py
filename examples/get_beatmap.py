from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_credentials(client_id, client_secret, redirect_url)


beatmap = client.get_beatmap(1031991)
print(beatmap)

beatmapset = client.get_beatmapset(407175)
print(beatmapset)

beatmaps = client.get_beatmaps([1765081, 1454407, 2987037, 3356285, 1530633, 1693575])
for beatmap in beatmaps:
    print(beatmap)
