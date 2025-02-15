import pytest


@pytest.fixture(scope="module")
def create_topic(dev_user_client):
    yield dev_user_client.create_topic(
        "this is a test for [url=https://github.com/sheppsu/osu.py]osu.py[/url]!",
        75,
        "osu.py test",
        with_poll=True,
        length_days=1,
        poll_options=["[b]borgar[/b]", "[i]pissa[/i]"],
        poll_title="foodge",
    )


class TestForum:
    @pytest.mark.dependency()
    def test_create_topic(self, create_topic):
        assert create_topic.topic.forum_id == 75
        assert create_topic.topic.title == "osu.py test"
        assert create_topic.post.body.raw == "this is a test for [url=https://github.com/sheppsu/osu.py]osu.py[/url]!"

    @pytest.mark.dependency(depends=["TestForum::test_create_topic"])
    def test_edit_post(self, dev_user_client, create_topic):
        new_body = (
            "this is a test for [url=https://github.com/sheppsu/osu.py]osu.py[/url]!\n\n"
            "edit: successfully edited post!"
        )

        post = dev_user_client.edit_post(create_topic.post.id, new_body)

        assert post.body.raw == new_body

    @pytest.mark.dependency(depends=["TestForum::test_create_topic"])
    def test_edit_topic(self, dev_user_client, create_topic):
        topic = dev_user_client.edit_topic(create_topic.topic.id, "osu.py test - title edit success")

        assert topic.title == "osu.py test - title edit success"

    @pytest.mark.dependency(depends=["TestForum::test_create_topic"])
    def test_reply_topic(self, dev_user_client, create_topic):
        post = dev_user_client.reply_topic(create_topic.topic.id, "testing reply")

        assert post.body.raw == "testing reply"

    def test_get_topic_and_posts(self, client, sample_topic):
        ret = client.get_topic_and_posts(sample_topic["id"])
        assert ret.topic
        assert ret.topic.id == sample_topic["id"]
        assert ret.topic.title == sample_topic["title"]
        assert ret.posts

    def test_get_forums(self, client):
        ret = client.get_forums()
        assert ret.forums
        assert isinstance(ret.forums, list)

    def test_get_forum(self, client, sample_forum):
        ret = client.get_forum(sample_forum["id"])
        assert ret.forum.id == sample_forum["id"]
        assert ret.forum.name == sample_forum["name"]
        assert ret.forum.description == sample_forum["description"]

    def test_get_topics(self, client, sample_forum):
        ret = client.get_forum_topics(sample_forum["id"])
        assert ret.topics
        assert isinstance(ret.topics, list)
        assert isinstance(ret.cursor, str)
