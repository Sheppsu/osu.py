from util_for_examples import get_lazer_client


client = get_lazer_client()
updates = client.get_updates(0)
print(updates)
