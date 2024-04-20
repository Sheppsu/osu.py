from pytest import fixture, mark
import asyncio
import json
import os

from osu import AsynchronousClient, Client, AuthHandler, AsynchronousAuthHandler, Scope
from tests.constants import CLIENT_SECRET, REDIRECT_URI, CLIENT_ID


@fixture(scope="session")
def event_loop():
    yield asyncio.get_event_loop()


@fixture(scope="session")
def client():
    yield Client.from_client_credentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URI)


@fixture(scope="session")
def async_client(client):
    def update(auth):
        client.http.auth = auth.as_sync()  # update auth

    auth = client.auth.as_async()
    auth.set_refresh_callback(update)
    yield AsynchronousClient(auth)


def get_user_client():
    def save(auth):
        with open("auth.json", "w") as f:
            json.dump(auth.get_save_data(), f)

    if not os.path.exists("auth.json"):
        raise RuntimeError("Run auth.py to populate auth.json")

    with open("auth.json", "r") as f:
        auth_data = json.load(f)
        if not auth_data:
            raise RuntimeError("Run auth.py to populate auth.json")

    client = Client(AuthHandler.from_save_data(auth_data))
    save(client.auth)
    client.auth.set_refresh_callback(save)  # auto save auth data
    return client


@fixture(scope="session")
def user_client():
    yield get_user_client()


@fixture(scope="session")
def async_user_client(user_client):
    def update(auth):
        refresh_callback = user_client.http.auth._refresh_callback
        user_client.http.auth = auth.as_sync()  # update auth
        user_client.http.auth._refresh_callback = refresh_callback
        refresh_callback(user_client.http.auth)  # since the auth data was just updated

    auth = user_client.auth.as_async()
    auth.set_refresh_callback(update)
    yield AsynchronousClient(auth)


@fixture(scope="session")
def own_data(user_client):
    yield user_client.get_own_data()
