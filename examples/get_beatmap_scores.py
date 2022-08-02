from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

ID = 509388
beatmap_scores = client.get_beatmap_scores(ID)
print("Top 5 scores on this beatmap:")
print("\n".join([f'{i+1}. {score.user.username} {"+"+score.mods.to_readable_string() if score.mods is not None else ""} - '
                 f'{score.pp}' for i, score in enumerate(beatmap_scores.scores[:5])]))
