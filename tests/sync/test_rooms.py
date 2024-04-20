from osu import RoomType


class TestRooms:
    def test_get_scores(self, user_client, sample_user_highscore):
        user_client.get_scores(sample_user_highscore["room_id"], sample_user_highscore["playlist_id"])

    def test_get_rooms(self, user_client):
        # TODO: test more parameters
        rooms = user_client.get_rooms(sort=RoomType.PLAYLISTS, limit=5)
        assert len(rooms) == 5
        assert all(map(lambda room: room.type == RoomType.PLAYLISTS, rooms))

    def test_get_room(self, client, sample_user_highscore):
        room = client.get_room(sample_user_highscore["room_id"])
        assert room.id == sample_user_highscore["room_id"]

    def test_get_room_leaderboard(self, user_client, sample_user_highscore):
        ret = user_client.get_room_leaderboard(sample_user_highscore["room_id"])
        scores = ret.leaderboard
        assert scores
        assert all(map(lambda score: score.room_id == sample_user_highscore["room_id"], scores))
        assert any(map(lambda score: score.user_id == sample_user_highscore["user_id"], scores))
