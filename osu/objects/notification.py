from ..util import prettify


class Notification:
    """
    Represents a notification object.
    Go to :class:`Details` object to see details for each event

    **Attributes**

    id: :class:`int`

    name: :class:`str`
        Name of the event

    created_at: :class:`str`
        ISO 8601 date

    object_type	: :class:`str`

    object_id: :class:`int`

    source_user_id: :class:`int`

    is_read: :class:`bool`

    details: :class:`Details`
        message_id of last known message (only returned in presence responses)

    **Event Names and Meanings**

    beatmapset_discussion_lock
        object_id: Beatmapset id
        object_type: beatmapset
        source_user_id: User who locked discussion

    beatmapset_discussion_post_new
        object_id: Beatmapset id
        object_type: beatmapset
        source_user_id: Poster of the discussion

    beatmapset_discussion_unlock
        object_id: Beatmapset id
        object_type: beatmapset
        source_user_id: User who unlocked discussion

    beatmapset_disqualify
        object_id: Beatmapset id
        object_type: beatmapset
        source_user_id: User who disqualified beatmapset

    beatmapset_love
        object_id: Beatmapset id
        object_type: beatmapset
        source_user_id: User who promoted beatmapset to Loved

    beatmapset_nominate
        object_id: Beatmapset id
        object_type: beatmapset
        source_user_id: User who nominated beatmapset

    beatmapset_qualify
        object_id: Beatmapset id
        object_type: beatmapset
        source_user_id: User whom beatmapset nomination triggered qualification

    beatmapset_remove_from_loved
        object_id: Beatmapset id
        object_type: beatmapset
        source_user_id: User who removed beatmapset from Loved

    beatmapset_reset_nominations
        object_id: Beatmapset id
        object_type: beatmapset
        source_user_id: User who locked discussion

    channel_message
        object_id: Channel id
        object_type: channel
        source_user_id: User who posted message

    forum_topic_reply
        object_id: Topic id
        object_type: forum_topic
        source_user_id: User who posted message
    """
    __slots__ = (
        "id", "name", "created_at", "object_type", "object_id", "is_read",
        "source_user_id", "details"
    )

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.object_type = data['object_type']
        self.object_id = data['object_id']
        self.is_read = data['is_read']

        self.source_user_id = data.get('source_user_id', None)
        self.details = Details(data['details'], self.name) if 'details' in data else None

    def __repr__(self):
        return prettify(self, 'name', 'details')


class Details:
    """
    Contains the details for an event

    **Attributes for each Event**

    beatmapset_discussion_lock
        cover_url: :class:`str`
            Beatmap cover
        title: :class:`str`
            Beatmap title
        username: :class:`str`
            Username of source_user_id

    beatmapset_discussion_post_new
        title: :class:`str`
            Beatmap title
        cover_url: :class:`str`
            Beatmap cover
        discussion_id: :class:`int`

        post_i: :class:`int`

        beatmap_id: :class:`int`
            null if posted to general all
        username: :class:`str`
            Username of source_user_id

    beatmapset_discussion_unlock
        title: :class:`str`
            Beatmap title
        cover_url: :class:`str`
            Beatmap cover
        username: :class:`str`
            Username of source_user_id

    beatmapset_disqualify
        title: :class:`str`
            Beatmap title
        cover_url: :class:`str`
            Beatmap cover
        username: :class:`str`
            Username of source_user_id

    beatmapset_love
        title: :class:`str`
            Beatmap title
        cover_url: :class:`str`
            Beatmap cover
        username: :class:`str`
            Username of source_user_id

    beatmapset_nominate
        title: :class:`str`
            Beatmap title
        cover_url: :class:`str`
            Beatmap cover
        username: :class:`str`
            Username of source_user_id

    beatmapset_qualify
        title: :class:`str`
            Beatmap title
        cover_url: :class:`str`
            Beatmap cover
        username: :class:`str`
            Username of source_user_id

    beatmapset_remove_from_loved
        title: :class:`str`
            Beatmap title
        cover_url: :class:`str`
            Beatmap cover
        username: :class:`str`
            Username of source_user_id

    beatmapset_reset_nominations
        title: :class:`str`
            Beatmap title
        cover_url: :class:`str`
            Beatmap cover
        username: :class:`str`
            Username of source_user_id

    channel_message
        title: :class:`str`
            Up to 36 characters of the message (ends with ... when exceeding 36 characters)
        cover_url: :class:`str`
            Avatar of source_user_id
        username: :class:`str`
            Username of source_user_id

    forum_topic_reply
        title: :class:`str`
            Title of the replied topic
        cover_url: :class:`str`
            Topic cover
        post_id: :class:`int`
            Post id
        username: :class:`str`
            Username of source_user_id
    """
    def __init__(self, data, event_name):
        if event_name in ('beatmapset_discussion_lock', 'beatmapset_discussion_unlock',
                          'beatmapset_disqualify', 'beatmapset_love', 'beatmapset_nominate',
                          'beatmapset_qualify', 'beatmapset_remove_from_loved', 'beatmapset_reset_nominations',
                          'channel_message'):
            self.cover_url = data['cover_url']
            self.title = data['title']
            self.username = data['username']
        elif event_name == 'beatmapset_discussion_post_new':
            self.title = data['title']
            self.cover_url = data['cover_url']
            self.discussion_id = data['discussion_id']
            self.post_id = data['post_id']
            self.beatmap_id = data['beatmap_id']
            self.username = data['username']
        elif event_name == 'forum_topic_reply':
            self.title = data['title']
            self.cover_url = data['cover_url']
            self.post_id = data['post_id']
            self.username = data['username']

    def __repr__(self):
        return prettify(self, 'title')
