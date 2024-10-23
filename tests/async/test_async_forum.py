import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="module")
async def async_create_topic(dev_async_user_client):
    return await dev_async_user_client.create_topic(
        "this is a test for [url=https://github.com/sheppsu/osu.py]osu.py[/url]!",
        75,
        "osu.py test",
        with_poll=True,
        length_days=1,
        poll_options=["[b]borgar[/b]", "[i]pissa[/i]"],
        poll_title="foodge",
    )


class TestAsynchronousForum:
    @pytest.mark.asyncio
    @pytest.mark.dependency()
    async def test_create_topic(self, async_create_topic):
        assert async_create_topic.topic.forum_id == 75
        assert async_create_topic.topic.title == "osu.py test"
        assert (
            async_create_topic.post.body.raw
            == "this is a test for [url=https://github.com/sheppsu/osu.py]osu.py[/url]!"
        )

    @pytest.mark.asyncio
    @pytest.mark.dependency(depends=["TestForum::test_create_topic"])
    async def test_edit_post(self, dev_async_user_client, async_create_topic):
        new_body = (
            "this is a test for [url=https://github.com/sheppsu/osu.py]osu.py[/url]!\n\n"
            "edit: successfully edited post!"
        )

        post = await dev_async_user_client.edit_post(async_create_topic.post.id, new_body)

        assert post.body.raw == new_body

    @pytest.mark.asyncio
    @pytest.mark.dependency(depends=["TestForum::test_create_topic"])
    async def test_edit_topic(self, dev_async_user_client, async_create_topic):
        topic = await dev_async_user_client.edit_topic(async_create_topic.topic.id, "osu.py test - title edit success")

        assert topic.title == "osu.py test - title edit success"

    @pytest.mark.asyncio
    @pytest.mark.dependency(depends=["TestForum::test_create_topic"])
    async def test_reply_topic(self, dev_async_user_client, async_create_topic):
        post = await dev_async_user_client.reply_topic(async_create_topic.topic.id, "testing reply")

        assert post.body.raw == "testing reply"

    @pytest.mark.asyncio
    async def test_get_topic_and_posts(self, async_client, sample_topic):
        ret = await async_client.get_topic_and_posts(sample_topic["id"])
        assert ret.topic
        assert ret.topic.id == sample_topic["id"]
        assert ret.topic.title == sample_topic["title"]
        assert ret.posts
