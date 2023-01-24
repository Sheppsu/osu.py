from osu import CommentSort


class TestComment:
    def assert_comment_bundle(self, comments, sample_comment):
        assert comments
        assert comments.comments
        comment = comments.comments[0]
        assert comment
        assert comment.id == sample_comment["id"]
        assert comment.message == sample_comment["message"]
        assert comment.user_id == sample_comment["user_id"]

    def test_get_comments(self, client, sample_comment):
        comments = client.get_comments(sort=CommentSort.OLD)
        self.assert_comment_bundle(comments, sample_comment)

    def test_post_new_comment(self, lazer_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    def test_get_comment(self, client, sample_comment):
        comments = client.get_comment(sample_comment["id"])
        self.assert_comment_bundle(comments, sample_comment)

    def test_edit_comment(self, lazer_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    def test_delete_comment(self, lazer_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    def test_add_comment_vote(self, lazer_client, sample_comment):
        comments = lazer_client.add_comment_vote(sample_comment["id"])
        self.assert_comment_bundle(comments, sample_comment)

    def test_remove_comment_vote(self, lazer_client, sample_comment):
        comments = lazer_client.remove_comment_vote(sample_comment["id"])
        self.assert_comment_bundle(comments, sample_comment)
