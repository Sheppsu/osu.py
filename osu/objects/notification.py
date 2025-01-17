from typing import Optional, TYPE_CHECKING, Union

from ..util import prettify, get_optional, get_required, fromisoformat
from ..enums import (
    NotificationCategory,
    ObjectType,
    NotificationType,
    ChatChannelType,
    GameModeStr,
)


if TYPE_CHECKING:
    from datetime import datetime


__all__ = (
    "Notification",
    "ReadNotification",
    "NotificationsDetailsBase",
    "BeatmapOwnerChangeDetails",
    "BeatmapsetNotificationDetails",
    "BeatmapsetDiscussionPostNotificationDetails",
    "ReviewStats",
    "BeatmapsetDiscussionReviewNewDetails",
    "ChannelAnnouncementDetails",
    "ChannelMessageDetails",
    "CommentNewDetails",
    "ForumTopicReplyDetails",
    "UserAchievementUnlockDetails",
    "UserBeatmapsetNewDetails",
    "BeatmapsetDiscussionLockDetails",
    "BeatmapsetDiscussionPostNewDetails",
    "BeatmapsetDiscussionQualifiedProblemDetails",
    "BeatmapsetDiscussionUnlockDetails",
    "BeatmapsetDisqualifyDetails",
    "BeatmapsetLoveDetails",
    "BeatmapsetNominateDetails",
    "BeatmapsetQualifyDetails",
    "BeatmapsetRankDetails",
    "BeatmapsetRemoveFromLovedDetails",
    "BeatmapsetResetNominationsDetails",
    "UserBeatmapsetReviveDetails",
)


