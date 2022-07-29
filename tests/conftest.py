from pytest import fixture

from constants import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from osu import AsynchronousClient, AuthHandler, Client


@fixture(scope="session")
def async_client():
    auth = AuthHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URI)
    client = AsynchronousClient(auth)
    yield client


@fixture(scope="session")
def client():
    auth = AuthHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URI)
    client = Client(auth)
    yield client


@fixture
def sample_beatmap():
    yield {
        "id": 2063622,
        "artist": "Loki",
        "title": "Wizard's Tower",
        "type": "osu",
        "max_combo": 866,
    }
