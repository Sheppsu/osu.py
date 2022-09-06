from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

ID = 2335553
user_id = 14895608
beatmap_scores = client.get_user_beatmap_scores(ID, user_id)
for score in beatmap_scores:
    print(f"{score.mods} {score.accuracy} {score.pp}")
