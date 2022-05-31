from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

bm_id = 1031991
beatmap = client.get_beatmap(bm_id)
print(f"{beatmap.beatmapset.artist} - {beatmap.beatmapset.title}")

bm_ids = [1765081, 1454407, 2987037, 3356285, 1530633, 1693575]
beatmaps = client.get_beatmaps(bm_ids)
for beatmap in beatmaps:
    print(f"{beatmap.beatmapset.artist} - {beatmap.beatmapset.title}")
