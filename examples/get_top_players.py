from osu import Client, GameModeStr, RankingType
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_credentials(client_id, client_secret, redirect_url)

# Print the top 100 players
cursor = None
for _ in range(2):
    rankings = client.get_ranking(GameModeStr.STANDARD, RankingType.PERFORMANCE, cursor=cursor)
    cursor = rankings.cursor
    for stats in rankings.ranking:
        rank_change = stats.rank_change_since_30_days
        print(
            f"[{'+' if rank_change >= 0 else ''}{rank_change}] "
            f"{stats.user.username} - #{stats.global_rank} ({stats.pp})"
        )