from pytest_asyncio import fixture

from osu import Mod, GameModeStr


@fixture
def sample_beatmap_scores():
    yield dict(
        beatmap_id=741477,
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
        scores=list(
            [
                dict(
                    accuracy=0.9725056689342404,
                    mods=[Mod.Hidden, Mod.DoubleTime, Mod.Classic],
                ),
                dict(
                    accuracy=0.9747732426303855,
                    mods=[Mod.DoubleTime, Mod.Classic],
                ),
                dict(
                    accuracy=0.9810090702947846,
                    mods=[Mod.Classic],
                ),
            ]
        ),
    )


@fixture
def sample_scores():
    yield list(
        [
            dict(
                id=1267337687,
                mode=GameModeStr.STANDARD,
                user_id=7562902,
                accuracy=1,
                mods=[Mod.Hidden, Mod.HardRock, Mod.DoubleTime, Mod.Classic],
            ),
            dict(
                id=1496013792,
                mode=GameModeStr.STANDARD,
                user_id=124493,
                accuracy=0.9983190452176837,
                mods=[Mod.Hidden, Mod.HardRock, Mod.Classic],
            ),
            dict(
                id=786148462,
                mode=GameModeStr.STANDARD,
                user_id=4650315,
                accuracy=0.9928113767776215,
                mods=[Mod.HardRock, Mod.Classic],
            ),
        ]
    )
