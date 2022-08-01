import pytest


class TestBeatmap:
    @pytest.mark.asyncio
    async def test_async_get_beatmap(self, async_client, sample_beatmap):
        beatmap = await async_client.get_beatmap(sample_beatmap["id"])
        assert beatmap.id == sample_beatmap["id"]
        assert beatmap.beatmapset.title == sample_beatmap["title"]
        assert beatmap.beatmapset.artist == sample_beatmap["artist"]

    @pytest.mark.asyncio
    async def test_async_get_beatmap_attributes(self, async_client, sample_beatmap):
        attributes = await async_client.get_beatmap_attributes(sample_beatmap["id"])
        assert attributes.max_combo == sample_beatmap["max_combo"]
        assert attributes.type == sample_beatmap["type"]

    @pytest.mark.asyncio
    async def test_async_get_beatmaps(self, async_client, sample_beatmaps):
        beatmaps = await async_client.get_beatmaps([beatmap["id"] for beatmap in sample_beatmaps])
        assert beatmaps
        for beatmap in beatmaps:
            keys = sample_beatmaps[0].keys()
            assert {key: getattr(beatmap, key) for key in keys} in sample_beatmaps

    @pytest.mark.asyncio
    async def test_async_get_beatmap_scores(self, async_client, sample_scores):
        scores = await async_client.get_beatmap_scores(sample_scores["beatmap_id"])
        for received_score, sample_score in zip(scores.scores[:3], sample_scores["scores"]):
            assert received_score.id == sample_score["id"]
            assert received_score.user_id == sample_score["user_id"]
            assert received_score.max_combo == sample_score["max_combo"]

    @pytest.mark.asyncio
    async def test_async_get_user_beatmap_score(self, async_client, sample_user_beatmap_score):
        score = (await async_client.get_user_beatmap_score(
            beatmap=sample_user_beatmap_score["beatmap_id"],
            user=sample_user_beatmap_score["user_id"],
        )).score
        assert score
        assert score.user_id == sample_user_beatmap_score["user_id"]
        assert score.accuracy == sample_user_beatmap_score["accuracy"]

    @pytest.mark.asyncio
    async def test_async_get_user_beatmap_scores(self, async_client, sample_user_beatmap_scores):
        scores = await async_client.get_user_beatmap_scores(
            beatmap=sample_user_beatmap_scores["beatmap_id"],
            user=sample_user_beatmap_scores["user_id"],
        )
        assert scores
        for score in scores:
            keys = sample_user_beatmap_scores["scores"][0].keys()
            assert {key: getattr(score, key) for key in keys} in sample_user_beatmap_scores["scores"]

    @pytest.mark.asyncio
    async def test_async_get_user_beatmaps(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_async_search_beatmapsets(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_async_get_beatmapset_discussion_posts(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_async_get_beatmapset_discussion_votes(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_async_get_beatmapset_discussions(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_async_lookup_beatmap(self, async_client):
        ...
