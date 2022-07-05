from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

user_id = 14895608
mode = 'osu'
rankings = client.get_ranking('osu', 'performance')
for ranking in rankings.ranking:
    print(f"{ranking.user.username} - #{ranking.global_rank} ({ranking.pp})")

rankings2 = client.get_ranking('osu', 'performance', cursor=rankings.cursor)
for ranking in rankings2.ranking:
    print(f"{ranking.user.username} - #{ranking.global_rank} ({ranking.pp})")
