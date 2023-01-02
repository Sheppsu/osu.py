from util_for_examples import get_lazer_client


client = get_lazer_client()
channels = client.get_channel_list()
print(channels)
channel = channels[0]
messages = client.get_channel_messages(channel.channel_id)
print(messages)
