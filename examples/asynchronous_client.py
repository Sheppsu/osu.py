from osu import AsynchronousClient, GameModeStr
from os import getenv
from time import perf_counter
import asyncio


client_id = int(getenv("osu_client_id"))
client_secret = getenv("osu_client_secret")
client = AsynchronousClient.from_credentials(client_id, client_secret, "http://127.0.0.1:8080", request_wait_time=0)


async def make_requests(mode, rank_type):
    cursor = None
    ret = []
    for i in range(8):
        print(f"{mode} {rank_type} {i}")
        ranking = await client.get_ranking(mode, rank_type, cursor=cursor)
        cursor = ranking.cursor
        ret.append(ranking.ranking[0].user.username)
    return ret


async def run():
    start_time = perf_counter()
    results = await asyncio.gather(
        make_requests(GameModeStr.STANDARD, "performance"),
        make_requests(GameModeStr.STANDARD, "score"),
        make_requests(GameModeStr.MANIA, "performance"),
        make_requests(GameModeStr.MANIA, "score"),
        make_requests(GameModeStr.TAIKO, "performance"),
        make_requests(GameModeStr.TAIKO, "score"),
        make_requests(GameModeStr.CATCH, "performance"),
        make_requests(GameModeStr.CATCH, "score"),
    )
    print(results)
    print(f"Total run time: {perf_counter() - start_time}")


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(run())
