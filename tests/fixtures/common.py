from pytest import fixture

from osu import AsynchronousClient, AuthHandler, Client
from tests.constants import CLIENT_SECRET, REDIRECT_URI, CLIENT_ID


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
