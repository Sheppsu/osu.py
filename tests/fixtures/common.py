from pytest import fixture
import asyncio

from osu import AsynchronousClient, Client
from tests.constants import CLIENT_SECRET, REDIRECT_URI, CLIENT_ID, OSU_USERNAME, OSU_PASSWORD


@fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@fixture(scope="session")
def client():
    yield Client.from_client_credentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URI)


@fixture(scope="session")
def async_client(client):
    yield AsynchronousClient(auth=client.auth)


@fixture(scope="session")
def lazer_client():
    print(OSU_USERNAME, OSU_PASSWORD)
    yield Client.from_osu_credentials(username=OSU_USERNAME, password=OSU_PASSWORD)


@fixture(scope="session")
def lazer_async_client(lazer_client):
    yield AsynchronousClient(auth=lazer_client.auth, use_lazer=True)


@fixture(scope="session")
def own_data(lazer_client):
    yield lazer_client.get_own_data()
