from pytest import fixture

from osu import ChatChannelType


@fixture(scope="module")
def sample_channel():
    yield dict(id=5, name="#osu", type=ChatChannelType.PUBLIC)
