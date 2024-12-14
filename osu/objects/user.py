from typing import TYPE_CHECKING, List, Optional, NamedTuple
import math
from collections import namedtuple

from .group import UserGroup
from .forum import TextFormat
from ..util import prettify, get_optional, get_optional_list, get_required, fromisoformat
from ..enums import GameModeStr, UserAccountHistoryType, UserRelationType


if TYPE_CHECKING:
    from datetime import datetime, date


__all__ = (
    "UserCompact",
    "User",
    "UserPreferences",
    "UserRelation",
    "ProfileBanner",
    "UserSilence",
    "UserAccountHistory",
    "UserBadge",
    "UserMonthlyPlaycount",
    "UserStatistics",
    "UserStatisticVariant",
    "UserStatisticsRulesets",
    "RankHighest",
    "UserAchievement",
    "UserReplaysWatchedCount",
    "RankHistory",
    "UserCover",
    "Country",
    "UserKudosu",
    "DailyChallengeUserStats",
)


class UserCompact:
    """
    Mainly used for embedding in certain responses to save additional api lookups.

    **Attributes**

    avatar_url: str
        url of user's avatar

    country_code: str
        two-letter code representing user's country

    default_group: str
        Identifier of the default Group the user belongs to.

    id: int
        unique identifier for user

    is_active: bool
        has this account been active in the last x months?

    is_bot: bool
        is this a bot account?

    is_deleted: bool

    is_online: bool
        is the user currently online? (either on lazer or the new website)

    is_supporter: bool
        does this user have supporter?

    last_visit: Optional[:py:class:`datetime.datetime`]
        null if the user hides online presence

    pm_friends_only: bool
        whether or not the user allows PM from other than friends

    profile_colour: Optional[str]
        colour of username/profile highlight, hex code (e.g. #333333)

    username: str
        user's display name

    account_history: Optional[List[:class:`UserAccountHistory`]]

    active_tournament_banner: Optional[:class:`ProfileBanner`]
        deprecated; use active_tournament_banners

    active_tournament_banners: Optional[List[:class:`ProfileBanner`]]

    badges: Optional[List[:class:`UserBadge`]]

    beatmap_playcounts_count: Optional[int]

    blocks: Optional[List[:class:`UserRelations`]]

    comments_count: Optional[int]

    country: Optional[:class:`Country`]

    cover: Optional[:class:`UserCover`]

    daily_challenge_user_stats: Optional[:class:`DailyChallengeUserStats`]

    favourite_beatmapset_count: Optional[int]

    follow_user_mapping: Optional[List[int]]

    follower_count: Optional[int]

    friends: Optional[List[:class:`UserRelation`]]

    graveyard_beatmapset_count: Optional[int]

    groups: Optional[List[:class:`UserGroup`]]

    guest_beatmapset_count: Optional[int]

    is_admin: Optional[bool]

    is_bng: Optional[bool]

    is_gmt: Optional[bool]

    is_limited_bn: Optional[bool]

    is_moderator: Optional[bool]

    is_nat: Optional[bool]

    is_restricted: Optional[bool]

    is_silenced: Optional[bool]

    loved_beatmapset_count: Optional[int]

    mapping_follower_count: Optional[int]

    monthly_playcounts: Optional[List[:class:`UserMonthlyPlaycount`]]

    nominated_beatmapset_count: Optional[int]

    page: Optional[:class:`TextFormat`]

    pending_beatmapset_count: Optional[int]

    previous_usernames: Optional[List[str]]

    rank_highest: Optional[:class:`RankHighest`]

    rank_history: Optional[:class:`RankHistory`]

    ranked_beatmapset_count: Optional[int]

    replays_watched_counts: Optional[List[:class:`UserReplaysWatchedCount`]]

    scores_best_count: Optional[int]

    scores_first_count: Optional[int]

    scores_pinned_count: Optional[int]

    scores_recent_count: Optional[int]

    statistics: Optional[:class:`UserStatistics`]

    statistics_rulesets: Optional[:class:`UserStatisticsRulesets`]

    support_level: Optional[int]

    unread_pm_count: Optional[int]

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
        "daily_challenge_user_stats",
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
        self.avatar_url: str = get_required(data, "avatar_url")
        self.country_code: str = get_required(data, "country_code")
        self.default_group: str = get_required(data, "default_group")
        self.id: int = get_required(data, "id")
        self.is_active: bool = get_required(data, "is_active")
        self.is_bot: bool = get_required(data, "is_bot")
        self.is_deleted: bool = get_required(data, "is_deleted")
        self.is_online: bool = get_required(data, "is_online")
        self.is_supporter: bool = get_required(data, "is_supporter")
        self.last_visit: Optional[datetime] = get_optional(data, "last_visit", fromisoformat)
        self.pm_friends_only: bool = get_required(data, "pm_friends_only")
        self.profile_colour: Optional[str] = get_required(data, "profile_colour")
        self.username: str = get_required(data, "username")

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
        self.blocks: Optional[List[UserRelation]] = get_optional_list(data, "blocks", UserRelation)
        self.comments_count: Optional[int] = data.get("comments_count")
        self.country: Optional[Country] = get_optional(data, "country", Country)
        self.cover: Optional[UserCover] = get_optional(data, "cover", UserCover)
        self.daily_challenge_user_stats: Optional[DailyChallengeUserStats] = get_optional(
            data, "daily_challenge_user_stats", DailyChallengeUserStats
        )
        self.favourite_beatmapset_count: Optional[int] = data.get("favourite_beatmapset_count")
        self.follow_user_mapping: Optional[List[int]] = data.get("follower_user_mapping")
        self.follower_count: Optional[int] = data.get("follower_count")
        self.friends: Optional[List[UserRelation]] = get_optional_list(data, "friends", UserRelation)
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

    cover_url: str
        url of profile cover. Deprecated, use cover.url instead.

    discord: Optional[str]

    has_supported: bool
        Has been a supporter in the past

    interests: Optional[str]

    join_date: :py:class:`datetime.datetime`

    kudosu: :class:`UserKudosu`

    location: Optional[str]

    max_blocks: int
        maximum number of users allowed to be blocked

    max_friends: int
        maximum number of friends allowed to be added

    occupation: Optional[str]

    playmode: :class:`GameModeStr`

    playstyle: List[str]
        Device choices of the user.

    post_count: int
        number of forum posts

    profile_hue: Optional[int]
        Custom color hue in HSL degrees (0-359).

    profile_order: List[str]
        Ordered list of sections in user profile page. Sections consist of:
        me, recent_activity, beatmaps, historical, kudosu, top_ranks, medals

    title: Optional[str]
        user-specific title

    title_url:  Optional[str]

    twitter:  Optional[str]

    website:  Optional[str]
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
        "profile_hue",
        "profile_order",
        "title",
        "title_url",
        "twitter",
        "website",
    )

    def __init__(self, data):
        super().__init__(data)
        self.cover_url: str = data.get("cover_url")
        self.discord: Optional[str] = get_required(data, "discord")
        self.has_supported: bool = get_required(data, "has_supported")
        self.interests: Optional[str] = get_required(data, "interests")
        self.join_date: datetime = fromisoformat(get_required(data, "join_date"))
        self.kudosu: UserKudosu = UserKudosu(get_required(data, "kudosu"))
        self.location: Optional[str] = get_required(data, "location")
        self.max_blocks: int = get_required(data, "max_blocks")
        self.max_friends: int = get_required(data, "max_friends")
        self.occupation: Optional[str] = get_required(data, "occupation")
        self.playmode: GameModeStr = GameModeStr(get_required(data, "playmode"))
        self.playstyle: List[str] = get_required(data, "playstyle")
        self.post_count: int = get_required(data, "post_count")
        self.profile_hue: Optional[int] = get_required(data, "profile_hue")
        self.profile_order: List[str] = get_required(data, "profile_order")
        self.title: Optional[str] = get_required(data, "title")
        self.title_url: Optional[str] = get_required(data, "title_url")
        self.twitter: Optional[str] = get_required(data, "twitter")
        self.website: Optional[str] = get_required(data, "website")


class UserPreferences:
    # TODO: enum for beatmapset_card_size, beatmapset_download, user_list_filter, user_list_sort, user_list_view
    """
    The settings preferences of a user

    audio_autoplay: bool

    audio_muted: bool

    audio_volume: float

    beatmapset_card_size: str
        normal or extra

    beatmapset_download: str
        all, no_video, or direct

    beatmapset_show_nsfw: bool

    beatmapset_title_show_original: bool

    comments_show_deleted: bool

    forum_posts_show_deleted: bool

    profile_cover_expanded: bool

    user_list_filter: str
        all, online, or offline

    user_list_sort: str
        last_visit, rank, or username

    user_list_view: str
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
        self.audio_autoplay: bool = get_required(data, "audio_autoplay")
        self.audio_muted: bool = get_required(data, "audio_muted")
        self.audio_volume: float = get_required(data, "audio_volume")
        self.beatmapset_card_size: str = get_required(data, "beatmapset_card_size")
        self.beatmapset_download: str = get_required(data, "beatmapset_download")
        self.beatmapset_show_nsfw: bool = get_required(data, "beatmapset_show_nsfw")
        self.beatmapset_title_show_original: bool = get_required(data, "beatmapset_title_show_original")
        self.comments_show_deleted: bool = get_required(data, "comments_show_deleted")
        self.forum_posts_show_deleted: bool = get_required(data, "forum_posts_show_deleted")
        self.profile_cover_expanded: bool = get_required(data, "profile_cover_expanded")
        self.user_list_filter: str = get_required(data, "user_list_filter")
        self.user_list_sort: str = get_required(data, "user_list_sort")
        self.user_list_view: str = get_required(data, "user_list_view")

    def __repr__(self):
        return prettify(self)


