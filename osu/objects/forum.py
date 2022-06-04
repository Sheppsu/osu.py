class ForumPost:
    """
    **Attributes**

    created_at: :ref:`Timestamp`

    deleted_at: :ref:`Timestamp`

    edited_at: :ref:`Timestamp`

    edited_by_id: :class:`int`

    forum_id: :class:`int`

    id: :class:`int`

    topic_id: :class:`int`

    user_id: :class:`int`

    **Possible Attributes**

    body: :class:`dict`
        dictionary containing keys html and raw. html: Post content in HTML format. raw: content in BBCode format.
    """
    __slots__ = (
        "created_at", "deleted_at", "edited_at", "edited_by_id", "forum_id",
        "id", "topic_id", "user_id", "body"
    )

    def __init__(self, data):
        self.created_at = data['created_at']
        self.deleted_at = data['deleted_at']
        self.edited_at = data['edited_at']
        self.edited_by_id = data['edited_by_id']
        self.forum_id = data['forum_id']
        self.id = data['id']
        self.topic_id = data['topic_id']
        self.user_id = data['user_id']
        self.body = data.get('body', None)


class ForumTopic:
    """
    **Attributes**

    created_at: :ref:`Timestamp`

    deleted_at: :ref:`Timestamp`

    first_post_id: :class:`int`

    forum_id: :class:`int`

    id: :class:`int`

    is_locked: :class:`bool`

    last_post_id: :class:`int`

    post_count: :class:`int`

    title: :class:`str`

    type: :class:`str`
        normal, sticky, or announcement

    updated_at: :ref:`Timestamp`

    user_id: :class:`int`
    """
    __slots__ = (
        "created_at", "deleted_at", "first_post_id", "forum_id", "id", "is_locked",
        "last_post_id", "post_count", "title", "type", "updated_at", "user_id"
    )

    def __init__(self, data):
        self.created_at = data['created_at']
        self.deleted_at = data['deleted_at']
        self.first_post_id = data['first_post_id']
        self.forum_id = data['forum_id']
        self.id = data['id']
        self.is_locked = data['is_locked']
        self.last_post_id = data['last_post_id']
        self.post_count = data['post_count']
        self.title = data['title']
        self.type = data['type']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
