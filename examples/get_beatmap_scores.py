from osu import Client, GameModeStr, Mods
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)


def readable_mod(mods):
    if not mods:
        return ""
    if isinstance(mods, Mods):
        return "+"+mods.to_readable_string()
    return "+"+"".join(map(lambda x: x.mod.value, mods))


def do(mode, lazer=False):
    beatmap_scores = (client.get_beatmap_scores if not lazer else client.get_lazer_beatmap_scores)(878369, mode)
    print(f"Top 5 scores on this beatmap ({mode.name}, lazer={lazer}):")
    print("\n".join(
        [f'{i + 1}. {score.user.username} {readable_mod(score.mods)} - '
         f'{score.pp}' for i, score in enumerate(beatmap_scores.scores[:5])]))
    print()


do(GameModeStr.STANDARD)
do(GameModeStr.TAIKO)
do(GameModeStr.STANDARD, True)