class UserRelation:
    """
    Info about relationship to a user

    **Attributes**

    target_id: int
        zebra id

    relation_type: :class:`UserRelationType`

    mutual: bool

    target: Optional[:class:`UserCompact`]
    """

    __slots__ = ("target_id", "relation_type", "mutual", "target")

    def __init__(self, data):
        self.target_id: int = get_required(data, "target_id")
        self.relation_type: UserRelationType = UserRelationType(get_required(data, "relation_type"))
        self.mutual: bool = get_required(data, "mutual")
        self.target: Optional[UserCompact] = get_optional(data, "target", UserCompact)

    def __repr__(self):
        return prettify(self, "target_id" if self.target is None else "target", "mutual")


# legacy support for the old name of the class
UserRelations = UserRelation


class ProfileBanner:
    """
    **Attributes**

    id: int

    tournament_id: int

    image: Optional[str]

    image2x: Optional[str]
    """

    __slots__ = ("id", "tournament_id", "image", "image2x")

    def __init__(self, data):
        self.id: int = get_required(data, "id")
        self.tournament_id: int = get_required(data, "tournament_id")
        self.image: Optional[str] = get_required(data, "image")
        self.image2x: Optional[str] = data["image@2x"]

    def __repr__(self):
        return prettify(self, "tournament_id")


