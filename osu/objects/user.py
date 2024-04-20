from dateutil import parser
from typing import TYPE_CHECKING, List, Optional, NamedTuple
import math
from collections import namedtuple

from .group import UserGroup
from .forum import TextFormat
from ..util import prettify, get_optional, get_optional_list
from ..enums import GameModeStr, UserAccountHistoryType, UserRelationType


if TYPE_CHECKING:
    from datetime import datetime, date


class UserCompact:
    """
    Mainly used for embedding in certain responses to save additional api lookups.

    **Attributes**

    avatar_url: :class:`str`
        url of user's avatar

    country_code: :class:`str`
        two-letter code representing user's country

    default_group: :class:`str`
        Identifier of the default Group the user belongs to.

    id: :class:`int`
        unique identifier for user

    is_active: :class:`bool`
        has this account been active in the last x months?

    is_bot: :class:`bool`
        is this a bot account?

    is_deleted: :class:`bool`

    is_online: :class:`bool`
        is the user currently online? (either on lazer or the new website)

    is_supporter: :class:`bool`
        does this user have supporter?

    last_visit: Optional[:class:`datetime.datetime`]
        null if the user hides online presence

    pm_friends_only: :class:`bool`
        whether or not the user allows PM from other than friends

    profile_colour: Optional[:class:`str`]
        colour of username/profile highlight, hex code (e.g. #333333)

    username: :class:`str`
        user's display name

    account_history: Optional[List[:class:`UserAccountHistory`]]

    active_tournament_banner: Optional[:class:`ProfileBanner`]
        deprecated; use active_tournament_banners

    active_tournament_banners: Optional[List[:class:`ProfileBanner`]]

    badges: Optional[List[:class:`UserBadge`]]

    beatmap_playcounts_count: Optional[:class:`int`]

    blocks: Optional[List[:class:`UserRelations`]]

    comments_count: Optional[:class:`int`]

    country: Optional[:class:`Country`]

    cover: Optional[:class:`UserCover`]

    favourite_beatmapset_count: Optional[:class:`int`]

    follow_user_mapping: Optional[List[:class:`int`]]

    follower_count: Optional[:class:`int`]

    friends: Optional[List[UserRelations]]

    graveyard_beatmapset_count: Optional[:class:`int`]

    groups: Optional[List[:class:`UserGroup`]]

    guest_beatmapset_count: Optional[:class:`int`]

    is_admin: Optional[:class:`bool`]

    is_bng: Optional[:class:`bool`]

    is_gmt: Optional[:class:`bool`]

    is_limited_bn: Optional[:class:`bool`]

    is_moderator: Optional[:class:`bool`]

    is_nat: Optional[:class:`bool`]

    is_restricted: Optional[:class:`bool`]

    is_silenced: Optional[:class:`bool`]

    loved_beatmapset_count: Optional[:class:`int`]

    mapping_follower_count: Optional[:class:`int`]

    monthly_playcounts: Optional[List[:class:`UserMonthlyPlaycount`]]

    nominated_beatmapset_count: Optional[:class:`int`]

    page: Optional[:class:`TextFormat`]

    pending_beatmapset_count: Optional[:class:`int`]

    previous_usernames: Optional[List[:class:`str`]]

    rank_highest: Optional[:class:`RankHighest`]

    rank_history: Optional[:class:`RankHistory`]

    ranked_beatmapset_count: Optional[:class:`int`]

    replays_watched_counts: Optional[List[:class:`UserReplaysWatchedCount`]]

    scores_best_count: Optional[:class:`int`]

    scores_first_count: Optional[:class:`int`]

    scores_pinned_count: Optional[:class:`int`]

    scores_recent_count: Optional[:class:`int`]

    statistics: Optional[:class:`UserStatistics`]

    statistics_rulesets: Optional[:class:`UserStatisticsRulesets`]

    support_level: Optional[:class:`int`]

    unread_pm_count: Optional[:class:`int`]

    user_achievements: Optional[List[:class:`UserAchievement`]]

    user_preferences: Optional[:class:`UserPreferences`]
    """

    __slots__ = (
        "avatar_url",
        "country_code",
        "default_group",
        "id",
        "is_active",
        "is_bot",
        "is_deleted",
        "is_online",
        "is_supporter",
        "last_visit",
        "pm_friends_only",
        "profile_colour",
        "username",
        "account_history",
        "active_tournament_banner",
        "active_tournament_banners",
        "badges",
        "beatmap_playcounts_count",
        "blocks",
        "comments_count",
        "country",
        "cover",
        "favourite_beatmapset_count",
        "follow_user_mapping",
        "follower_count",
        "friends",
        "graveyard_beatmapset_count",
        "groups",
        "guest_beatmapset_count",
        "is_admin",
        "is_bng",
        "is_full_bn",
        "is_gmt",
        "is_limited_bn",
        "is_moderator",
        "is_nat",
        "is_restricted",
        "is_silenced",
        "loved_beatmapset_count",
        "mapping_follower_count",
        "monthly_playcounts",
        "nominated_beatmapset_count",
        "page",
        "pending_beatmapset_count",
        "previous_usernames",
        "rank_highest",
        "rank_history",
        "ranked_beatmapset_count",
        "replays_watched_counts",
        "scores_best_count",
        "scores_first_count",
        "scores_pinned_count",
        "scores_recent_count",
        "statistics",
        "statistics_rulesets",
        "support_level",
        "unread_pm_count",
        "user_achievements",
        "user_preferences",
    )

    def __init__(self, data):
        self.avatar_url: str = data["avatar_url"]
        self.country_code: str = data["country_code"]
        self.default_group: str = data["default_group"]
        self.id: int = data["id"]
        self.is_active: bool = data["is_active"]
        self.is_bot: bool = data["is_bot"]
        self.is_deleted: bool = data["is_deleted"]
        self.is_online: bool = data["is_online"]
        self.is_supporter: bool = data["is_supporter"]
        self.last_visit: Optional[datetime] = get_optional(data, "last_visit", parser.parse)
        self.pm_friends_only: bool = data["pm_friends_only"]
        self.profile_colour: Optional[str] = data["profile_colour"]
        self.username: str = data["username"]

        # Optional attributes
        self.account_history: Optional[List[UserAccountHistory]] = get_optional_list(
            data, "account_history", UserAccountHistory
        )
        self.active_tournament_banner: Optional[ProfileBanner] = get_optional(
            data, "active_tournament_banner", ProfileBanner
        )
        self.active_tournament_banners: Optional[List[ProfileBanner]] = get_optional_list(
            data, "active_tournament_banners", ProfileBanner
        )
        self.badges: Optional[List[UserBadge]] = get_optional_list(data, "badges", UserBadge)
        self.beatmap_playcounts_count: Optional[int] = data.get("beatmap_playcounts_count")
        self.blocks: Optional[List[UserRelations]] = get_optional_list(data, "blocks", UserRelations)
        self.comments_count: Optional[int] = data.get("comments_count")
        self.country: Optional[Country] = get_optional(data, "country", Country)
        self.cover: Optional[UserCover] = get_optional(data, "cover", UserCover)
        self.favourite_beatmapset_count: Optional[int] = data.get("favourite_beatmapset_count")
        self.follow_user_mapping: Optional[List[int]] = data.get("follower_user_mapping")
        self.follower_count: Optional[int] = data.get("follower_count")
        self.friends: Optional[List[UserRelations]] = get_optional_list(data, "friends", UserRelations)
        self.graveyard_beatmapset_count: Optional[int] = data.get("graveyard_beatmapset_count")
        self.groups: Optional[List[UserGroup]] = get_optional_list(data, "groups", UserGroup)
        self.guest_beatmapset_count: Optional[int] = data.get("guest_beatmapset_count")
        self.is_admin: Optional[bool] = data.get("is_admin")
        self.is_bng: Optional[bool] = data.get("is_bng")
        self.is_full_bn: Optional[bool] = data.get("is_full_bn")
        self.is_gmt: Optional[bool] = data.get("is_gmt")
        self.is_limited_bn: Optional[bool] = data.get("is_limited_bn")
        self.is_moderator: Optional[bool] = data.get("is_moderator")
        self.is_nat: Optional[bool] = data.get("is_nat")
        self.is_restricted: Optional[bool] = data.get("is_restricted")
        self.is_silenced: Optional[bool] = data.get("is_silenced")
        self.loved_beatmapset_count: Optional[int] = data.get("loved_beatmapset_count")
        self.mapping_follower_count: Optional[int] = data.get("mapping_follower_count")
        self.monthly_playcounts: Optional[List[UserMonthlyPlaycount]] = get_optional_list(
            data, "monthly_playcounts", UserMonthlyPlaycount
        )
        self.nominated_beatmapset_count: Optional[int] = data.get("nominated_beatmapset_count")
        self.page: Optional[TextFormat] = get_optional(data, "page", TextFormat)
        self.pending_beatmapset_count: Optional[int] = data.get("pending_beatmapset_count")
        self.previous_usernames: Optional[List[str]] = data.get("previous_usernames")
        self.rank_highest: Optional[RankHighest] = get_optional(data, "rank_highest", RankHighest)
        self.rank_history: Optional[RankHistory] = get_optional(data, "rank_history", RankHistory)
        self.ranked_beatmapset_count: Optional[int] = data.get("ranked_beatmapset_count")
        self.replays_watched_counts: Optional[List[UserReplaysWatchedCount]] = get_optional_list(
            data, "replays_watched_counts", UserReplaysWatchedCount
        )
        self.scores_best_count: Optional[int] = data.get("scores_best_count")
        self.scores_first_count: Optional[int] = data.get("scores_first_count")
        self.scores_pinned_count: Optional[int] = data.get("scores_pinned_count")
        self.scores_recent_count: Optional[int] = data.get("scores_recent_count")
        self.statistics: Optional[UserStatistics] = get_optional(data, "statistics", UserStatistics)
        self.statistics_rulesets: Optional[UserStatisticsRulesets] = get_optional(
            data, "statistics_rulesets", UserStatisticsRulesets
        )
        self.support_level: Optional[int] = data.get("support_level")
        self.unread_pm_count: Optional[int] = data.get("unread_pm_count")
        self.user_achievements: Optional[List[UserAchievement]] = get_optional_list(
            data, "user_achievements", UserAchievement
        )
        self.user_preferences: Optional[UserPreferences] = get_optional(data, "user_preferences", UserPreferences)

    def __repr__(self):
        return prettify(self, "username", "id")


