from osu import WikiSearchMode, GameModeStr, RankingType


class TestMisc:
    def test_get_updates(self, lazer_client):
        lazer_client.get_updates(0)

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

    def test_get_notifications(self, lazer_client):
        ret = lazer_client.get_notifications()
        assert ret

    def test_mark_notifications_as_read(self, lazer_client):
        # can't really implement
        pass

    def test_get_ranking(self, client):
        # TODO: test more parameters
        rankings = client.get_ranking(GameModeStr.STANDARD, RankingType.PERFORMANCE)
        assert rankings
        assert rankings.ranking
        assert all(map(lambda r: r.user is not None, rankings.ranking))

    def test_get_spotlights(self, client):
        assert client.get_spotlights()

    def test_get_wiki_page(self, client, sample_wiki_page):
        page = client.get_wiki_page(sample_wiki_page["locale"], sample_wiki_page["path"])
        assert page
        assert page.locale == sample_wiki_page["locale"]
        assert page.path == sample_wiki_page["path"]
        assert page.title == sample_wiki_page["title"]

    def test_get_matches(self, client):
        matches = client.get_matches(limit=5)
        assert matches
        assert len(matches.matches) == 5

    def test_get_match(self, client, sample_match):
        match = client.get_match(sample_match["id"])
        assert match
        assert match.id == sample_match["id"]
        assert match.name == sample_match["name"]
        assert match.start_time == sample_match["start_time"]
        assert match.end_time == sample_match["end_time"]

    def test_get_seasonal_backgrounds(self, client):
        backgrounds = client.get_seasonal_backgrounds()
        assert backgrounds

    def test_get_replay_data(self, lazer_client):
        replay_data = lazer_client.get_replay_data(GameModeStr.STANDARD, 3693301831)
        assert replay_data

    def test_send_report(self, lazer_client):
        # I will not implement this for obvious reasons lol
        pass

    def test_check_download_quota(self, lazer_client):
        assert lazer_client.check_download_quota() is not None

    def test_get_topic_and_posts(self, client, sample_topic):
        ret = client.get_topic_and_posts(1699086)
        assert ret.topic
        assert ret.topic.id == sample_topic["id"]
        assert ret.topic.title == sample_topic["title"]
        assert ret.posts