class UserSilence:
    """
    A record indicating a :class:`User` was silenced.

    **Attributes**

    id: int
        id of this object.

    user_id: int
        id of the User that was silenced
    """

    __slots__ = ("id", "user_id")

    def __init__(self, data):
        self.id: int = get_required(data, "id")
        self.user_id: int = get_required(data, "user_id")

    def __repr__(self):
        return prettify(self, "user_id")


class UserAccountHistory:
    """
    **Attributes**

    actor: Optional[:class:`UserCompact`]

    description: str

    id: int

    length: int

    permanent: bool

    supporting_url: Optional[str]

    timestamp: :py:class:`datetime.datetime`

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
        self.description: str = get_required(data, "description")
        self.id: int = get_required(data, "id")
        self.length: int = get_required(data, "length")
        self.permanent: bool = get_required(data, "permanent")
        self.supporting_url: Optional[str] = data.get("supporting_url")
        self.timestamp: datetime = fromisoformat(get_required(data, "timestamp"))
        self.type: UserAccountHistoryType = UserAccountHistoryType(get_required(data, "type"))

    def __repr__(self):
        return prettify(self, "type", "length")


class UserBadge:
    """
    **Attributes**

    awarded_at: :py:class:`datetime.datetime`

    description: str

    image_url: str

    image_2x_url: str

    url: str
    """

    __slots__ = ("awarded_at", "description", "image_url", "image_2x_url", "url")

    def __init__(self, data):
        self.awarded_at: datetime = fromisoformat(get_required(data, "awarded_at"))
        self.description: str = get_required(data, "description")
        self.image_url: str = get_required(data, "image_url")
        self.image_2x_url = data["image@2x_url"]
        self.url: str = get_required(data, "url")

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
        self.start_date: date = fromisoformat(get_required(data, "start_date")).date()
        self.count: int = get_required(data, "count")

    def __repr__(self):
        return prettify(self, "start_date", "count")


class UserStatistics:
    """
    A summary of various gameplay statistics for a User. Specific to a :class:`GameMode`

    **Attributes**

    count_300: int

    count_100: int

    count_50: int

    count_miss: int

    country_rank: Optional[int]
        Current country rank according to pp.

     global_rank: Optional[int]
        Current global rank according to pp.

    global_rank_exp: Optional[int]
        Current global rank according to experimental pp (not used anymore).

    grade_counts: :class:`NamedTuple`
        Below are the attributes and their meanings.

        a: int
            Number of A ranked scores.

        s: int
            Number of S ranked scores.

        sh: int
            Number of Silver S ranked scores.

        ss: int
            Number of SS ranked scores.

        ssh: int
            Number of Silver SS ranked scores.

    hit_accuracy: float
        Hit accuracy percentage

    is_ranked: bool
        Does the player have a rank

    level: :class:`NamedTuple`
        Has attributes 'current' (current level) and 'progress' (progress to next level).

    maximum_combo: int
        Highest maximum combo.

    play_count: int
        Number of maps played.

    play_time: int
        Cumulative time played.

    pp: int
        Performance points

    pp_exp: Optional[int]
        Experimental performance points (not used anymore)

    rank_change_since_30_days: Optional[int]

    recommended_difficulty: float
        Recommended difficulty for a player. This value is not received from the api, but locally calculated.
        The formula is pp^0.4 * 0.195

    recommended_difficulty_exp: float
        Recommended difficulty based on the pp_exp value.

    ranked_score: int
        Current ranked score.

    replays_watched_by_others: int
        Number of replays watched by other users.

    total_hits: int
        Total number of hits.

    total_score: int
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
        "rank_change_since_30_days",
    )

    def __init__(self, data):
        self.count_100: int = get_required(data, "count_100")
        self.count_300: int = get_required(data, "count_300")
        self.count_50: int = get_required(data, "count_50")
        self.count_miss: int = get_required(data, "count_miss")
        self.country_rank: Optional[int] = data.get("country_rank")
        self.global_rank: Optional[int] = get_required(data, "global_rank")
        self.global_rank_exp: Optional[int] = data.get("global_rank_exp")
        self.grade_counts: NamedTuple = namedtuple("GradeCounts", ("ssh", "ss", "sh", "s", "a"))(
            **get_required(data, "grade_counts")
        )
        self.level: NamedTuple = namedtuple("Level", ("current", "progress"))(**get_required(data, "level"))
        self.hit_accuracy: float = get_required(data, "hit_accuracy")
        self.is_ranked: bool = get_required(data, "is_ranked")
        self.maximum_combo: int = get_required(data, "maximum_combo")
        self.play_count: int = get_required(data, "play_count")
        self.play_time: int = get_required(data, "play_time")
        self.pp: int = get_required(data, "pp")
        self.pp_exp: Optional[int] = data.get("pp_exp")
        self.recommended_difficulty: float = math.pow(self.pp, 0.4) * 0.195
        self.recommended_difficulty_exp: float = math.pow(self.pp_exp, 0.4) * 0.195 if self.pp_exp is not None else None
        self.ranked_score: int = get_required(data, "ranked_score")
        self.replays_watched_by_others: int = get_required(data, "replays_watched_by_others")
        self.total_hits: int = get_required(data, "total_hits")
        self.total_score: int = get_required(data, "total_score")
        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)
        self.variants: Optional[List[UserStatisticVariant]] = get_optional_list(data, "variants", UserStatisticVariant)
        self.rank_change_since_30_days: Optional[int] = data.get("rank_change_since_30_days")

    def __repr__(self):
        return prettify(self, "pp", "global_rank", "user")


