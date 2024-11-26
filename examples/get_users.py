from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_credentials(client_id, client_secret, redirect_url)

user_ids = [7562902, 11443437, 3717598, 1473890, 4230827]
mode = 'osu'
users = client.get_users(user_ids)
for user in users:
    print(user)
