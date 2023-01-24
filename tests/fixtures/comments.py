from pytest import fixture


@fixture
def sample_comment():
    yield dict(
        id=29,
        message="Like this map(hard and fun to play) and song!（´∀`）ｂ",
        user_id=None,
    )
