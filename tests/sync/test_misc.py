from osu import WikiSearchMode, GameModeStr, RankingType


class TestMisc:
    def test_get_updates(self, lazer_client):
        lazer_client.get_updates(0)

    def test_search(self, client):
        result = client.search(WikiSearchMode.WIKI, "Hardrock")
        assert result["wiki_page"]
        assert result['wiki_page'].results

    def test_get_news_listing(self, client):
        news = client.get_news_listing(limit=5)
        assert news
        assert len(news["news_posts"]) == 5

    def test_get_news_post(self, client, sample_news_post):
        news = client.get_news_post(sample_news_post["id"], "id")
        assert news
        assert news.id == sample_news_post["id"]
        assert news.slug == sample_news_post["slug"]
        assert news.author == sample_news_post["author"]
        assert news.title == sample_news_post["title"]

    def test_get_notifications(self, lazer_client):
        lazer_client.get_notifications()

    def test_mark_notifications_as_read(self, lazer_client):
        # can't really implement
        pass

    def test_get_ranking(self, client):
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
        assert len(matches["matches"]) == 5

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
        lazer_client.check_download_quota()