class User(UserCompact):
    # TODO: playstyle enum, profile order enum
    """
    Represents a User. Extends :class:`UserCompact` with additional attributes.
    Includes `country`, `cover`, and `is_restricted` attributes of :class:`UserCompact`.

    **Attributes**

    cover_url: :class:`str`
        url of profile cover. Deprecated, use cover.url instead.

    discord: Optional[:class:`str`]

    has_supported: :class:`bool`
        Has been a supporter in the past

    interests: Optional[:class:`str`]

    join_date: :class:`datetime.datetime`

    kudosu: :class:`UserKudosu`

    location: Optional[:class:`str`]

    max_blocks: :class:`int`
        maximum number of users allowed to be blocked

    max_friends: :class:`int`
        maximum number of friends allowed to be added

    occupation: Optional[:class:`str`]

    playmode: :class:`GameModeStr`

    playstyle: List[:class:`str`]
        Device choices of the user.

    post_count: :class:`int`
        number of forum posts

    profile_order: List[:class:`str`]
        Ordered list of sections in user profile page. Sections consist of:
        me, recent_activity, beatmaps, historical, kudosu, top_ranks, medals

    title: Optional[:class:`str`]
        user-specific title

    title_url:  Optional[:class:`str`]

    twitter:  Optional[:class:`str`]

    website:  Optional[:class:`str`]
    """
    __slots__ = (
        "cover_url",
        "discord",
        "has_supported",
        "interests",
        "join_date",
        "kudosu",
        "location",
        "max_blocks",
        "max_friends",
        "occupation",
        "playmode",
        "playstyle",
        "post_count",
        "profile_order",
        "title",
        "title_url",
        "twitter",
        "website",
    )

    def __init__(self, data):
        super().__init__(data)
        self.cover_url: str = data.get("cover_url")
        self.discord: Optional[str] = data["discord"]
        self.has_supported: bool = data["has_supported"]
        self.interests: Optional[str] = data["interests"]
        self.join_date: datetime = parser.parse(data["join_date"])
        self.kudosu: UserKudosu = UserKudosu(data["kudosu"])
        self.location: Optional[str] = data["location"]
        self.max_blocks: int = data["max_blocks"]
        self.max_friends: int = data["max_friends"]
        self.occupation: Optional[str] = data["occupation"]
        self.playmode: GameModeStr = GameModeStr(data["playmode"])
        self.playstyle: List[str] = data["playstyle"]
        self.post_count: int = data["post_count"]
        self.profile_order: List[str] = data["profile_order"]
        self.title: Optional[str] = data["title"]
        self.title_url: Optional[str] = data["title_url"]
        self.twitter: Optional[str] = data["twitter"]
        self.website: Optional[str] = data["website"]


