import json
import os
from osu import Client, AuthHandler, Scope


def get_user_client():
    def save(auth):
        with open("auth.json", "w") as f:
            json.dump(auth.get_save_data(), f)

    if not os.path.exists("auth.json"):
        with open("auth.json", "w") as f:
            f.write("{}")

    with open("auth.json", "r") as f:
        auth_data = json.load(f)

    if auth_data:
        print("Loading auth from save data.")
        client = Client(AuthHandler.from_save_data(auth_data))
    else:
        print("No auth data found. Creating auth from scratch.")
        client_id = int(os.getenv('CLIENT_ID'))
        client_secret = os.getenv('CLIENT_SECRET')
        redirect_url = "http://127.0.0.1:8080"

        auth = AuthHandler(client_id, client_secret, redirect_url, Scope.identify())
        auth.get_auth_token(input(f"Get the code from authorizing with this url\n{auth.get_auth_url()}\nCode: "))
        client = Client(auth)

    save(client.auth)
    client.auth.set_refresh_callback(save)  # auto save auth data
    return client