class Notification:
    """
    Represents a notification object.
    Go to :class:`Details` object to see details for each event

    **Attributes**

    id: int

    name: :class:`NotificationType`
        The type of event

    created_at: :py:class:`datetime.datetime`

    object_type: :class:`ObjectType`

    object_id: int

    source_user_id: Optional[int]

    is_read: bool

    details: Union[
    :class:`BeatmapOwnerChangeDetails`, :class:`BeatmapsetDiscussionLockDetails`,
    :class:`BeatmapsetDiscussionPostNewDetails`, :class:`BeatmapsetDiscussionQualifiedProblemDetails`,
    :class:`BeatmapsetDiscussionReviewNewDetails`, :class:`BeatmapsetDiscussionUnlockDetails`,
    :class:`BeatmapsetDisqualifyDetails`, :class:`BeatmapsetLoveDetails`,
    :class:`BeatmapsetNominateDetails`, :class:`BeatmapsetQualifyDetails`,
    :class:`BeatmapsetRankDetails`, :class:`BeatmapsetRemoveFromLovedDetails`,
    :class:`BeatmapsetResetNominationsDetails`, :class:`ChannelAnnouncementDetails`,
    :class:`ChannelMessageDetails`, :class:`CommentNewDetails`,
    :class:`ForumTopicReplyDetails`, :class:`UserAchievementUnlockDetails`,
    :class:`UserBeatmapsetNewDetails`, :class:`UserBeatmapsetReviveDetails`
    ]

        Details of the notification.

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
        "id",
        "name",
        "created_at",
        "object_type",
        "object_id",
        "is_read",
        "source_user_id",
        "details",
    )

    def __init__(self, data):
        self.id: int = get_required(data, "id")
        self.name: NotificationType = NotificationType(get_required(data, "name"))
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.object_type: ObjectType = ObjectType(get_required(data, "object_type"))
        self.object_id: int = get_required(data, "object_id")
        self.source_user_id: Optional[int] = data.get("source_user_id")
        self.is_read: bool = get_required(data, "is_read")
        self.details: _DETAILS_TYPE = _get_details_object(get_required(data, "details"), self.name)

    def __repr__(self):
        return prettify(self, "name", "details")


class ReadNotification:
    """
    Represents a read notification.

    **Attributes**

    category: :class:`NotificationCategory`

    id: int

    object_id: int

    object_type: :class:`ObjectType`
    """

    __slots__ = ("category", "id", "object_id", "object_type")

    def __init__(self, data):
        self.category: NotificationCategory = NotificationCategory(get_required(data, "category"))
        self.id: int = get_required(data, "id")
        self.object_id: int = get_required(data, "object_id")
        self.object_type: ObjectType = ObjectType(get_required(data, "object_type"))

    def __repr__(self):
        return prettify(self, "id")


class NotificationsDetailsBase:
    """
    Base class for all Detail objects.

    **Attributes**

    username: str
    """

    __slots__ = ("username",)

    def __init__(self, data):
        self.username: str = get_required(data, "username")

    def __repr__(self):
        # all the subclasses have a title attribute
        return prettify(self, "title", "username")


class BeatmapOwnerChangeDetails(NotificationsDetailsBase):
    """
    When ownership of a beatmap is transferred (for guest difficulties).

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    beatmap_id: int

    cover_url: str

    title: str

    title_unicode: str

    version: str
    """

    __slots__ = ("beatmap_id", "cover_url", "title", "title_unicode", "version")

    def __init__(self, data):
        super().__init__(data)
        self.beatmap_id: int = get_required(data, "beatmap_id")
        self.cover_url: str = get_required(data, "cover_url")
        self.title: str = get_required(data, "title")
        self.title_unicode: str = get_required(data, "title_unicode")
        self.version: str = get_required(data, "version")


class BeatmapsetNotificationDetails(NotificationsDetailsBase):
    """
    Base class for several other detail objects.

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    title: str

    title_unicode: str

    cover_url: str
    """

    __slots__ = ("title", "title_unicode", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.title: str = get_required(data, "title")
        self.title_unicode: str = get_required(data, "title_unicode")
        self.cover_url: str = get_required(data, "cover_url")


class BeatmapsetDiscussionPostNotificationDetails(NotificationsDetailsBase):
    """
    Base class for a couple other detail objects.

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    content: str

    title: str

    title_unicode: str

    post_id: int

    discussion_id: int

    beatmap_id: int

    cover_url: str
    """

    __slots__ = (
        "content",
        "title",
        "title_unicode",
        "post_id",
        "discussion_id",
        "beatmap_id",
        "cover_url",
    )

    def __init__(self, data):
        super().__init__(data)
        self.content: str = get_required(data, "content")
        self.title: str = get_required(data, "title")
        self.title_unicode: str = get_required(data, "title_unicode")
        self.post_id: int = get_required(data, "post_id")
        self.discussion_id: int = get_required(data, "discussion_id")
        self.beatmap_id: int = get_required(data, "beatmap_id")
        self.cover_url: str = get_required(data, "cover_url")


class ReviewStats:
    """
    **Attributes**

    praises: int

    suggestions: int

    problems: int
    """

    __slots__ = ("praises", "suggestions", "problems")

    def __init__(self, data):
        self.praises = get_required(data, "praises")
        self.suggestions = get_required(data, "suggestions")
        self.problems = get_required(data, "problems")


class BeatmapsetDiscussionReviewNewDetails(NotificationsDetailsBase):
    """
    New beatmapset discussion review.

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    title: str

    title_unicode: str

    post_id: int

    discussion_id: int

    beatmap_id: int

    cover_url: str

    embeds: :class:`ReviewStats`
    """

    __slots__ = (
        "title",
        "title_unicode",
        "post_id",
        "discussion_id",
        "beatmap_id",
        "cover_url",
        "embeds",
    )

    def __init__(self, data):
        super().__init__(data)
        self.title: str = get_required(data, "title")
        self.title_unicode: str = get_required(data, "title_unicode")
        self.post_id: int = get_required(data, "post_id")
        self.discussion_id: int = get_required(data, "discussion_id")
        self.beatmap_id: int = get_required(data, "beatmap_id")
        self.cover_url: str = get_required(data, "cover_url")
        self.embeds: ReviewStats = ReviewStats(get_required(data, "embeds"))


class ChannelAnnouncementDetails(NotificationsDetailsBase):
    """
    Chat channel announcement

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    channel_id: int

    name: str

    title: str

    type: :class:`ChatChannelType`

    cover_url: str
    """

    __slots__ = ("channel_id", "name", "title", "type", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.channel_id: int = get_required(data, "channel_id")
        self.name: str = get_required(data, "name")
        self.title: str = get_required(data, "title")
        self.type: ChatChannelType = ChatChannelType(get_required(data, "type").upper())
        self.cover_url: str = get_required(data, "cover_url")


class ChannelMessageDetails(NotificationsDetailsBase):
    """
    Chat channel message

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    title: str

    type: :class:`ChatChannelType`

    cover_url: str
    """

    __slots__ = ("title", "type", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.title: str = get_required(data, "title")
        self.type: ChatChannelType = ChatChannelType(get_required(data, "type").upper())
        self.cover_url: str = get_required(data, "cover_url")


class CommentNewDetails(NotificationsDetailsBase):
    """
    New comment

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    comment_id: int

    title: str

    content: str

    cover_url: str
    """

    __slots__ = ("comment_id", "title", "content", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.comment_id: int = get_required(data, "comment_id")
        self.title: str = get_required(data, "title")
        self.content: str = get_required(data, "content")
        self.cover_url: str = get_required(data, "cover_url")


class ForumTopicReplyDetails(NotificationsDetailsBase):
    """
    Forum topic reply

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    title: str

    post_id: int

    cover_url: str
    """

    __slots__ = ("title", "post_id", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.title: str = get_required(data, "title")
        self.post_id: int = get_required(data, "post_id")
        self.cover_url: str = get_required(data, "cover_url")


class UserAchievementUnlockDetails(NotificationsDetailsBase):
    """
    New achievement unlocked

    Extends :class:`NotificationsDetailsBase`

    **Attributes**

    achievement_id: int

    achievement_mode: Optional[:class:`GameModeStr`]

    cover_url: str

    slug: str

    title: str

    user_id: int
    """

    __slots__ = (
        "achievement_id",
        "achievement_mode",
        "cover_url",
        "slug",
        "title",
        "user_id",
    )

    def __init__(self, data):
        super().__init__(data)
        self.achievement_id: int = get_required(data, "achievement_id")
        self.achievement_mode: Optional[GameModeStr] = get_optional(data, "achievement_mode", GameModeStr)
        self.cover_url: str = get_required(data, "cover_url")
        self.slug: str = get_required(data, "slug")
        self.title: str = get_required(data, "title")
        self.user_id: int = get_required(data, "user_id")


class UserBeatmapsetNewDetails(NotificationsDetailsBase):
    """
    New beatmapset

    Extends: :class:`NotificationsDetailsBase`

    **Attributes**

    beatmapset_id: int

    title: str

    title_unicode: str

    cover_url: str
    """

    __slots__ = ("beatmapset_id", "title", "title_unicode", "cover_url")

    def __init__(self, data):
        super().__init__(data)
        self.beatmapset_id: int = get_required(data, "beatmapset_id")
        self.title: str = get_required(data, "title")
        self.title_unicode: str = get_required(data, "title_unicode")
        self.cover_url: str = get_required(data, "cover_url")


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


_DETAILS_TYPE = Union[
    BeatmapOwnerChangeDetails,
    BeatmapsetDiscussionLockDetails,
    BeatmapsetDiscussionPostNewDetails,
    BeatmapsetDiscussionQualifiedProblemDetails,
    BeatmapsetDiscussionReviewNewDetails,
    BeatmapsetDiscussionUnlockDetails,
    BeatmapsetDisqualifyDetails,
    BeatmapsetLoveDetails,
    BeatmapsetNominateDetails,
    BeatmapsetQualifyDetails,
    BeatmapsetRankDetails,
    BeatmapsetRemoveFromLovedDetails,
    BeatmapsetResetNominationsDetails,
    ChannelAnnouncementDetails,
    ChannelMessageDetails,
    CommentNewDetails,
    ForumTopicReplyDetails,
    UserAchievementUnlockDetails,
    UserBeatmapsetNewDetails,
    UserBeatmapsetReviveDetails,
]
_DETAIL_MAP = {
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


def _get_details_object(data, detail_type) -> _DETAILS_TYPE:
    return _DETAIL_MAP[detail_type](data)
