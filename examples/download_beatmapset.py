from util_for_examples import get_lazer_client
import asyncio


client = get_lazer_client(True)
asyncio.run(client.download_beatmapset(461966, "461966.osz"))