class UserPreferences:
    # TODO: enum for beatmapset_card_size, beatmapset_download, user_list_filter, user_list_sort, user_list_view
    """
    The settings preferences of a user

    audio_autoplay: :class:`bool`

    audio_muted: :class:`bool`

    audio_volume: :class:`float`

    beatmapset_card_size: :class:`str`
        normal or extra

    beatmapset_download: :class:`str`
        all, no_video, or direct

    beatmapset_show_nsfw: :class:`bool`

    beatmapset_title_show_original: :class:`bool`

    comments_show_deleted: :class:`bool`

    forum_posts_show_deleted: :class:`bool`

    profile_cover_expanded: :class:`bool`

    user_list_filter: :class:`str`
        all, online, or offline

    user_list_sort: :class:`str`
        last_visit, rank, or username

    user_list_view: :class:`str`
        brick, card, or list
    """
    __slots__ = (
        "audio_autoplay",
        "audio_muted",
        "audio_volume",
        "beatmapset_card_size",
        "beatmapset_download",
        "beatmapset_show_nsfw",
        "beatmapset_title_show_original",
        "comments_show_deleted",
        "forum_posts_show_deleted",
        "profile_cover_expanded",
        "user_list_filter",
        "user_list_sort",
        "user_list_view",
    )

    def __init__(self, data):
        self.audio_autoplay: bool = data["audio_autoplay"]
        self.audio_muted: bool = data["audio_muted"]
        self.audio_volume: float = data["audio_volume"]
        self.beatmapset_card_size: str = data["beatmapset_card_size"]
        self.beatmapset_download: str = data["beatmapset_download"]
        self.beatmapset_show_nsfw: bool = data["beatmapset_show_nsfw"]
        self.beatmapset_title_show_original: bool = data["beatmapset_title_show_original"]
        self.comments_show_deleted: bool = data["comments_show_deleted"]
        self.forum_posts_show_deleted: bool = data["forum_posts_show_deleted"]
        self.profile_cover_expanded: bool = data["profile_cover_expanded"]
        self.user_list_filter: str = data["user_list_filter"]
        self.user_list_sort: str = data["user_list_sort"]
        self.user_list_view: str = data["user_list_view"]


