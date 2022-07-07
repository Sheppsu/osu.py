from osu import Mods, GameModeStr, UserBeatmapType, BeatmapPlaycount, Beatmapset
from test import BaseTest
from data import DataCompiler


class Test(BaseTest):
    test_name = "beatmap"

    def search_beatmapsets(self):
        # TODO: test other search parameters
        print("Getting 8 beatmaps of each gamemode via search...")
        beatmapsets = DataCompiler.get_eight_beatmapsets(self.client)
        print("Checking gamemodes")
        assert all(list(map(lambda bms: any(list(map(lambda bm: bm.mode == GameModeStr.STANDARD, bms.beatmaps))), beatmapsets[:2])))
        assert all(list(map(lambda bms: any(list(map(lambda bm: bm.mode == GameModeStr.TAIKO, bms.beatmaps))), beatmapsets[2:4])))
        assert all(list(map(lambda bms: any(list(map(lambda bm: bm.mode == GameModeStr.CATCH, bms.beatmaps))), beatmapsets[4:6])))
        assert all(list(map(lambda bms: any(list(map(lambda bm: bm.mode == GameModeStr.MANIA, bms.beatmaps))), beatmapsets[6:8])))
        print("Finished testing search_beatmapsets")
        return beatmapsets

    def get_beatmaps(self, beatmapsets):
        print("Creating list of beatmap ids to test...")
        beatmap_ids = []
        modes = [GameModeStr.STANDARD, GameModeStr.TAIKO, GameModeStr.CATCH, GameModeStr.MANIA]
        for i, beatmapset in enumerate(beatmapsets):
            for bm in beatmapset.beatmaps:
                if bm.mode == modes[i//2]:
                    beatmap_ids.append(bm.id)
                    break

        print("Testing get_beatmap...")
        beatmaps1 = [self.client.get_beatmap(bm_id) for bm_id in beatmap_ids]
        print("Testing get_beatmaps...")
        self.client.get_beatmaps(beatmap_ids)
        print("Finished testing get_beatmap and get_beatmaps")
        return beatmaps1

    def get_user_beatmaps(self, beatmaps):
        print("Generating list of users to test with...")
        users = [bm.user_id for bm in beatmaps]
        beatmap_types = [
            UserBeatmapType.FAVOURITE, UserBeatmapType.GRAVEYARD, UserBeatmapType.LOVED,
            UserBeatmapType.MOST_PLAYED, UserBeatmapType.PENDING, UserBeatmapType.RANKED
        ]
        for i, user in enumerate(users[:2]):
            print("Testing get_user_beatmaps for user {}...".format(user))
            for beatmap_type in beatmap_types:
                print("Testing get_user_beatmaps for user {} with beatmap type {}...".format(user, beatmap_type))
                beatmaps = self.client.get_user_beatmaps(user, beatmap_type)
                if not beatmaps:
                    continue
                if beatmap_type == UserBeatmapType.MOST_PLAYED:
                    assert type(beatmaps[0]) == BeatmapPlaycount
                else:
                    assert type(beatmaps[0]) == Beatmapset
            print("Finished testing get_user_beatmaps for user {}".format(user))
        print("Finished testing get_user_beatmaps")

    def get_beatmap_attributes(self, beatmaps):
        mods = [
            Mods.DoubleTime | Mods.SpunOut | Mods.Hidden | Mods.Relax,
            Mods.parse_and_return_any_list(["TD", "Easy", Mods.NoFail | Mods.HalfTime, "SO"]),
            Mods.get_from_abbreviation("FL"),
            Mods.parse_and_return_any_list(["HD", "HardRock", (1 << 6), Mods.Flashlight]),
            Mods.get_from_list([Mods.DoubleTime, Mods.HardRock]),
            Mods.get_from_list([Mods.HalfTime, Mods.Hidden]),
            Mods.Flashlight | Mods.Easy | Mods.Hidden,
            Mods.Mirror
        ]
        print("Testing get_beatmap_attributes...")
        for i, beatmap in enumerate(beatmaps):
            self.client.get_beatmap_attributes(beatmap.id, mods=mods[i])
        print("Finished testing get_beatmap_attributes")

    def lookup_beatmap(self, beatmaps):
        print("Testing lookup_beatmap...")
        # TODO: figure out how to do checksum ig?

        for beatmap in beatmaps[4:6]:
            beatmap_result = self.client.lookup_beatmap(
                filename=f"{beatmap.beatmapset.artist} - {beatmap.beatmapset.title} "
                         f"({beatmap.beatmapset.creator}) [{beatmap.version}].osu"
            )
            assert beatmap_result.id == beatmap.id

        for beatmap in beatmaps[:2]:
            beatmap_result = self.client.lookup_beatmap(id=beatmap.id)
            assert beatmap_result.id == beatmap.id
        print("Finished testing lookup_beatmap")

    def run_all_tests(self):
        beatmapsets = self.test(self.search_beatmapsets)
        if beatmapsets is None:
            return print("Unable to continue beatmap testing because search_beatmapsets failed.")
        beatmaps = self.test(self.get_beatmaps, beatmapsets)
        if beatmaps is None:
            return print("Unable to continue beatmap testing because get_beatmaps failed.")
        #self.test(self.get_beatmap_attributes, beatmaps)
        #self.test(self.get_user_beatmaps, beatmaps)
        self.test(self.lookup_beatmap, beatmaps)
