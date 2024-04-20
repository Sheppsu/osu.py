import pytest

from osu import RoomType


class TestAsynchronousRooms:
    @pytest.mark.asyncio
    async def test_get_scores(self, async_user_client, sample_user_highscore):
        await async_user_client.get_scores(
            sample_user_highscore["room_id"], sample_user_highscore["playlist_id"]
        )

    @pytest.mark.asyncio
    async def test_get_rooms(self, async_user_client):
        rooms = await async_user_client.get_rooms(sort=RoomType.PLAYLISTS, limit=5)
        assert len(rooms) == 5
        assert all(map(lambda room: room.type == RoomType.PLAYLISTS, rooms))

    @pytest.mark.asyncio
    async def test_get_room(self, async_client, sample_user_highscore):
        room = await async_client.get_room(sample_user_highscore["room_id"])
        assert room.id == sample_user_highscore["room_id"]

    @pytest.mark.asyncio
    async def test_get_room_leaderboard(self, async_user_client, sample_user_highscore):
        ret = await async_user_client.get_room_leaderboard(sample_user_highscore["room_id"])
        scores = ret.leaderboard
        assert scores
        assert all(map(lambda score: score.room_id == sample_user_highscore["room_id"], scores))
        assert any(map(lambda score: score.user_id == sample_user_highscore["user_id"], scores))
