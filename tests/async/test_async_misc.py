import pytest

from osu import WikiSearchMode, GameModeStr, RankingType


class TestAsynchronousMisc:
    @pytest.mark.asyncio
    async def test_get_updates(self, lazer_async_client):
        await lazer_async_client.get_updates(0)

    @pytest.mark.asyncio
    async def test_search(self, async_client):
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
    async def test_get_news_listing(self, async_client):
        news = await async_client.get_news_listing(limit=5)
        assert news
        assert len(news["news_posts"]) == 5

    @pytest.mark.asyncio
    async def test_get_news_post(self, async_client, sample_news_post):
        news = await async_client.get_news_post(sample_news_post["id"], "id")
        assert news
        assert news.id == sample_news_post["id"]
        assert news.slug == sample_news_post["slug"]
        assert news.author == sample_news_post["author"]
        assert news.title == sample_news_post["title"]

    @pytest.mark.asyncio
    async def test_get_notifications(self, lazer_async_client):
        await lazer_async_client.get_notifications()

    @pytest.mark.asyncio
    async def test_mark_notifications_as_read(self, lazer_async_client):
        # can't really implement
        pass

    @pytest.mark.asyncio
    async def test_get_ranking(self, async_client):
        rankings = await async_client.get_ranking(GameModeStr.STANDARD, RankingType.PERFORMANCE)
        assert rankings
        assert rankings.ranking
        assert all(map(lambda r: r.user is not None, rankings.ranking))

    @pytest.mark.asyncio
    async def test_get_spotlights(self, async_client):
        assert await async_client.get_spotlights()

    @pytest.mark.asyncio
    async def test_get_wiki_page(self, async_client, sample_wiki_page):
        page = await async_client.get_wiki_page(sample_wiki_page["locale"], sample_wiki_page["path"])
        assert page
        assert page.locale == sample_wiki_page["locale"]
        assert page.path == sample_wiki_page["path"]
        assert page.title == sample_wiki_page["title"]

    @pytest.mark.asyncio
    async def test_get_matches(self, async_client):
        matches = await async_client.get_matches(limit=5)
        assert matches
        assert len(matches["matches"]) == 5

    @pytest.mark.asyncio
    async def test_get_match(self, async_client, sample_match):
        match = await async_client.get_match(sample_match["id"])
        assert match
        assert match.id == sample_match["id"]
        assert match.name == sample_match["name"]
        assert match.start_time == sample_match["start_time"]
        assert match.end_time == sample_match["end_time"]

    @pytest.mark.asyncio
    async def test_get_seasonal_backgrounds(self, async_client):
        backgrounds = await async_client.get_seasonal_backgrounds()
        assert backgrounds

    @pytest.mark.asyncio
    async def test_get_replay_data(self, lazer_async_client):
        replay_data = await lazer_async_client.get_replay_data(GameModeStr.STANDARD, 3693301831)
        assert replay_data

    @pytest.mark.asyncio
    async def test_send_report(self, lazer_async_client):
        # I will not implement this for obvious reasons lol
        pass

    @pytest.mark.asyncio
    async def test_check_download_quota(self, lazer_async_client):
        assert await lazer_async_client.check_download_quota() is not None

    @pytest.mark.asyncio
    async def test_get_topic_and_posts(self, async_client, sample_topic):
        ret = await async_client.get_topic_and_posts(1699086)
        assert ret.topic
        assert ret.topic.id == sample_topic["id"]
        assert ret.topic.title == sample_topic["title"]
        assert ret.posts
