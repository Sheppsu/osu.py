from osu import KudosuHistory, Event, LegacyScore, UserBeatmapType, SoloScore


class TestUser:
    def test_get_user(self, client, sample_user):
        def check_user(user):
            assert user
            assert user.statistics
            assert user.id == sample_user["id"]
            assert user.username == sample_user["username"]
            assert user.has_supported == sample_user["has_supported"]

        check_user(client.get_user(sample_user["id"]))
        check_user(client.get_user("@" + sample_user["username"]))
        # deprecated usage
        check_user(client.get_user(sample_user["username"], key="username"))

    def test_get_users(self, client, sample_users):
        user_ids = [user["id"] for user in sample_users]
        users = sorted(client.get_users(user_ids), key=lambda u: user_ids.index(u.id))
        for user, sample_user in zip(users, sample_users):
            assert user
            assert user.id == sample_user["id"]
            assert user.username == sample_user["username"]

    def test_lookup_users(self, client, sample_users):
        users = [sample_users[0]["id"], "@" + sample_users[1]["username"]]
        users = sorted(client.lookup_users(users), key=lambda u: 0 if u.id == sample_users[0]["id"] else 1)
        for user, sample_user in zip(users, sample_users[:2]):
            assert user
            assert user.id == sample_user["id"]
            assert user.username == sample_user["username"]

    def test_get_user_kudosu(self, client):
        kudosu_list = client.get_user_kudosu(user=2)
        assert kudosu_list
        for kudosu in kudosu_list:
            assert isinstance(kudosu, KudosuHistory)
            assert kudosu.post
            assert kudosu.action

    def test_get_user_recent_activity(self, client):
        activity = client.get_user_recent_activity(user=7562902)
        for a in activity:
            assert isinstance(a, Event)
            assert getattr(a, "user", None) or getattr(a, "beatmapset", None)

    def test_get_user_scores(self, client, sample_user):
        scores = client.get_user_scores(user=sample_user["id"], type="best")
        assert scores
        for score in scores:
            assert isinstance(score, LegacyScore) or isinstance(score, SoloScore)
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

    def test_get_own_data(self, own_data):
        assert own_data
        assert own_data.id
        assert own_data.username

    def get_friends(self, user_client):
        user_client.get_friends()
