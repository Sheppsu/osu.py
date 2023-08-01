from osu import Client
import os


client_id = int(os.getenv("CLIENT_ID"))
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = None

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

user_id = 5182050
mode = 'osu'
user = client.get_user(user_id, mode)
print(user)