class UserRelations:
    """
    Info about relationship to a user

    **Attributes**

    target_id: :class:`int`
        zebra id

    relation_type: :class:`UserRelationType`

    mutual: :class:`bool`
    """

    __slots__ = ("target_id", "relation_type", "mutual")

    def __init__(self, data):
        self.target_id: int = data["target_id"]
        self.relation_type: UserRelationType = UserRelationType(data["relation_type"])
        self.mutual: bool = data["mutual"]


class ProfileBanner:
    """
    **Attributes**

    id: :class:`int`

    tournament_id: :class:`int`

    image: Optional[:class:`str`]

    image2x: Optional[:class:`str`]
    """

    __slots__ = ("id", "tournament_id", "image", "image2x")

    def __init__(self, data):
        self.id: int = data["id"]
        self.tournament_id: int = data["tournament_id"]
        self.image: Optional[str] = data["image"]
        self.image2x: Optional[str] = data["image@2x"]

    def __repr__(self):
        return prettify(self, "tournament_id")


class UserSilence:
    """
    **Attributes**

    id: :class:`int`
        id of this object.

    user_id: :class:`int`
        id of the User that was silenced
    """

    __slots__ = ("id", "user_id")

    def __init__(self, data):
        self.id: int = data["id"]
        self.user_id: int = data["user_id"]

    def __repr__(self):
        return prettify(self, "user_id")


