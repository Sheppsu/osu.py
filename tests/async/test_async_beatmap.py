import pytest

from osu import (
    BeatmapsetEventType,
    BeatmapsetSearchFilter,
    GameModeStr,
    BeatmapsetSearchStatus,
    BeatmapsetSearchExtra,
    BeatmapsetSearchSort,
    RankStatus,
    GameModeInt,
)

from tests.util import as_async


class TestAsynchronousBeatmap:
    @pytest.mark.asyncio
    async def test_get_beatmap(self, client, sample_beatmap):
        async_client = as_async(client)
        beatmap = await async_client.get_beatmap(sample_beatmap["id"])
        assert beatmap.id == sample_beatmap["id"]
        assert beatmap.beatmapset.title == sample_beatmap["title"]
        assert beatmap.beatmapset.artist == sample_beatmap["artist"]

    @pytest.mark.asyncio
    async def test_get_beatmap_attributes(self, client, sample_beatmap):
        async_client = as_async(client)
        attributes = await async_client.get_beatmap_attributes(sample_beatmap["id"])
        assert attributes.max_combo == sample_beatmap["max_combo"]
        assert attributes.type.value == sample_beatmap["type"]
        attributes = await async_client.get_beatmap_attributes(sample_beatmap["id"], ruleset=GameModeStr.TAIKO)
        assert attributes.type == GameModeStr.TAIKO
        attributes = await async_client.get_beatmap_attributes(sample_beatmap["id"], ruleset=GameModeStr.MANIA)
        assert attributes.type == GameModeStr.MANIA
        attributes = await async_client.get_beatmap_attributes(sample_beatmap["id"], ruleset=GameModeStr.CATCH)
        assert attributes.type == GameModeStr.CATCH

    @pytest.mark.asyncio
    async def test_get_beatmaps(self, client, sample_beatmaps):
        async_client = as_async(client)
        beatmaps = await async_client.get_beatmaps([beatmap["id"] for beatmap in sample_beatmaps])
        assert beatmaps
        for beatmap in beatmaps:
            keys = sample_beatmaps[0].keys()
            assert {key: getattr(beatmap, key) for key in keys} in sample_beatmaps

    @pytest.mark.asyncio
    async def test_get_beatmapset(self, client, sample_beatmapset):
        async_client = as_async(client)
        beatmapset = await async_client.get_beatmapset(sample_beatmapset["id"])
        assert beatmapset.id == sample_beatmapset["id"]
        assert beatmapset.title == sample_beatmapset["title"]
        assert beatmapset.creator == sample_beatmapset["mapper"]

    @pytest.mark.asyncio
    async def test_search_beatmapsets(self, client):
        async_client = as_async(client)
        filters = (
            BeatmapsetSearchFilter()
            .set_mode(GameModeInt.MANIA)
            .set_status(BeatmapsetSearchStatus.LOVED)
            .set_extra([BeatmapsetSearchExtra.VIDEO])
        )
        results = await async_client.search_beatmapsets(filters)
        beatmapsets = results["beatmapsets"]
        for beatmapset in beatmapsets:
            assert any([beatmap.mode == GameModeStr.MANIA for beatmap in beatmapset.beatmaps])
            assert beatmapset.status == RankStatus.LOVED
            assert beatmapset.video

        reversed_filters = filters.set_sort(BeatmapsetSearchSort.ARTIST, "asc")
        results = await async_client.search_beatmapsets(reversed_filters)

        assert results["beatmapsets"][0].id != beatmapsets[0].id

    @pytest.mark.asyncio
    async def test_get_beatmapset_discussion_posts(self, client, sample_beatmapset_discussion_post):
        async_client = as_async(client)
        data = await async_client.get_beatmapset_discussion_posts(
            beatmapset_discussion_id=sample_beatmapset_discussion_post["id"]
        )
        assert data
        assert data["posts"]
        assert len(data["beatmapsets"]) == 1
        beatmapset = data["beatmapsets"][0]
        assert beatmapset.title == sample_beatmapset_discussion_post["beatmapset_title"]
        assert beatmapset.artist == sample_beatmapset_discussion_post["beatmapset_artist"]
        target_post = None
        for post in data["posts"]:
            if (
                post.user_id == sample_beatmapset_discussion_post["target_user"]
                and post.message == sample_beatmapset_discussion_post["target_message"]
            ):
                target_post = post
        assert target_post

    @pytest.mark.asyncio
    async def test_get_beatmapset_discussion_votes(self, client, sample_beatmapset_discussion_post):
        async_client = as_async(client)
        data = await async_client.get_beatmapset_discussion_votes(sample_beatmapset_discussion_post["id"])
        assert data["votes"]
        target_vote = data["votes"][0]
        assert target_vote.beatmapset_discussion_id == sample_beatmapset_discussion_post["id"]
        assert target_vote.score == 1

    @pytest.mark.asyncio
    async def test_get_beatmapset_discussions(self, client, sample_beatmapset_discussion_post):
        async_client = as_async(client)
        ret = await async_client.get_beatmapset_discussions(
            beatmapset_id=sample_beatmapset_discussion_post["beatmapset_id"]
        )
        assert ret
        assert ret.discussions
        target_post = None
        for discussion in ret.discussions:
            if (
                discussion.starting_post.user_id == sample_beatmapset_discussion_post["discussion_user"]
                and discussion.starting_post.message == sample_beatmapset_discussion_post["discussion_message"]
            ):
                target_post = discussion.starting_post
        assert target_post

    @pytest.mark.asyncio
    async def test_lookup_beatmap(self, client, sample_beatmap):
        async_client = as_async(client)
        beatmap = await async_client.lookup_beatmap(checksum=sample_beatmap["md5_sum"])
        assert beatmap
        assert beatmap.beatmapset.title == sample_beatmap["title"]
        assert beatmap.beatmapset.artist == sample_beatmap["artist"]
        assert beatmap.id == sample_beatmap["id"]

    @pytest.mark.asyncio
    async def test_get_beatmapset_events(self, client):
        async_client = as_async(client)
        for event_type in BeatmapsetEventType:
            data = await async_client.get_beatmapset_events(type=event_type)
            assert data
            events = data["events"]
            if (
                event_type != BeatmapsetEventType.DISCUSSION_LOCK
                and event_type != BeatmapsetEventType.DISCUSSION_UNLOCK
            ):
                assert all([event.type == event_type for event in events])
