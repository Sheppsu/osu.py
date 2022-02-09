from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

user_id = 14895608
mode = 'osu'
scores = client.get_user_scores(user_id, 'best', mode=mode, limit=10)
for score in scores:
    print(f"{score.beatmapset.title}: {score.pp}")
