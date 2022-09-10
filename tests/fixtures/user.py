from pytest import fixture


@fixture
def sample_user():
    yield dict(
        id=6943941,
        username="nouvelle",
        has_supported=True,
    )


@fixture
def sample_users():
    yield [
        dict(
            id=6943941,
            username="nouvelle",
            has_supported=True,
        ),
        dict(
            id=2,
            username="peppy",
            has_supported=True,
        ),
        dict(
            id=14895608,
            username="SheeppOSU",
            has_supported=True,
        ),
    ]


@fixture
def sample_room():
    yield dict(
        id=213518,
        user_id=8116659,
    )
