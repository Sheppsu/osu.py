from util_for_examples import get_lazer_client


client = get_lazer_client()
resp = client.create_new_pm(14895608, "a", False)
