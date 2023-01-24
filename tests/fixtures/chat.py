from pytest import fixture, mark


SAMPLE_CHANNEL = {
    "id": 5,
    "name": "#osu"
}


@fixture
def sample_channel():
    yield dict(SAMPLE_CHANNEL)


@fixture(scope="session")
def real_messages(lazer_client):
    yield lazer_client.get_channel_messages(SAMPLE_CHANNEL["id"])
