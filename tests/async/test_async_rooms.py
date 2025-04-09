import pytest

from osu import RoomType, RoomSort

from tests.util import as_async


class TestAsynchronousRooms:
    @pytest.mark.asyncio
    async def test_get_scores(self, user_client, sample_user_highscore):
        async_user_client = as_async(user_client)
        await async_user_client.get_scores(sample_user_highscore["room_id"], sample_user_highscore["playlist_id"])

    @pytest.mark.asyncio
    async def test_get_rooms(self, user_client):
        async_user_client = as_async(user_client)
        rooms = await async_user_client.get_rooms(room_type=RoomType.PLAYLISTS, limit=5)
        assert len(rooms) == 5
        assert all(map(lambda room: room.type == RoomType.PLAYLISTS, rooms))

    @pytest.mark.asyncio
    async def test_get_room(self, client, sample_user_highscore):
        async_client = as_async(client)
        room = await async_client.get_room(sample_user_highscore["room_id"])
        assert room.id == sample_user_highscore["room_id"]

    @pytest.mark.asyncio
    async def test_get_room_leaderboard(self, user_client, sample_user_highscore):
        async_user_client = as_async(user_client)
        ret = await async_user_client.get_room_leaderboard(sample_user_highscore["room_id"])
        scores = ret.leaderboard
        assert scores
        assert all(map(lambda score: score.room_id == sample_user_highscore["room_id"], scores))
        assert any(map(lambda score: score.user_id == sample_user_highscore["user_id"], scores))