class UserAccountHistory:
    """
    **Attributes**

    actor: Optional[:class:`UserCompact`]

    description: :class:`str`

    id: :class:`int`

    length: :class:`int`

    permanent: :class:`bool`

    supporting_url: Optional[:class:`str`]

    timestamp: :class:`datetime.datetime`

    type: :class:`UserAccountHistoryType`
    """

    __slots__ = (
        "actor",
        "description",
        "id",
        "length",
        "permanent",
        "supporting_url",
        "timestamp",
        "type",
    )

    def __init__(self, data):
        self.actor: Optional[UserCompact] = get_optional(data, "actor", UserCompact)
        self.description: str = data["description"]
        self.id: int = data["id"]
        self.length: int = data["length"]
        self.permanent: bool = data["permanent"]
        self.supporting_url: Optional[str] = data.get("supporting_url")
        self.timestamp: datetime = parser.parse(data["timestamp"])
        self.type: UserAccountHistoryType = UserAccountHistoryType(data["type"])

    def __repr__(self):
        return prettify(self, "type", "length")


class UserBadge:
    """
    **Attributes**

    awarded_at: :class:`datetime.datetime`

    description: :class:`str`

    image_url: :class:`str`

    image_2x_url: :class:`str`

    url: :class:`str`
    """

    __slots__ = ("awarded_at", "description", "image_url", "image_2x_url", "url")

    def __init__(self, data):
        self.awarded_at: datetime = parser.parse(data["awarded_at"])
        self.description: str = data["description"]
        self.image_url: str = data["image_url"]
        self.image_2x_url = data["image@2x_url"]
        self.url: str = data["url"]

    def __repr__(self):
        return prettify(self, "awarded_at")


class UserMonthlyPlaycount:
    """
    **Attributes**

    start_date: :class:`datetime.date`
        year-month-day format

    count: class:`int`
        playcount
    """

    __slots__ = ("start_date", "count")

    def __init__(self, data):
        self.start_date: date = parser.parse(data["start_date"]).date()
        self.count: int = data["count"]

    def __repr__(self):
        return prettify(self, "start_date", "count")


