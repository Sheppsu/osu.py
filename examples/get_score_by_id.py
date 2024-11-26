from osu import Client
import os


client = Client.from_credentials(int(os.getenv("CLIENT_ID")), os.getenv("CLIENT_SECRET"), None)
score = client.get_score_by_id_only(2843952435)
print(score)
