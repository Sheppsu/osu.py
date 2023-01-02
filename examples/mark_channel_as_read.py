from util_for_examples import get_lazer_client


client = get_lazer_client()
messages = client.get_channel_messages(5)
for message in messages:
    print(f"{message.sender.username}: {message.content}")
client.mark_channel_as_read(5, messages[-1].message_id)
