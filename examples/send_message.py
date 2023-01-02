from util_for_examples import get_lazer_client


client = get_lazer_client()
for channel in client.get_updates(0)['presence']:
    if channel.name == "SUPERTIAZH":
        print(client.send_message_to_channel(channel.channel_id, "test", False))
        break
