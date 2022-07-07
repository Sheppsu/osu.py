from osu import GameModeInt, GameModeStr


class DataCompiler:
    @staticmethod
    def get_eight_beatmapsets(client):
        return client.search_beatmapsets(filters={'m': GameModeInt.STANDARD.value})["beatmapsets"][:2] + \
               client.search_beatmapsets(filters={'m': GameModeInt.TAIKO.value})["beatmapsets"][:2] + \
               client.search_beatmapsets(filters={'m': GameModeInt.CATCH.value})["beatmapsets"][:2] + \
               client.search_beatmapsets(filters={'m': GameModeInt.MANIA.value})["beatmapsets"][:2]

    @staticmethod
    def get_eight_beatmaps_from_eight_beatmapsets(beatmapsets):
        beatmaps = []
        modes = [GameModeStr.STANDARD, GameModeStr.TAIKO, GameModeStr.CATCH, GameModeStr.MANIA]
        for i, beatmapset in enumerate(beatmapsets):
            for bm in beatmapset.beatmaps:
                if bm.mode == modes[i // 2]:
                    beatmaps.append(bm)
                    break

        if len(beatmaps) != 8:
            raise ValueError("Something went wrong when processing the beatmapsets passed.")
        return beatmaps

