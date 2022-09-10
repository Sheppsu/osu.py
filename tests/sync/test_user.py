from osu import KudosuHistory, Event, LegacyScore, UserBeatmapType


class TestUser:
    def test_get_user(self, client, sample_user):
        user = client.get_user(6943941)
        assert user
        assert user.statistics
        assert user.id == sample_user["id"]
        assert user.username == sample_user["username"]
        assert user.has_supported == sample_user["has_supported"]

    def test_get_users(self, client, sample_users):
        # Requires lazer scope
        ...

    def test_get_user_highscore(self, client, sample_room):
        # Requires lazer scope
        ...

    def test_get_user_kudosu(self, client):
        kudosu_list = client.get_user_kudosu(user=2)
        assert kudosu_list
        for kudosu in kudosu_list:
            assert isinstance(kudosu, KudosuHistory)
            assert kudosu.post
            assert kudosu.action

    def test_get_user_recent_activity(self, client):
        activity = client.get_user_recent_activity(user=2)
        assert activity
        for a in activity:
            assert isinstance(a, Event)
            assert getattr(a, "user", None) or getattr(a, "beatmapset", None)

    def test_get_user_scores(self, client, sample_user):
        scores = client.get_user_scores(user=sample_user["id"], type="best")
        assert scores
        for score in scores:
            assert isinstance(score, LegacyScore)
            assert score.user_id == sample_user["id"]
            assert score.accuracy

    def test_get_user_beatmaps(self, client, sample_user_beatmaps):
        beatmaps = client.get_user_beatmaps(
            user=sample_user_beatmaps["user_id"],
            type=UserBeatmapType.GRAVEYARD,
        )
        assert beatmaps
        target_beatmap = beatmaps[0]
        expected_beatmap = sample_user_beatmaps["beatmapset"]
        assert target_beatmap.artist == expected_beatmap["artist"]
        assert target_beatmap.title == expected_beatmap["title"]
        assert target_beatmap.creator == expected_beatmap["creator"]
