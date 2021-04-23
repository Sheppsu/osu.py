from osu import Client, AuthHandler


client_id = 0
client_secret = "****"
redirect_uri = "http://127.0.0.1:8080"

auth = AuthHandler(client_id, client_secret, redirect_uri)
auth.get_auth_token()

client = Client(auth)

ID = 2740197
beatmap = client.get_beatmap(ID)
print(beatmap.beatmapset.title)
