from osu import Client, AuthHandler


client_id = 0
client_secret = "****"
redirect_uri = "http://127.0.0.1:8080"

auth = AuthHandler(client_id, client_secret, redirect_uri)
auth.get_auth_token()

client = Client(auth)

user_id = 14895608
mode = 'osu'
scores = client.get_user_scores(user_id, 'best', mode=mode, limit=10)
for score in scores:
    print(f"{score.beatmapset.title}: {score.pp}")
