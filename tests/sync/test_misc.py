from osu import WikiSearchMode, GameModeStr, RankingType


class TestMisc:
    def test_search(self, client):
        result = client.search(query="Hardrock")
        assert result.wiki_page is not None
        assert result.user is not None
        result = client.search(WikiSearchMode.USER, "BTMC")
        assert result.user is not None
        assert result.wiki_page is None
        result = client.search(WikiSearchMode.WIKI, "Hardrock")
        assert result.wiki_page is not None
        assert result.user is None

    def test_get_news_listing(self, client):
        news = client.get_news_listing(limit=5, year=2022)
        assert news
        assert news.news_posts
        assert len(news.news_posts) == 5
        for post in news.news_posts:
            assert post.published_at.year == 2022

    def test_get_news_post(self, client, sample_news_post):
        news = client.get_news_post(sample_news_post["id"], key="id")
        assert news
        assert news.id == sample_news_post["id"]
        assert news.slug == sample_news_post["slug"]
        assert news.author == sample_news_post["author"]
        assert news.title == sample_news_post["title"]

    def test_get_ranking(self, client):
        # TODO: test more parameters
        rankings = client.get_ranking(GameModeStr.STANDARD, RankingType.PERFORMANCE)
        assert rankings
        assert rankings.ranking
        assert all(map(lambda r: r.user is not None, rankings.ranking))
        client.get_ranking(GameModeStr.TAIKO, RankingType.COUNTRY)
        client.get_ranking(GameModeStr.STANDARD, RankingType.SPOTLIGHT)
        client.get_ranking(GameModeStr.STANDARD, RankingType.TEAM)

    def test_get_spotlights(self, client):
        assert client.get_spotlights()

    def test_get_wiki_page(self, client, sample_wiki_page):
        page = client.get_wiki_page(sample_wiki_page["locale"], sample_wiki_page["path"])
        assert page
        assert page.locale == sample_wiki_page["locale"]
        assert page.path == sample_wiki_page["path"]
        assert page.title == sample_wiki_page["title"]

    def test_get_matches(self, client):
        result = client.get_matches(limit=20)
        assert result
        assert len(result.matches) == 20

        result = client.get_matches(limit=25, active=True, cursor=result.cursor)
        assert result
        assert len(result.matches) == 25
        assert all((match.end_time is None for match in result.matches))

    def test_get_match(self, client, sample_match):
        match = client.get_match(sample_match["id"])
        assert match
        assert match.id == sample_match["id"]
        assert match.name == sample_match["name"]
        assert match.start_time == sample_match["start_time"]
        assert match.end_time == sample_match["end_time"]

        after_id = match.events[2].id
        match = client.get_match(sample_match["id"], limit=5, after=after_id)
        assert len(match.events) <= 5
        assert all((evt.id > after_id for evt in match.events))

        before_id = match.events[2].id
        match = client.get_match(sample_match["id"], limit=5, before=before_id)
        assert len(match.events) <= 5
        assert all((evt.id < before_id for evt in match.events))

    def test_get_seasonal_backgrounds(self, client):
        backgrounds = client.get_seasonal_backgrounds()
        assert backgrounds

    def test_get_replay_data(self, client):
        assert client.get_replay_data(GameModeStr.STANDARD, 3693301831)
        assert client.get_replay_data(None, 1267337687)
        assert client.get_replay_data(GameModeStr.STANDARD, 3693301831, False)
        assert client.get_replay_data(None, 1267337687, False)
        assert client.get_replay_data_by_id_only(1267337687)
        assert client.get_replay_data_by_id_only(1267337687, False)
