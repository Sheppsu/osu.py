from dateutil import parser

from ..util import prettify
from ..enums import NotificationCategory, ObjectType, NotificationType, ChatChannelType, GameModeStr


class Notification:
    """
    Represents a notification object.
    Go to :class:`Details` object to see details for each event

    **Attributes**

    id: :class:`int`

    name: :class:`NotificationType`
        The type of event

    created_at: :class:`datetime.datetime`

    object_type: :class:`ObjectType`

    object_id: :class:`int`

    source_user_id: :class:`int`

    is_read: :class:`bool`

    details: Optional[Union[
    :class:`BeatmapOwnerChangeDetails`, :class:`BeatmapsetDiscussionLockDetails`,
    :class:`BeatmapsetDiscussionPostDetails`, :class:`BeatmapsetDiscussionQualifiedProblemDetails`,
    :class:`BeatmapsetDiscussionReviewNewDetails`, :class:`BeatmapsetDiscussionUnlockDetails`,
    :class:`BeatmapsetDisqualifyDetails`, :class:`BeatmapsetLoveDetails`,
    :class:`BeatmapsetNominateDetails`, :class:`BeatmapsetQualifyDetails`,
    :class:`BeatmapsetRankDetails`, :class:`BeatmapsetRemoveFromLovedDetails`,
    :class:`BeatmapsetResetNominationsDetails`, :class:`ChannelAnnouncementDetails`,
    :class:`ChannelMessageDetails`, :class:`CommentNewDetails`,
    :class:`ForumTopicReplyDetails`, :class:`UserAchievementUnlockDetails`,
    :class:`UserBeatmapsetNewDetails`, :class:`UserBeatmapsetReviveDetails`
    ]]
        Details of the notification.

    source_user_id: Optional[int]


    **Documented event names and their attribute meanings**

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
        self.name = NotificationType(data['name'])
        self.created_at = parser.parse(data['created_at'])
        self.object_type = ObjectType(data['object_type'])
        self.object_id = data['object_id']
        self.is_read = data['is_read']
        self.details = Details(data['details'], self.name)

        self.source_user_id = data.get('source_user_id', None)

    def __repr__(self):
        return prettify(self, 'name', 'details')


class ReadNotification:
    """
    Represents a read notification.

    **Attributes**

    category: :class:`str`

    id: :class:`int`

    object_id: :class:`int`

    object_type: :class:`str`
    """
    __slots__ = ("category", "id", "object_id", "object_type")

    def __init__(self, data):
        self.category = NotificationCategory(data["category"])
        self.id = data["id"]
        self.object_id = data["object_id"]
        self.object_type = ObjectType(data["object_type"])

    def __repr__(self):
        return prettify(self, 'id')


class NotificationsDetailsBase:
    """
    Base class for all Detail objects.

    **Attributes**

    username: :class:`str`
    """
    __slots__ = ("username",)

    def __init__(self, data):
        self.username = data["username"]

    def __repr__(self):
        # all the subclasses have a title attribute
        return prettify(self, "title", "username")


class BeatmapOwnerChangeDetails(NotificationsDetailsBase):
    """
    When ownership of a beatmap is transferred (for guest difficulties).

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    beatmap_id: :class:`int`

    cover_url: :class:`str`

    title: :class:`str`

    title_unicode: :class:`str`

    version: :class:`str`
    """
    __slots__ = ("beatmap_id", "cover_url", "title", "title_unicode", "version")

    def __init__(self, data):
        super().__init__(data)
        self.beatmap_id = data["beatmap_id"]
        self.cover_url = data["cover_url"]
        self.title = data["title"]
        self.title_unicode = data["title_unicode"]
        self.version = data["version"]


class BeatmapsetNotificationDetails(NotificationsDetailsBase):
    """
    Base class for several other detail objects.

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    title: :class:`str`

    title_unicode: :class:`str`

    cover_url: :class:`str`
    """
    __slots__ = ("title", "title_unicode", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.title = data["title"]
        self.title_unicode = data["title_unicode"]
        self.cover_url = data["cover_url"]


class BeatmapsetDiscussionPostNotificationDetails(NotificationsDetailsBase):
    """
    Base class for a couple other detail objects.

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    content: :class:`str`

    title: :class:`str`

    title_unicode: :class:`str`

    post_id: :class:`int`

    discussion_id: :class:`int`

    beatmap_id: :class:`int`

    cover_url: :class:`str`
    """
    __slots__ = (
        "content", "title", "title_unicode", "post_id", "discussion_id",
        "beatmap_id", "cover_url"
    )

    def __init__(self, data):
        super().__init__(data)
        self.content = data["content"]
        self.title = data["title"]
        self.title_unicode = data["title_unicode"]
        self.post_id = data["post_id"]
        self.discussion_id = data["discussion_id"]
        self.beatmap_id = data["beatmap_id"]
        self.cover_url = data["cover_url"]


class BeatmapsetDiscussionReviewNewDetails(NotificationsDetailsBase):
    """
    New beatmapset discussion review.

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    title: :class:`str`

    title_unicode: :class:`str`

    post_id: :class:`int`

    discussion_id: :class:`int`

    beatmap_id: :class:`int`

    cover_url: :class:`str`

    embeds: :class:`dict`
        contains keys 'suggestions', 'problems', and 'praises'
    """
    __slots__ = (
        "title", "title_unicode", "post_id", "discussion_id",
        "beatmap_id", "cover_url", "embeds"
    )

    def __init__(self, data):
        super().__init__(data)
        self.title = data["title"]
        self.title_unicode = data["title_unicode"]
        self.post_id = data["post_id"]
        self.discussion_id = data["discussion_id"]
        self.beatmap_id = data["beatmap_id"]
        self.cover_url = data["cover_url"]
        self.embeds = data["embeds"]


class ChannelAnnouncementDetails(NotificationsDetailsBase):
    """
    Chat channel announcement

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    channel_id: :class:`int`

    name: :class:`str`

    title: :class:`str`

    type: :class:`ChatChannelType`

    cover_url: :class:`str`
    """
    __slots__ = ("channel_id", "name", "title", "type", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.channel_id = data["channel_id"]
        self.name = data["name"]
        self.title = data["title"]
        self.type = ChatChannelType(data["type"].upper())
        self.cover_url = data["cover_url"]


class ChannelMessageDetails(NotificationsDetailsBase):
    """
    Chat channel message

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    title: :class:`str`

    type: :class:`ChatChannelType`

    cover_url: :class:`str`
    """
    __slots__ = ("title", "type", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.title = data["title"]
        self.type = ChatChannelType(data["type"].upper())
        self.cover_url = data["cover_url"]


class CommentNewDetails(NotificationsDetailsBase):
    """
    New comment

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    comment_id: :class:`int`

    title: :class:`str`

    content: :class:`str`

    cover_url: :class:`str`
    """
    __slots__ = ("comment_id", "title", "content", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.comment_id = data["comment_id"]
        self.title = data["title"]
        self.content = data["content"]
        self.cover_url = data["cover_url"]


class ForumTopicReplyDetails(NotificationsDetailsBase):
    """
    Forum topic reply

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    title: :class:`str`

    post_id: :class:`int`

    cover_url: :class:`str`
    """
    __slots__ = ("title", "post_id", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.title = data["title"]
        self.post_id = data["post_id"]
        self.cover_url = data["cover_url"]


class UserAchievementUnlockDetails(NotificationsDetailsBase):
    """
    New achievement unlocked

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    achievement_id: :class:`int`

    achievement_mode: Optional[:class:`GameModeStr`]

    cover_url: :class:`str`

    slug: :class:`str`

    title: :class:`str`

    user_id: :class:`int`
    """
    __slots__ = (
        "achievement_id", "achievement_mode", "cover_url",
        "slug", "title", "user_id"
    )

    def __init__(self, data):
        super().__init__(data)
        self.achievement_id = data["achievement_id"]
        self.achievement_mode = GameModeStr(data["achievement_mode"]) \
            if data["achievement_mode"] is not None else None
        self.cover_url = data["cover_url"]
        self.slug = data["slug"]
        self.title = data["title"]
        self.user_id = data["user_id"]


class UserBeatmapsetNewDetails(NotificationsDetailsBase):
    """
    New beatmapset

    Extends: :class:`NotificationsDetailsBase`

    **Attributes**

    beatmapset_id: :class:`int`

    title: :class:`str`

    title_unicode: :class:`str`

    cover_url: :class:`str`
    """
    __slots__ = ("beatmapset_id", "title", "title_unicode", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.beatmapset_id = data["beatmapset_id"]
        self.title = data["title"]
        self.title_unicode = data["title_unicode"]
        self.cover_url = data["cover_url"]
        self.username = data.get("username")


class BeatmapsetDiscussionLockDetails(BeatmapsetNotificationDetails):
    """
    Beatmapset discussion locked

    Extends :class:`BeatmapsetNotificationDetails`
    """


class BeatmapsetDiscussionPostNewDetails(BeatmapsetDiscussionPostNotificationDetails):
    """
    New beatmapset discussion post

    Extends :class:`BeatmapsetDiscussionPostNotificationDetails`
    """


class BeatmapsetDiscussionQualifiedProblemDetails(BeatmapsetDiscussionPostNotificationDetails):
    """
    Beatmapset discussion qualified problem

    Extends :class:`BeatmapsetDiscussionPostNotification`
    """


class BeatmapsetDiscussionUnlockDetails(BeatmapsetNotificationDetails):
    """
    Beatmapset discussion unlocked

    Extends :class:`BeatmapsetNotificationDetails`
    """


class BeatmapsetDisqualifyDetails(BeatmapsetNotificationDetails):
    """
    Beatmapset disqualified

    Extends :class:`BeatmapsetNotificationDetails`
    """


class BeatmapsetLoveDetails(BeatmapsetNotificationDetails):
    """
    Beatmapset loved

    Extends :class:`BeatmapsetNotificationDetails`
    """


class BeatmapsetNominateDetails(BeatmapsetNotificationDetails):
    """
    Beatmapset nominated

    Extends :class:`BeatmapsetNotificationDetails`
    """


class BeatmapsetQualifyDetails(BeatmapsetNotificationDetails):
    """
    Beatmapset qualified

    Extends :class:`BeatmapsetNotificationDetails`
    """


class BeatmapsetRankDetails(BeatmapsetNotificationDetails):
    """
    Beatmapset ranked

    Extends :class:`BeatmapsetNotificationDetails`
    """


class BeatmapsetRemoveFromLovedDetails(BeatmapsetNotificationDetails):
    """
    Beatmapset removed from love

    Extends :class:`BeatmapsetNotificationDetails`
    """


class BeatmapsetResetNominationsDetails(BeatmapsetNominateDetails):
    """
    Beatmapset nominations reset

    Extends :class:`BeatmapsetNominateDetails`
    """


class UserBeatmapsetReviveDetails(UserBeatmapsetNewDetails):
    """
    User beatmapset revived

    Extends :class:`UserBeatmapsetNewDetails`
    """


class Details:
    DETAIL_MAP = {
        NotificationType.BEATMAP_OWNER_CHANGE: BeatmapOwnerChangeDetails,
        NotificationType.BEATMAPSET_DISCUSSION_LOCK: BeatmapsetDiscussionLockDetails,
        NotificationType.BEATMAPSET_DISCUSSION_POST_NEW: BeatmapsetDiscussionPostNewDetails,
        NotificationType.BEATMAPSET_DISCUSSION_QUALIFIED_PROBLEM: BeatmapsetDiscussionQualifiedProblemDetails,
        NotificationType.BEATMAPSET_DISCUSSION_REVIEW_NEW: BeatmapsetDiscussionReviewNewDetails,
        NotificationType.BEATMAPSET_DISCUSSION_UNLOCK: BeatmapsetDiscussionUnlockDetails,
        NotificationType.BEATMAPSET_DISQUALIFY: BeatmapsetDisqualifyDetails,
        NotificationType.BEATMAPSET_LOVE: BeatmapsetLoveDetails,
        NotificationType.BEATMAPSET_NOMINATE: BeatmapsetNominateDetails,
        NotificationType.BEATMAPSET_QUALIFY: BeatmapsetQualifyDetails,
        NotificationType.BEATMAPSET_RANK: BeatmapsetRankDetails,
        NotificationType.BEATMAPSET_REMOVE_FROM_LOVED: BeatmapsetRemoveFromLovedDetails,
        NotificationType.BEATMAPSET_RESET_NOMINATIONS: BeatmapsetResetNominationsDetails,
        NotificationType.CHANNEL_ANNOUNCEMENT: ChannelAnnouncementDetails,
        NotificationType.CHANNEL_MESSAGE: ChannelMessageDetails,
        NotificationType.COMMENT_NEW: CommentNewDetails,
        NotificationType.FORUM_TOPIC_REPLY: ForumTopicReplyDetails,
        NotificationType.USER_ACHIEVEMENT_UNLOCK: UserAchievementUnlockDetails,
        NotificationType.USER_BEATMAPSET_NEW: UserBeatmapsetNewDetails,
        NotificationType.USER_BEATMAPSET_REVIVE: UserBeatmapsetReviveDetails,
    }

    def __new__(cls, data, detail_type):
        return cls.DETAIL_MAP[detail_type](data)
