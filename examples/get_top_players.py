from osu import Client, GameModeStr, RankingType
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

# Print the top 100 players
cursor = None
for _ in range(2):
    ranking = client.get_ranking(GameModeStr.STANDARD, RankingType.PERFORMANCE, cursor=cursor)
    cursor = ranking.cursor
    for r in ranking.ranking:
        print(f"{r.user.username} - #{r.global_rank} ({r.pp})")

