import pytest

from osu import ChatChannelType


@pytest.fixture(scope='module')
def create_new_pm(dev_user_client, sample_dev_user):
    ret = dev_user_client.create_new_pm(sample_dev_user["id"], "testing create_new_pm", False)

    assert ret.channel.type == ChatChannelType.PM
    assert ret.channel.name == sample_dev_user["username"]
    assert ret.message.content == "testing create_new_pm"

    yield ret.channel


@pytest.fixture(scope='module')
def get_channel_messages(dev_user_client, sample_channel):
    messages = dev_user_client.get_channel_messages(sample_channel["id"])
    if len(messages) == 0:
        return None

    assert messages[0].channel_id == sample_channel["id"]

    yield sorted(messages, key=lambda m: m.message_id)[-1]


class TestChat:
    def test_chat_keepalive(self, dev_user_client):
        dev_user_client.chat_keepalive()

    def test_create_new_pm(self, create_new_pm):
        pass

    @pytest.mark.dependency()
    def test_join_channel(self, dev_user_client, sample_channel, dev_own_data):
        channel = dev_user_client.join_channel(sample_channel["id"], dev_own_data.id)

        assert channel.channel_id == sample_channel["id"]
        assert channel.type == sample_channel["type"]
        assert channel.name == sample_channel["name"]

    @pytest.mark.dependency(depends=["TestChat::test_join_channel"])
    def test_get_channel(self, dev_user_client, sample_channel):
        ret = dev_user_client.get_channel(sample_channel["id"])
        assert ret.channel.channel_id == sample_channel["id"]

    @pytest.mark.dependency(depends=["TestChat::test_join_channel"])
    def test_get_channel_messages(self, get_channel_messages):
        pass

    @pytest.mark.dependency(depends=["TestChat::test_join_channel"])
    def test_mark_as_read(self, dev_user_client, sample_channel, get_channel_messages):
        dev_user_client.mark_channel_as_read(
            sample_channel["id"], 0 if get_channel_messages is None else get_channel_messages.channel_id
        )

    @pytest.mark.dependency(depends=["TestChat::test_join_channel"])
    def test_send_message_to_channel(self, dev_user_client, sample_channel, create_new_pm):
        msg = dev_user_client.send_message_to_channel(
            sample_channel["id"], "running test for (osu.py)[https://github.com/sheppsu/osu.py] :)", False
        )

        assert msg.content == "running test for (osu.py)[https://github.com/sheppsu/osu.py] :)"

        if create_new_pm.channel_id is not None:
            msg = dev_user_client.send_message_to_channel(
                create_new_pm.channel_id, "testing send_message_to_channel", False
            )

            assert msg.content == "testing send_message_to_channel"

    @pytest.mark.dependency(depends=["TestChat::test_join_channel"])
    def test_leave_channel(self, dev_user_client, sample_channel, dev_own_data):
        dev_user_client.leave_channel(sample_channel["id"], dev_own_data.id)

    def test_create_pm_channel(self, dev_user_client, sample_dev_user, create_new_pm):
        channel = dev_user_client.create_pm_channel(sample_dev_user["id"])

        assert channel.channel_id == create_new_pm.channel_id

    def test_get_channel_list(self, dev_user_client):
        dev_user_client.get_channel_list()
