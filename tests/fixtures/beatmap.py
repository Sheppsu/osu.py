from pytest_asyncio import fixture

from osu import UserBeatmapType, Mods


@fixture
def sample_beatmap():
    yield {
        "md5_sum": "8d351b3db141b2aa426d992374e80b24",
        "id": 2063622,
        "artist": "Loki",
        "title": "Wizard's Tower",
        "type": "osu",
        "max_combo": 866,
    }


@fixture
def sample_beatmaps():
    yield [
        {
            "id": 2063622,
            "max_combo": 866,
            "beatmapset_id": 985788,
            "ar": 9,
        },
        {
            "id": 1031991,
            "max_combo": 4353,
            "beatmapset_id": 461744,
            "ar": 10,
        },
        {
            "id": 252238,
            "max_combo": 2646,
            "beatmapset_id": 93523,
            "ar": 10,
        }
    ]


@fixture
def sample_scores():
    yield {
        "beatmap_id": 741477,
        "scores": [
            {
                "id": 2046025260,
                "user_id": 214187,
                "max_combo": 197,
            },
            {
                "id": 2157887005,
                "user_id": 6143840,
                "max_combo": 197,
            },
            {
                "id": 2427781720,
                "user_id": 7162035,
                "max_combo": 197,
            },
        ]
    }


@fixture
def sample_user_beatmap_score():
    yield {
        "user_id": 6943941,
        "accuracy": 0.9725056689342404,
        "beatmap_id": 2063622,
    }


@fixture
def sample_user_beatmap_scores():
    yield {
        "user_id": 6943941,
        "beatmap_id": 2063622,
        "scores": [
            {
                "accuracy": 0.9725056689342404,
                "mods": Mods.Hidden | Mods.DoubleTime,
            },
            {
                "accuracy": 0.9747732426303855,
                "mods": Mods.DoubleTime,
            },
            {
                "accuracy": 0.9810090702947846,
                "mods": None,
            },
        ],
    }


@fixture
def sample_user_beatmaps():
    yield dict(
        user_id=6943941,
        type=UserBeatmapType.GRAVEYARD,
        beatmapset=dict(
            artist="Fractal Dreamers",
            title="Gardens Under A Spring Sky",
            creator="nouvelle",
        ),
    )


@fixture
def sample_beatmapset_discussion_post():
    yield dict(
        id=1457454,
        beatmapset_id=632972,
        beatmapset_title="put' l'da",
        beatmapset_artist="Camellia",
        target_message="2 > 3.5 > 5 if I'm going to change it, I still want the lower diffs "
                       "to be more forgiving considering their difficulty isn't well represented with SR",
        target_user=4116573,
        discussion_user=6175280,
        discussion_message="HP settings are quite low for Advanced-Insane. Would go for HP3 - HP4 - HP5",
    )


@fixture
def sample_beatmapset_discussion():
    yield dict(
        beatmap_id=632972,
    )
