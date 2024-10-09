from osu import Client, GameModeStr
import os


client_id = int(os.getenv("CLIENT_ID"))
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = None

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

user = client.get_user(5182050)
print(user)
user = client.get_user("@dressurf", mode=GameModeStr.MANIA)
print(user)
