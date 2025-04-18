import pytest

from osu import KudosuHistory, Event, LegacyScore, UserBeatmapType, SoloScore

from tests.util import as_async


class TestAsynchronousUser:
    @pytest.mark.asyncio
    async def test_get_user(self, client, sample_user):
        async_client = as_async(client)
        def check_user(user):
            assert user
            assert user.statistics
            assert user.id == sample_user["id"]
            assert user.username == sample_user["username"]
            assert user.has_supported == sample_user["has_supported"]

        check_user(await async_client.get_user(sample_user["id"]))
        check_user(await async_client.get_user("@" + sample_user["username"]))
        # deprecated usage
        check_user(await async_client.get_user(sample_user["username"], key="username"))

    @pytest.mark.asyncio
    async def test_get_users(self, client, sample_users):
        async_client = as_async(client)
        sample_users = sorted(sample_users, key=lambda u: u["id"])
        users = await async_client.get_users([user["id"] for user in sample_users])
        for user, sample_user in zip(users, sample_users):
            assert user
            assert user.id == sample_user["id"]
            assert user.username == sample_user["username"]

    @pytest.mark.asyncio
    async def test_lookup_users(self, client, sample_users):
        async_client = as_async(client)
        users = [sample_users[0]["id"], "@" + sample_users[1]["username"]]
        users = sorted(await async_client.lookup_users(users), key=lambda u: 0 if u.id == sample_users[0]["id"] else 1)
        for user, sample_user in zip(users, sample_users[:2]):
            assert user
            assert user.id == sample_user["id"]
            assert user.username == sample_user["username"]

    @pytest.mark.asyncio
    async def test_get_user_kudosu(self, client):
        async_client = as_async(client)
        kudosu_list = await async_client.get_user_kudosu(user=2)
        assert kudosu_list
        for kudosu in kudosu_list:
            assert isinstance(kudosu, KudosuHistory)
            assert kudosu.post
            assert kudosu.action

    @pytest.mark.asyncio
    async def test_get_user_recent_activity(self, client):
        async_client = as_async(client)
        activity = await async_client.get_user_recent_activity(user=7562902)
        for a in activity:
            assert isinstance(a, Event)
            assert getattr(a, "user", None) or getattr(a, "beatmapset", None)

    @pytest.mark.asyncio
    async def test_get_user_scores(self, client, sample_user):
        async_client = as_async(client)
        scores = await async_client.get_user_scores(user=sample_user["id"], type="best")
        assert scores
        for score in scores:
            assert isinstance(score, LegacyScore) or isinstance(score, SoloScore)
            assert score.user_id == sample_user["id"]
            assert score.accuracy

    @pytest.mark.asyncio
    async def test_get_user_beatmaps(self, client, sample_user_beatmaps):
        async_client = as_async(client)
        beatmaps = await async_client.get_user_beatmaps(
            user=sample_user_beatmaps["user_id"],
            type=UserBeatmapType.GRAVEYARD,
        )
        assert beatmaps
        target_beatmap = beatmaps[0]
        expected_beatmap = sample_user_beatmaps["beatmapset"]
        assert target_beatmap.artist == expected_beatmap["artist"]
        assert target_beatmap.title == expected_beatmap["title"]
        assert target_beatmap.creator == expected_beatmap["creator"]

    @pytest.mark.asyncio
    async def test_get_own_data(self, user_client):
        async_user_client = as_async(user_client)
        me = await async_user_client.get_own_data()
        assert me
        assert me.id
        assert me.username

    @pytest.mark.asyncio
    async def test_get_friends(self, user_client):
        async_user_client = as_async(user_client)
        await async_user_client.get_friends()
