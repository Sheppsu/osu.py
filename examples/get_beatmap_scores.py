from osu import Client, GameModeStr, Mods, Mod
import os


client_id = int(os.getenv('CLIENT_ID'))
client_secret = os.getenv('CLIENT_SECRET')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_credentials(client_id, client_secret, redirect_url)


def readable_mod(mods):
    if not mods:
        return ""
    if isinstance(mods, Mods):
        return "+"+mods.to_readable_string()
    return "+"+"".join(map(lambda x: x.mod.value, mods))


def do(mode, mods=None, lazer=False):
    ret = (client.get_beatmap_scores if not lazer else client.get_lazer_beatmap_scores)(2874408, mode, mods)
    print(f"Top 5 scores on this beatmap ({mode.name}, lazer={lazer}):")
    print("\n".join(
        [f'{i + 1}. {score.user.username} {readable_mod(score.mods)} - '
         f'{score.pp}' for i, score in enumerate(ret.scores[:5])]))
    print()


do(GameModeStr.STANDARD, Mods.HardRock | Mods.NoFail)
do(GameModeStr.MANIA, ["HD"])
do(GameModeStr.STANDARD, [Mod.DifficultyAdjust], lazer=True)
