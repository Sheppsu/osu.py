import pytest

from osu import RoomType


class TestAsynchronousRooms:
    @pytest.mark.asyncio
    async def test_get_user_highscore(self, lazer_async_client, sample_user_highscore):
        highscore = await lazer_async_client.get_user_highscore(
            sample_user_highscore["room_id"], sample_user_highscore["playlist_id"],
            sample_user_highscore["user_id"])
        assert highscore
        assert highscore.user
        assert highscore.user.id == sample_user_highscore["user_id"]
        assert highscore.id == sample_user_highscore["score_id"]

    @pytest.mark.asyncio
    async def test_get_scores(self, lazer_async_client, sample_user_highscore):
        scores = await lazer_async_client.get_scores(
            sample_user_highscore["room_id"], sample_user_highscore["playlist_id"])
        assert any(map(lambda score: score.user_id == sample_user_highscore["user_id"], scores.scores))

    @pytest.mark.asyncio
    async def test_get_score(self, lazer_async_client, sample_user_highscore):
        score = await lazer_async_client.get_score(
            sample_user_highscore["room_id"], sample_user_highscore["playlist_id"],
            sample_user_highscore["score_id"])
        assert score
        assert score.user
        assert score.user.id == sample_user_highscore["user_id"]
        assert score.id == sample_user_highscore["score_id"]

    @pytest.mark.asyncio
    async def test_get_rooms(self, lazer_async_client):
        rooms = await lazer_async_client.get_rooms(sort=RoomType.PLAYLISTS, limit=5)
        assert len(rooms) == 5
        assert all(map(lambda room: room.type == RoomType.PLAYLISTS, rooms))

    @pytest.mark.asyncio
    async def test_get_room(self, async_client, sample_user_highscore):
        room = await async_client.get_room(sample_user_highscore["room_id"])
        assert room.id == sample_user_highscore["room_id"]

    @pytest.mark.asyncio
    async def test_get_room_leaderboard(self, lazer_async_client, sample_user_highscore):
        leaderboard = await lazer_async_client.get_room_leaderboard(sample_user_highscore["room_id"])
        scores = leaderboard["leaderboard"]
        assert scores
        assert all(map(lambda score: score.room_id == sample_user_highscore["room_id"], scores))
        assert any(map(lambda score: score.user_id == sample_user_highscore["user_id"], scores))

    @pytest.mark.asyncio
    async def test_join_to_room(self, lazer_async_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    @pytest.mark.asyncio
    async def test_kick_from_room(self, lazer_async_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    @pytest.mark.asyncio
    async def test_create_room(self, lazer_async_client):
        # I can implement this cuz the room just like disappears
        # when no one joins, but maybe later
        pass
