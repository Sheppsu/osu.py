from pytest import fixture


@fixture
def sample_topic():
    yield dict(id=1699086, title="[STD] Roundtable II Qualifier Tournament | [Registrations closed]")


@fixture
def sample_forum():
    yield dict(
        id=55,
        name="Tournaments",
        description="Get involved in community tournaments for some friendly or fierce competition!",
    )