class UserStatistics:
    """
    A summary of various gameplay statistics for a User. Specific to a :class:`GameMode`

    **Attributes**

    count_300: :class:`int`

    count_100: :class:`int`

    count_50: :class:`int`

    count_miss: :class:`int`

    country_rank: Optional[:class:`int`]
        Current country rank according to pp.

     global_rank: Optional[:class:`int`]
        Current global rank according to pp.

    global_rank_exp: Optional[:class:`int`]
        Current global rank according to experimental pp.

    grade_counts: :class:`NamedTuple`
        Below are the attributes and their meanings.

        a: :class:`int`
            Number of A ranked scores.

        s: :class:`int`
            Number of S ranked scores.

        sh: :class:`int`
            Number of Silver S ranked scores.

        ss: :class:`int`
            Number of SS ranked scores.

        ssh: :class:`int`
            Number of Silver SS ranked scores.

    hit_accuracy: :class:`float`
        Hit accuracy percentage

    is_ranked: :class:`bool`
        Does the player have a rank

    level: :class:`NamedTuple`
        Has attributes 'current' (current level) and 'progress' (progress to next level).

    maximum_combo: :class:`int`
        Highest maximum combo.

    play_count: :class:`int`
        Number of maps played.

    play_time: :class:`int`
        Cumulative time played.

    pp: :class:`int`
        Performance points

    pp_exp: :class:`int`
        Experimental performance points (on lazer.ppy.sh)

    recommended_difficulty: :class:`float`
        Recommended difficulty for a player. This value is not received from the api, but locally calculated.
        The formula is pp^0.4 * 0.195

    recommended_difficulty_exp: :class:`float`
        Recommended difficulty based on the pp_exp value.

    ranked_score: :class:`int`
        Current ranked score.

    replays_watched_by_others: :class:`int`
        Number of replays watched by other users.

    total_hits: :class:`int`
        Total number of hits.

    total_score: :class:`int`
        Total score.

    user: Optional[:class:`UserCompact`]
        The associated user.

    variants: Optional[List[:class:`UserStatisticVariant`]]
    """

    __slots__ = (
        "grade_counts",
        "level",
        "hit_accuracy",
        "is_ranked",
        "maximum_combo",
        "play_count",
        "play_time",
        "pp",
        "global_rank",
        "ranked_score",
        "replays_watched_by_others",
        "total_hits",
        "total_score",
        "user",
        "country_rank",
        "global_rank_exp",
        "pp_exp",
        "count_100",
        "count_300",
        "count_50",
        "count_miss",
        "recommended_difficulty",
        "recommended_difficulty_exp",
        "variants",
    )

    def __init__(self, data):
        self.count_100: int = data["count_100"]
        self.count_300: int = data["count_300"]
        self.count_50: int = data["count_50"]
        self.count_miss: int = data["count_miss"]
        self.country_rank: Optional[int] = data.get("country_rank")
        self.global_rank: Optional[int] = data["global_rank"]
        self.global_rank_exp: Optional[int] = data.get("global_rank_exp")
        self.grade_counts: NamedTuple = namedtuple("GradeCounts", ("ssh", "ss", "sh", "s", "a"))(**data["grade_counts"])
        self.level: NamedTuple = namedtuple("Level", ("current", "progress"))(**data["level"])
        self.hit_accuracy: float = data["hit_accuracy"]
        self.is_ranked: bool = data["is_ranked"]
        self.maximum_combo: int = data["maximum_combo"]
        self.play_count: int = data["play_count"]
        self.play_time: int = data["play_time"]
        self.pp: int = data["pp"]
        self.pp_exp: int = data.get("pp_exp")
        self.recommended_difficulty: float = math.pow(self.pp, 0.4) * 0.195
        self.recommended_difficulty_exp: float = math.pow(self.pp_exp, 0.4) * 0.195 if self.pp_exp is not None else None
        self.ranked_score: int = data["ranked_score"]
        self.replays_watched_by_others: int = data["replays_watched_by_others"]
        self.total_hits: int = data["total_hits"]
        self.total_score: int = data["total_score"]
        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)
        self.variants: Optional[List[UserStatisticVariant]] = get_optional_list(data, "variants", UserStatisticVariant)

    def __repr__(self):
        return prettify(self, "pp", "global_rank", "user")


class UserStatisticVariant:
    """
    A variant ranking system.

    **Attributes**

    country_rank: Optional[:class:`int`]

    global_rank: Optional[:class:`int`]

    mode: :class:`GameModeStr`

    pp: :class:`int`

    variant: :class:`str`
        4k or 7k
    """

    __slots__ = ("country_rank", "global_rank", "mode", "pp", "variant")

    def __init__(self, data):
        self.country_rank: Optional[int] = data["country_rank"]
        self.global_rank: Optional[int] = data["global_rank"]
        self.mode: GameModeStr = GameModeStr(data["mode"])
        self.pp: int = data["pp"]
        self.variant: str = data["variant"]


