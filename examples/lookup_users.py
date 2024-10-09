from osu import Client, GameModeStr
import os


client_id = int(os.getenv("CLIENT_ID"))
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = None

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

users = client.lookup_users([14895608, "@mrekk"])
print(users)
