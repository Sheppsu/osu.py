import pytest


class TestAsynchronousChat:
    @pytest.mark.asyncio
    async def test_chat_acknowledge(self, lazer_async_client):
        await lazer_async_client.chat_acknowledge()

    @pytest.mark.asyncio
    async def test_create_new_pm(self, lazer_async_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    @pytest.mark.asyncio
    async def get_updates(self, lazer_client):
        ret = await lazer_client.get_updates()
        assert ret

    @pytest.mark.asyncio
    async def test_send_message_to_channel(self, lazer_async_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    @pytest.mark.asyncio
    async def test_join_channel(self, lazer_async_client, sample_channel, own_data):
        channel = await lazer_async_client.join_channel(sample_channel["id"], own_data.id)
        assert channel
        assert channel.channel_id == sample_channel["id"]
        assert channel.name == sample_channel["name"]

    @pytest.mark.asyncio
    async def test_get_channel_messages(self, async_real_messages):
        assert async_real_messages

    @pytest.mark.asyncio
    async def test_get_channel(self, lazer_async_client, sample_channel):
        ret = await lazer_async_client.get_channel(sample_channel["id"])
        assert ret
        assert ret.channel
        assert ret.channel.channel_id == sample_channel["id"]

    @pytest.mark.asyncio
    async def test_mark_channel_as_read(self, lazer_async_client, sample_channel, async_real_messages):
        async_real_messages = await async_real_messages
        await lazer_async_client.mark_channel_as_read(sample_channel["id"], async_real_messages[-1].message_id)

    @pytest.mark.asyncio
    async def test_leave_channel(self, lazer_async_client, sample_channel, own_data):
        await lazer_async_client.leave_channel(sample_channel["id"], own_data.id)

    @pytest.mark.asyncio
    async def test_get_channel_list(self, lazer_async_client, sample_channel):
        channels = await lazer_async_client.get_channel_list()
        assert channels
        assert any(map(lambda channel: channel.channel_id == sample_channel["id"], channels))

    @pytest.mark.asyncio
    async def test_create_channel(self, lazer_async_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    @pytest.mark.asyncio
    async def test_get_open_chat_channels(self, lazer_async_client):
        channels = await lazer_async_client.get_open_chat_channels()
        assert channels
