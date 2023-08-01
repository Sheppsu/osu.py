from pytest import fixture


@fixture
def sample_user_highscore():
    yield dict(
        room_id=239531,
        playlist_id=1434674,
        score_id=3960115,
        user_id=20198397,
    )
