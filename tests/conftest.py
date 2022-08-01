from pytest import fixture

from constants import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from osu import AsynchronousClient, AuthHandler, Client, Score


@fixture(scope="session")
def async_client():
    auth = AuthHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URI)
    client = AsynchronousClient(auth)
    yield client


@fixture(scope="session")
def client():
    auth = AuthHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URI)
    client = Client(auth)
    yield client


@fixture
def sample_beatmap():
    yield {
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
            "mods": ["HD", "DT"],
            },
            {
            "accuracy": 0.9747732426303855,
            "mods": ["DT"],
            },
            {
            "accuracy": 0.9810090702947846,
            "mods": [],
            },
        ],
    }
