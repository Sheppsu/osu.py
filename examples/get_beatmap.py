from osu import Client, AuthHandler
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_uri = "http://127.0.0.1:8080"

auth = AuthHandler(client_id, client_secret, redirect_uri)
auth.get_auth_token()

client = Client(auth)

ID = 1031991
beatmap = client.get_beatmap(ID)
print(beatmap.beatmapset.title)
