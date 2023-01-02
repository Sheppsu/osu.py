from util_for_examples import get_lazer_client


client = get_lazer_client()
channels = client.get_open_chat_channels()
print(channels)
