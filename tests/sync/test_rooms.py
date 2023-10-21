from osu import RoomType


class TestRooms:
    def test_get_user_highscore(self, lazer_client, sample_user_highscore):
        highscore = lazer_client.get_user_highscore(
            sample_user_highscore["room_id"], sample_user_highscore["playlist_id"], sample_user_highscore["user_id"]
        )
        assert highscore
        assert highscore.user
        assert highscore.user.id == sample_user_highscore["user_id"]
        assert highscore.id == sample_user_highscore["score_id"]

    def test_get_scores(self, lazer_client, sample_user_highscore):
        scores = lazer_client.get_scores(sample_user_highscore["room_id"], sample_user_highscore["playlist_id"])
        assert any(map(lambda score: score.user_id == sample_user_highscore["user_id"], scores.scores))

    def test_get_rooms(self, lazer_client):
        # TODO: test more parameters
        rooms = lazer_client.get_rooms(sort=RoomType.PLAYLISTS, limit=5)
        assert len(rooms) == 5
        assert all(map(lambda room: room.type == RoomType.PLAYLISTS, rooms))

    def test_get_room(self, client, sample_user_highscore):
        room = client.get_room(sample_user_highscore["room_id"])
        assert room.id == sample_user_highscore["room_id"]

    def test_get_room_leaderboard(self, lazer_client, sample_user_highscore):
        ret = lazer_client.get_room_leaderboard(sample_user_highscore["room_id"])
        scores = ret.leaderboard
        assert scores
        assert all(map(lambda score: score.room_id == sample_user_highscore["room_id"], scores))
        assert any(map(lambda score: score.user_id == sample_user_highscore["user_id"], scores))

    def test_join_to_room(self, lazer_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    def test_kick_from_room(self, lazer_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    def test_create_room(self, lazer_client):
        # I can implement this cuz the room just like disappears
        # when no one joins, but maybe later
        pass
