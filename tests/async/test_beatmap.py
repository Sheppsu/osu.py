import pytest


class TestBeatmap:
    @pytest.mark.asyncio
    async def test_get_beatmap(self, async_client, sample_beatmap):
        beatmap = await async_client.get_beatmap(sample_beatmap["id"])
        assert beatmap.id == sample_beatmap["id"]
        assert beatmap.beatmapset.title == sample_beatmap["title"]
        assert beatmap.beatmapset.artist == sample_beatmap["artist"]

    @pytest.mark.asyncio
    async def test_get_beatmap_attributes(self, async_client, sample_beatmap):
        attributes = await async_client.get_beatmap_attributes(sample_beatmap["id"])
        assert attributes.max_combo == sample_beatmap["max_combo"]
        assert attributes.type == sample_beatmap["type"]

    @pytest.mark.asyncio
    async def test_get_beatmaps(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_get_beatmap_scores(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_get_user_beatmap_score(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_get_user_beatmap_scores(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_get_user_beatmaps(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_search_beatmapsets(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_get_beatmapset_discussion_posts(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_get_beatmapset_discussion_votes(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_get_beatmapset_discussions(self, async_client):
        ...

    @pytest.mark.asyncio
    async def test_lookup_beatmap(self, async_client):
        ...
