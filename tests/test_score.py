from test import BaseTest
from data import DataCompiler


class Test(BaseTest):
    test_name = 'score'

    def get_beatmap_scores(self, beatmaps):
        # TODO: check mods and types once they're implemented by the api
        scores = []

        print("Testing get_beatmap_scores for each beatmap...")
        for beatmap in beatmaps:
            score = self.client.get_beatmap_scores(beatmap.id, beatmap.mode).scores[0]
            score.beatmap = beatmap  # score objects from BeatmapScores objects lack the beatmap attribute
            scores.append(score)

        return scores

    def get_user_beatmap_score_open_parenthesis_s_closed_parenthesis(self, scores):  # :tf: function name
        # TODO: check mods once that's implemented by the api

        print("Testing get_user_beatmap_score(s) for each score...")
        for score in scores:
            self.client.get_user_beatmap_score(score.beatmap.id, score.user_id, score.mode)
            self.client.get_user_beatmap_scores(score.beatmap.id, score.user_id, score.mode)

    def run_all_tests(self):
        beatmapsets = DataCompiler.get_eight_beatmapsets(self.client)
        beatmaps = DataCompiler.get_eight_beatmaps_from_eight_beatmapsets(beatmapsets)
        if beatmaps is None:
            return print("Unable to continue score testing because beatmaps could not be retrieved.")
        scores = self.test(self.get_beatmap_scores, beatmaps)
        self.test(self.get_user_beatmap_score_open_parenthesis_s_closed_parenthesis, scores)
