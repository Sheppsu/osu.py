from util_for_examples import get_user_client
from osu import GameModeStr


client = get_user_client()
replay = client.get_replay_data(GameModeStr.STANDARD, 3693301831)
replay.write_path('replay.osr')
