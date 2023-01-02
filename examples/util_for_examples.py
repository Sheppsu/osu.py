import json
import os
from osu import Client, AuthHandler, Scope


def get_user_client():
    def save(auth):
        with open("auth.json", "w") as f:
            json.dump(auth.get_save_data(), f)

    with open("auth.json", "r") as f:
        auth_data = json.load(f)

    if auth_data:
        print("Loading auth from save data.")
        client = Client(AuthHandler.from_save_data(auth_data))
    else:
        print("No auth data found. Creating auth from scratch.")
        client_id = int(os.getenv('osu_client_id'))
        client_secret = os.getenv('osu_client_secret')
        redirect_url = "http://127.0.0.1:8080"

        auth = AuthHandler(client_id, client_secret, redirect_url, Scope.identify())
        print(auth.get_auth_url())
        auth.get_auth_token(input("Code: "))
        client = Client(auth)

    save(client.auth)
    client.auth.set_refresh_callback(save)  # auto save auth data
    return client


def get_lazer_client():
    with open(".env", "r") as f:
        env = f.readlines()
        env = dict(map(lambda k: k.replace("\n", "").split("="), env))

    return Client.from_osu_credentials(env["OSU_USERNAME"], env["OSU_PASSWORD"])
