from util_for_examples import get_lazer_client


client = get_lazer_client()
print(client.check_download_quota())