class UserStatisticsRulesets:
    """
    Object that contains statistics for each gamemode.

    **Attributes**

    osu: Optional[:class:`UserStatistics`]
        statistics for osu!standard.

    taiko: Optional[:class:`UserStatistics`]
        statistics for osu!taiko.

    fruits: Optional[:class:`UserStatistics`]
        statistics for osu!catch.

    mania: Optional[:class:`UserStatistics`]
        statistics for osu!mania.
    """

    __slots__ = ("osu", "taiko", "fruits", "mania")

    def __init__(self, data):
        self.osu: Optional[UserStatistics] = get_optional(data, "osu", UserStatistics)
        self.taiko: Optional[UserStatistics] = get_optional(data, "taiko", UserStatistics)
        self.fruits: Optional[UserStatistics] = get_optional(data, "fruits", UserStatistics)
        self.mania: Optional[UserStatistics] = get_optional(data, "mania", UserStatistics)

    def __repr__(self):
        fields = [slot for slot in self.__slots__ if getattr(self, slot, None) is not None]
        return prettify(self, *fields)


class RankHighest:
    """
    Highest rank a player achieved at any point in time.

    **Attributes**

    rank: :class:`int`

    updated_at: :class:`datetime.datetime`
    """

    __slots__ = ("rank", "updated_at")

    def __init__(self, data):
        self.rank: int = data["rank"]
        self.updated_at: datetime = parser.parse(data["updated_at"])

    def __repr__(self):
        return prettify(self, "rank", "updated_at")


class UserAchievement:
    """
    An achievement that a user received

    **Attributes**

    achieved_at: :class:`datetime.datetime`

    achievement_id: :class:`int`
    """

    __slots__ = ("achieved_at", "achievement_id")

    def __init__(self, data):
        self.achieved_at: datetime = parser.parse(data["achieved_at"])
        self.achievement_id: int = data["achievement_id"]

    def __repr__(self):
        return prettify(self, "achievement_id", "achieved_at")


class UserReplaysWatchedCount:
    """
    The count of replays watched for a month

    **Attributes**

    start_date: :class:`datetime.datetime`

    count: :class:`int`
    """

    __slots__ = ("start_date", "count")

    def __init__(self, data):
        self.start_date: datetime = parser.parse(data["start_date"])
        self.count: int = data["count"]

    def __repr__(self):
        return prettify(self, "count", "start_date")


class RankHistory:
    """
    Rank history data for a user

    **Attributes**

    mode: :class:`GameModeStr`

    data: List[:class:`int`]
        List of ranks from oldest to newest
    """

    __slots__ = ("mode", "data")

    def __init__(self, data):
        self.mode: GameModeStr = GameModeStr(data["mode"])
        self.data: List[int] = data["data"]

    def __repr__(self):
        return prettify(self, "mode", "data")


class UserCover:
    """
    Cover of a user's profile

    **Attributes**

    custom_url: Optional[:class:`str`]

    url: Optional[:class:`str`]

    id: Optional[:class:`int`]
    """

    __slots__ = ("custom_url", "url", "id")

    def __init__(self, data):
        self.custom_url: Optional[str] = data["custom_url"]
        self.url: Optional[str] = data["url"]
        self.id: Optional[int] = data.get("id")

    def __repr__(self):
        return prettify(self, "custom_url")


class Country:
    """
    Country data

    **Attributes**

    code: :class:`str`

    name: :class:`str`

    display: Optional[:class:`int`]
    """

    __slots__ = ("code", "name", "display")

    def __init__(self, data):
        self.code: str = data["code"]
        self.name: str = data["name"]
        self.display: Optional[int] = data.get("display")

    def __repr__(self):
        return prettify(self, "code", "name")


class UserKudosu:
    """
    User kudosu data

    **Attributes**

    total: :class:`int`

    available: :class:`int`
    """

    __slots__ = ("total", "available")

    def __init__(self, data):
        self.total: int = data["total"]
        self.available: int = data["available"]

    def __repr__(self):
        return prettify(self, "total", "available")
