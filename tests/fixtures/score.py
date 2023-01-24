from pytest_asyncio import fixture

from osu import Mods, GameModeStr


@fixture
def sample_beatmap_scores():
    yield dict(
        beatmap_id=741477,
        scores=list([
            dict(
                id=2046025260,
                user_id=214187,
                max_combo=197,
            ),
            dict(
                id=2157887005,
                user_id=6143840,
                max_combo=197,
            ),
            dict(
                id=2427781720,
                user_id=7162035,
                max_combo=197,
            ),
        ])
    )


@fixture
def sample_user_beatmap_score():
    yield dict(
        user_id=6943941,
        accuracy=0.9725056689342404,
        beatmap_id=2063622,
    )


@fixture
def sample_user_beatmap_scores():
    yield dict(
        user_id=6943941,
        beatmap_id=2063622,
        scores=list([
            dict(
                accuracy=0.9725056689342404,
                mods=Mods.Hidden | Mods.DoubleTime,
            ),
            dict(
                accuracy=0.9747732426303855,
                mods=Mods.DoubleTime,
            ),
            dict(
                accuracy=0.9810090702947846,
                mods=None,
            ),
        ]),
    )


@fixture
def sample_scores():
    yield list([
        dict(
            id=3693301831,
            mode=GameModeStr.STANDARD,
            user_id=7562902,
            accuracy=1,
            mods=Mods.Hidden | Mods.HardRock | Mods.DoubleTime,
            score=4988391,
        ),
        dict(
            id=2177560145,
            mode=GameModeStr.STANDARD,
            user_id=124493,
            accuracy=0.9983190452176837,
            mods=Mods.Hidden | Mods.HardRock,
            score=132408001,
        ),
        dict(
            id=2847567607,
            mode=GameModeStr.STANDARD,
            user_id=4650315,
            accuracy=0.9928113767776215,
            mods=Mods.HardRock,
            score=182745963,
        )
    ])
