from osu import CommentSort


class TestComment:
    def _assert_comment_bundle(self, comments, sample_comment):
        assert comments
        assert comments.comments
        comment = comments.comments[0]
        assert comment
        assert comment.id == sample_comment["id"]
        assert comment.message == sample_comment["message"]
        assert comment.user_id == sample_comment["user_id"]

    def test_get_comments(self, client, sample_comment):
        # TODO: test more parameters
        comments = client.get_comments(sort=CommentSort.OLD)
        self._assert_comment_bundle(comments, sample_comment)

    def test_get_comment(self, client, sample_comment):
        comments = client.get_comment(sample_comment["id"])
        self._assert_comment_bundle(comments, sample_comment)
