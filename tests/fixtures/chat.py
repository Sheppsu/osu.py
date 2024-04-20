from pytest import fixture


SAMPLE_CHANNEL = {"id": 5, "name": "#osu"}


@fixture
def sample_channel():
    yield dict(SAMPLE_CHANNEL)
