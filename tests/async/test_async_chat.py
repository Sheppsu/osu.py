import pytest
import pytest_asyncio

from osu import ChatChannelType

from tests.util import as_async


@pytest_asyncio.fixture(scope="module")
async def async_create_new_pm(dev_user_client, sample_dev_user):
    dev_async_user_client = as_async(dev_user_client)
    ret = await dev_async_user_client.create_new_pm(sample_dev_user["id"], "testing create_new_pm", False)

    assert ret.channel.type == ChatChannelType.PM
    assert ret.channel.name == sample_dev_user["username"]
    assert ret.message.content == "testing create_new_pm"

    return ret.channel


@pytest_asyncio.fixture(scope="module")
async def async_get_channel_messages(dev_user_client, sample_channel):
    dev_async_user_client = as_async(dev_user_client)
    messages = await dev_async_user_client.get_channel_messages(sample_channel["id"])
    if len(messages) == 0:
        return

    assert messages[0].channel_id == sample_channel["id"]

    return sorted(messages, key=lambda m: m.message_id)[-1]


class TestAsynchronousChat:
    @pytest.mark.asyncio
    async def test_chat_keepalive(self, dev_user_client):
        dev_async_user_client = as_async(dev_user_client)
        await dev_async_user_client.chat_keepalive()

    @pytest.mark.asyncio
    async def test_create_new_pm(self, async_create_new_pm):
        pass

    @pytest.mark.asyncio
    @pytest.mark.dependency()
    async def test_join_channel(self, dev_user_client, sample_channel, dev_own_data):
        dev_async_user_client = as_async(dev_user_client)
        channel = await dev_async_user_client.join_channel(sample_channel["id"], dev_own_data.id)

        assert channel.channel_id == sample_channel["id"]
        assert channel.type == sample_channel["type"]
        assert channel.name == sample_channel["name"]

    @pytest.mark.asyncio
    @pytest.mark.dependency(depends=["TestAsynchronousChat::test_join_channel"])
    async def test_get_channel(self, dev_user_client, sample_channel):
        dev_async_user_client = as_async(dev_user_client)
        ret = await dev_async_user_client.get_channel(sample_channel["id"])
        assert ret.channel.channel_id == sample_channel["id"]

    @pytest.mark.asyncio
    @pytest.mark.dependency(depends=["TestAsynchronousChat::test_join_channel"])
    async def test_get_channel_messages(self, async_get_channel_messages):
        pass

    @pytest.mark.asyncio
    @pytest.mark.dependency(depends=["TestAsynchronousChat::test_join_channel"])
    async def test_mark_as_read(self, dev_user_client, sample_channel, async_get_channel_messages):
        dev_async_user_client = as_async(dev_user_client)
        await dev_async_user_client.mark_channel_as_read(
            sample_channel["id"], 0 if async_get_channel_messages is None else async_get_channel_messages.channel_id
        )

    @pytest.mark.asyncio
    @pytest.mark.dependency(depends=["TestAsynchronousChat::test_join_channel"])
    async def test_send_message_to_channel(self, dev_user_client, sample_channel, async_create_new_pm):
        dev_async_user_client = as_async(dev_user_client)
        msg = await dev_async_user_client.send_message_to_channel(
            sample_channel["id"], "running test for (osu.py)[https://github.com/sheppsu/osu.py] :)", False
        )

        assert msg.content == "running test for (osu.py)[https://github.com/sheppsu/osu.py] :)"

        if async_create_new_pm.channel_id is not None:
            msg = await dev_async_user_client.send_message_to_channel(
                async_create_new_pm.channel_id, "testing send_message_to_channel", False
            )

            assert msg.content == "testing send_message_to_channel"

    @pytest.mark.asyncio
    @pytest.mark.dependency(depends=["TestAsynchronousChat::test_join_channel"])
    async def test_leave_channel(self, dev_user_client, sample_channel, dev_own_data):
        dev_async_user_client = as_async(dev_user_client)
        await dev_async_user_client.leave_channel(sample_channel["id"], dev_own_data.id)

    @pytest.mark.asyncio
    async def test_create_pm_channel(self, dev_user_client, sample_dev_user, async_create_new_pm):
        dev_async_user_client = as_async(dev_user_client)
        channel = await dev_async_user_client.create_pm_channel(sample_dev_user["id"])

        assert channel.channel_id == async_create_new_pm.channel_id

    @pytest.mark.asyncio
    async def test_get_channel_list(self, dev_user_client):
        dev_async_user_client = as_async(dev_user_client)
        await dev_async_user_client.get_channel_list()
