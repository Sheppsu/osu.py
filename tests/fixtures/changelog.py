from pytest_asyncio import fixture


@fixture
def sample_build():
    yield dict(stream="stable40", version="20230727.9")