class UserStatisticVariant:
    """
    A variant ranking system.

    **Attributes**

    country_rank: Optional[int]

    global_rank: Optional[int]

    mode: :class:`GameModeStr`

    pp: int

    variant: str
        4k or 7k
    """

    __slots__ = ("country_rank", "global_rank", "mode", "pp", "variant")

    def __init__(self, data):
        self.country_rank: Optional[int] = get_required(data, "country_rank")
        self.global_rank: Optional[int] = get_required(data, "global_rank")
        self.mode: GameModeStr = GameModeStr(get_required(data, "mode"))
        self.pp: int = get_required(data, "pp")
        self.variant: str = get_required(data, "variant")


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

    rank: int

    updated_at: :py:class:`datetime.datetime`
    """

    __slots__ = ("rank", "updated_at")

    def __init__(self, data):
        self.rank: int = get_required(data, "rank")
        self.updated_at: datetime = fromisoformat(get_required(data, "updated_at"))

    def __repr__(self):
        return prettify(self, "rank", "updated_at")


class UserAchievement:
    """
    An achievement that a user received

    **Attributes**

    achieved_at: :py:class:`datetime.datetime`

    achievement_id: int
    """

    __slots__ = ("achieved_at", "achievement_id")

    def __init__(self, data):
        self.achieved_at: datetime = fromisoformat(get_required(data, "achieved_at"))
        self.achievement_id: int = get_required(data, "achievement_id")

    def __repr__(self):
        return prettify(self, "achievement_id", "achieved_at")


class UserReplaysWatchedCount:
    """
    The count of replays watched for a month

    **Attributes**

    start_date: :py:class:`datetime.datetime`

    count: int
    """

    __slots__ = ("start_date", "count")

    def __init__(self, data):
        self.start_date: datetime = fromisoformat(get_required(data, "start_date"))
        self.count: int = get_required(data, "count")

    def __repr__(self):
        return prettify(self, "count", "start_date")


class RankHistory:
    """
    Rank history data for a user

    **Attributes**

    mode: :class:`GameModeStr`

    data: List[int]
        List of ranks from oldest to newest
    """

    __slots__ = ("mode", "data")

    def __init__(self, data):
        self.mode: GameModeStr = GameModeStr(get_required(data, "mode"))
        self.data: List[int] = get_required(data, "data")

    def __repr__(self):
        return prettify(self, "mode", "data")


class UserCover:
    """
    Cover of a user's profile

    **Attributes**

    custom_url: Optional[str]

    url: Optional[str]

    id: Optional[int]
    """

    __slots__ = ("custom_url", "url", "id")

    def __init__(self, data):
        self.custom_url: Optional[str] = get_required(data, "custom_url")
        self.url: Optional[str] = get_required(data, "url")
        self.id: Optional[int] = data.get("id")

    def __repr__(self):
        return prettify(self, "custom_url")


class Country:
    """
    Country data

    **Attributes**

    code: str

    name: str

    display: Optional[int]
    """

    __slots__ = ("code", "name", "display")

    def __init__(self, data):
        self.code: str = get_required(data, "code")
        self.name: str = get_required(data, "name")
        self.display: Optional[int] = data.get("display")

    def __repr__(self):
        return prettify(self, "code", "name")


class UserKudosu:
    """
    User kudosu data

    **Attributes**

    total: int

    available: int
    """

    __slots__ = ("total", "available")

    def __init__(self, data):
        self.total: int = get_required(data, "total")
        self.available: int = get_required(data, "available")

    def __repr__(self):
        return prettify(self, "total", "available")


class DailyChallengeUserStats:
    """
    Daily challenge stats of a user

    **Attributes**

    daily_streak_best: int

    daily_streak_current: int

    last_update: Optional[:py:class:`datetime.datetime`]

    last_weekly_streak: Optional[:py:class:`datetime.datetime`]

    playcount: int

    top_10p_placements: int

    top_50p_placements: int

    user_id: int

    weekly_streak_best: int

    weekly_streak_current: int
    """

    __slots__ = (
        "daily_streak_best",
        "daily_streak_current",
        "last_update",
        "last_weekly_streak",
        "playcount",
        "top_10p_placements",
        "top_50p_placements",
        "user_id",
        "weekly_streak_best",
        "weekly_streak_current",
    )

    def __init__(self, data):
        self.daily_streak_best: int = get_required(data, "daily_streak_best")
        self.daily_streak_current: int = get_required(data, "daily_streak_current")
        self.last_update: Optional[datetime] = get_optional(data, "last_update", fromisoformat)
        self.last_weekly_streak: Optional[datetime] = get_optional(data, "last_weekly_streak", fromisoformat)
        self.playcount: int = get_required(data, "playcount")
        self.top_10p_placements: int = get_required(data, "top_10p_placements")
        self.top_50p_placements: int = get_required(data, "top_50p_placements")
        self.user_id: int = get_required(data, "user_id")
        self.weekly_streak_best: int = get_required(data, "weekly_streak_best")
        self.weekly_streak_current: int = get_required(data, "weekly_streak_current")

    def __repr__(self):
        return prettify(self, "daily_streak_best", "daily_streak_current")
