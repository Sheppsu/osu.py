from pytest import fixture
import asyncio
import json
import os

from osu import AsynchronousClient, Client, AuthHandler
from tests.constants import CLIENT_SECRET, REDIRECT_URI, CLIENT_ID


@fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@fixture(scope="session")
def client() -> Client:
    return Client.from_credentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URI)


@fixture(scope="function")
def async_client(client) -> AsynchronousClient:
    def update(auth):
        client.auth = auth.as_sync()  # update auth

    auth = client.auth.as_async()
    auth.set_refresh_callback(update)
    return AsynchronousClient(auth)


def get_user_client(dev=False) -> Client:
    file = "auth.json" if not dev else "dev-auth.json"

    def save(auth):
        with open(file, "w") as f:
            json.dump(auth.get_save_data(), f)

    if not os.path.exists(file):
        raise RuntimeError(f"Run auth.py to populate {file}")

    with open(file, "r") as f:
        auth_data = json.load(f)
        if not auth_data:
            raise RuntimeError(f"Run auth.py to populate {file}")

    client = Client(AuthHandler.from_save_data(auth_data))
    save(client.auth)
    client.auth.set_refresh_callback(save)  # auto save auth data
    return client


@fixture(scope="session")
def user_client() -> Client:
    return get_user_client()


@fixture(scope="function")
def async_user_client(user_client) -> AsynchronousClient:
    def update(auth):
        user_client.auth = auth.as_sync()  # update auth
        user_client.auth._refresh_callback(user_client.auth)  # since the auth data was just updated

    auth = user_client.auth.as_async()
    auth.set_refresh_callback(update)
    return AsynchronousClient(auth)


@fixture(scope="session")
def dev_user_client(async_user_client) -> Client:
    yield get_user_client(dev=True)


@fixture(scope="function")
def dev_async_user_client(dev_user_client) -> AsynchronousClient:
    def update(auth):
        dev_user_client.auth = auth.as_sync()  # update auth
        dev_user_client.auth._refresh_callback(dev_user_client.auth)  # since the auth data was just updated

    auth = dev_user_client.auth.as_async()
    auth.set_refresh_callback(update)
    return AsynchronousClient(auth)


@fixture(scope="session")
def own_data(user_client):
    yield user_client.get_own_data()


@fixture(scope="session")
def dev_own_data(dev_user_client):
    yield dev_user_client.get_own_data()
