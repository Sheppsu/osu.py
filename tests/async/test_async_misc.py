import pytest

from osu import WikiSearchMode, GameModeStr, RankingType

from tests.util import as_async


class TestAsynchronousMisc:
    @pytest.mark.asyncio
    async def test_search(self, client):
        async_client = as_async(client)
        result = await async_client.search(query="Hardrock")
        assert result.wiki_page is not None
        assert result.user is not None
        result = await async_client.search(WikiSearchMode.USER, "BTMC")
        assert result.user is not None
        assert result.wiki_page is None
        result = await async_client.search(WikiSearchMode.WIKI, "Hardrock")
        assert result.wiki_page is not None
        assert result.user is None

    @pytest.mark.asyncio
    async def test_get_news_listing(self, client):
        async_client = as_async(client)
        news = await async_client.get_news_listing(limit=5)
        assert news
        assert len(news["news_posts"]) == 5

    @pytest.mark.asyncio
    async def test_get_news_post(self, client, sample_news_post):
        async_client = as_async(client)
        news = await async_client.get_news_post(sample_news_post["id"], "id")
        assert news
        assert news.id == sample_news_post["id"]
        assert news.slug == sample_news_post["slug"]
        assert news.author == sample_news_post["author"]
        assert news.title == sample_news_post["title"]

    @pytest.mark.asyncio
    async def test_get_ranking(self, client):
        async_client = as_async(client)
        rankings = await async_client.get_ranking(GameModeStr.STANDARD, RankingType.PERFORMANCE)
        assert rankings
        assert rankings.ranking
        assert all(map(lambda r: r.user is not None, rankings.ranking))
        await async_client.get_ranking(GameModeStr.TAIKO, RankingType.COUNTRY)
        await async_client.get_ranking(GameModeStr.STANDARD, RankingType.SPOTLIGHT)
        await async_client.get_ranking(GameModeStr.STANDARD, RankingType.TEAM)

    @pytest.mark.asyncio
    async def test_get_spotlights(self, client):
        async_client = as_async(client)
        assert await async_client.get_spotlights()

    @pytest.mark.asyncio
    async def test_get_wiki_page(self, client, sample_wiki_page):
        async_client = as_async(client)
        page = await async_client.get_wiki_page(sample_wiki_page["locale"], sample_wiki_page["path"])
        assert page
        assert page.locale == sample_wiki_page["locale"]
        assert page.path == sample_wiki_page["path"]
        assert page.title == sample_wiki_page["title"]

    @pytest.mark.asyncio
    async def test_get_matches(self, client):
        async_client = as_async(client)
        matches = await async_client.get_matches(limit=5)
        assert matches
        assert len(matches["matches"]) == 5

    @pytest.mark.asyncio
    async def test_get_match(self, client, sample_match):
        async_client = as_async(client)
        match = await async_client.get_match(sample_match["id"])
        assert match
        assert match.id == sample_match["id"]
        assert match.name == sample_match["name"]
        assert match.start_time == sample_match["start_time"]
        assert match.end_time == sample_match["end_time"]

        after_id = match.events[2].id
        match = await async_client.get_match(sample_match["id"], limit=5, after=after_id)
        assert len(match.events) <= 5
        assert all((evt.id > after_id for evt in match.events))

        before_id = match.events[2].id
        match = await async_client.get_match(sample_match["id"], limit=5, before=before_id)
        assert len(match.events) <= 5
        assert all((evt.id < before_id for evt in match.events))

    @pytest.mark.asyncio
    async def test_get_seasonal_backgrounds(self, client):
        async_client = as_async(client)
        backgrounds = await async_client.get_seasonal_backgrounds()
        assert backgrounds

    @pytest.mark.asyncio
    async def test_get_replay_data(self, client):
        async_client = as_async(client)
        assert await async_client.get_replay_data(GameModeStr.STANDARD, 3693301831)
        assert await async_client.get_replay_data(None, 1267337687)
        assert await async_client.get_replay_data(GameModeStr.STANDARD, 3693301831, False)
        assert await async_client.get_replay_data(None, 1267337687, False)
        assert await async_client.get_replay_data_by_id_only(1267337687)
        assert await async_client.get_replay_data_by_id_only(1267337687, False)
