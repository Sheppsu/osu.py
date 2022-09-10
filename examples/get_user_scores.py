from osu import Client, UserScoreType
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

user_id = 7562902
recent_score = client.get_user_scores(user_id, UserScoreType.RECENT, limit=1)
top_scores = client.get_user_scores(user_id, UserScoreType.BEST, limit=5)
first_place_scores = client.get_user_scores(user_id, UserScoreType.FIRSTS, limit=5)

if not recent_score:
    print("No recent scores")
else:
    score = recent_score[0]
    print(f"{score.beatmapset.artist} - {score.beatmapset.title}")
for i, score in enumerate(top_scores):
    print(f"{i+1}. {score.beatmapset.artist} - {score.beatmapset.title}: {score.pp}")
if not first_place_scores:
    print("No first place scores")
else:
    for i, score in enumerate(first_place_scores):
        print(f"{i+1}. {score.beatmapset.artist} - {score.beatmapset.title}")
