class TestChat:
    def test_chat_acknowledge(self, lazer_client):
        # TODO: test parameters
        lazer_client.chat_acknowledge()

    def test_create_new_pm(self, lazer_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    def get_updates(self, lazer_client):
        ret = lazer_client.get_updates()
        assert ret

    def test_send_message_to_channel(self, lazer_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    def test_join_channel(self, lazer_client, sample_channel, own_data):
        channel = lazer_client.join_channel(sample_channel["id"], own_data.id)
        assert channel
        assert channel.channel_id == sample_channel["id"]
        assert channel.name == sample_channel["name"]

    def test_get_channel_messages(self, real_messages):
        assert real_messages

    def test_get_channel(self, lazer_client, sample_channel):
        ret = lazer_client.get_channel(sample_channel["id"])
        assert ret
        assert ret.channel
        assert ret.channel.channel_id == sample_channel["id"]

    def test_mark_channel_as_read(self, lazer_client, sample_channel, real_messages):
        lazer_client.mark_channel_as_read(sample_channel["id"], real_messages[-1].message_id)

    def test_leave_channel(self, lazer_client, sample_channel, own_data):
        lazer_client.leave_channel(sample_channel["id"], own_data.id)

    def test_get_channel_list(self, lazer_client, sample_channel):
        channels = lazer_client.get_channel_list()
        assert channels
        assert any(map(lambda channel: channel.channel_id == sample_channel["id"], channels))

    def test_create_channel(self, lazer_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    def test_get_open_chat_channels(self, lazer_client):
        channels = lazer_client.get_open_chat_channels()
        assert channels
