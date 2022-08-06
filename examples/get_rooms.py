from osu import Client, AuthHandler, Scope
import os
import json


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

auth = AuthHandler(client_id, client_secret, redirect_url, Scope.identify())
print(auth.get_auth_url())
auth.get_auth_token(input("Code: "))
client = Client(auth)

print(client.get_rooms())
