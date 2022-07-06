from .group import UserGroup
from ..util import Util
from dateutil import parser
import math


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

    last_visit: :class:`datetime.datetime`
        null if the user hides online presence

    pm_friends_only: :class:`bool`
        whether or not the user allows PM from other than friends

    profile_colour: :class:`str`
        colour of username/profile highlight, hex code (e.g. #333333)

    username: :class:`str`
        user's display name

    **Possible Attributes**

    account_history: Sequence[:class:`UserAccountHistory`]

    active_tournament_banner: :class:`ProfileBanner`

    badges: Sequence[:class:`UserBadge`]

    beatmap_playcounts_count: :class:`int`

    blocks

    country

    cover

    favourite_beatmapset_count: :class:`int`

    follower_count: :class:`int`

    mapping_follower_count: :class:`int`

    friends

    graveyard_beatmapset_count: :class:`int`

    groups: Sequencep[:class:`UserGroup`]

    is_restricted: :class:`bool`

    loved_beatmapset_count: :class:`int`

    monthly_playcounts: Sequence[:class:`UserMonthlyPlaycount`]

    page

    previous_usernames

    ranked_beatmapset_count

    replays_watched_counts

    scores_best_count: :class:`int`

    scores_first_count: :class:`int`

    scores_recent_count: :class:`int`

    statistics

    statistics_rulesets: :class:`UserStatisticsRulesets`

    support_level

    pending_beatmapset_count

    unread_pm_count

    user_achievements

    user_preferences

    rank_history
    """
    __slots__ = (
        'avatar_url', 'country_code', 'default_group', 'id', 'is_active', 'is_bot', 'is_deleted', 'is_online',
        'is_supporter', 'last_visit', 'pm_friends_only', 'profile_colour', 'username', 'account_history',
        'active_tournament_banner', 'badges', 'beatmap_playcounts_count', 'blocks', 'country', 'cover',
        'favourite_beatmapset_count', 'follower_count', 'mapping_follower_count', 'friends', 'graveyard_beatmapset_count', 'groups',
        'is_restricted', 'loved_beatmapset_count', 'monthly_playcounts', 'page', 'previous_usernames',
        'ranked_beatmapset_count', 'replays_watched_counts', 'scores_best_count', 'scores_first_count',
        'scores_recent_count', 'statistics', 'statistics_rulesets', 'support_level', 'pending_beatmapset_count',
        'unread_pm_count', 'user_achievements', 'user_preferences', 'rank_history', 'ranked_beatmapset_counts'
    )

    def __init__(self, data):
        self.avatar_url = data['avatar_url']
        self.country_code = data['country_code']
        self.default_group = data['default_group']
        self.id = data['id']
        self.is_active = data['is_active']
        self.is_bot = data['is_bot']
        self.is_deleted = data['is_deleted']
        self.is_online = data['is_online']
        self.is_supporter = data['is_supporter']
        self.last_visit = parser.parse(data['last_visit']) if data['last_visit'] is not None else None
        self.pm_friends_only = data['pm_friends_only']
        self.profile_colour = data['profile_colour']
        self.username = data['username']

        # Optional attributes
        self.active_tournament_banner = ProfileBanner(data['active_tournament_banner']) if data.get('active_tournament_banner') is not None else None
        self.account_history = list(map(UserAccountHistory, data.get('account_history', [])))
        self.badges = list(map(UserBadge, data.get('badges', [])))
        self.groups = list(map(UserGroup, data.get('groups', [])))
        self.monthly_playcounts = list(map(UserMonthlyPlaycount, data.get('monthly_playcounts', []))) if data.get("monthly_playcounts") is not None else None
        self.statistics = UserStatistics(data['statistics']) if 'statistics' in data else None
        self.page = data.get('page')
        self.pending_beatmapset_count = Util.int(data.get('pending_beatmapset_count'))
        self.previous_usernames = data.get('previous_usernames')
        self.rank_history = data.get('rank_history')
        self.ranked_beatmapset_counts = data.get('ranked_beatmapset_counts')
        self.replays_watched_counts = data.get('replays_watched_counts')
        self.scores_best_count = Util.int(data.get('scores_best_count'))
        self.scores_first_count = Util.int(data.get('scores_first_count'))
        self.scores_recent_count = Util.int(data.get('scores_recent_count'))
        self.statistics_rulesets = UserStatisticsRulesets(data['statistics_rulesets']) if 'statistics_rulesets' in data else None  # TODO
        self.support_level = data.get('support_level')
        self.unread_pm_count = Util.int(data.get('unread_pm_count'))
        self.user_achievements = data.get('user_achievements')
        self.user_preferences = data.get('user_preferences')
        self.beatmap_playcounts_count = Util.int(data.get('beatmap_playcounts_count'))
        self.blocks = data.get('blocks')
        self.country = data.get('country')
        self.cover = data.get('cover')
        self.favourite_beatmapset_count = Util.int(data.get('favourite_beatmapset_count'))
        self.follower_count = Util.int(data.get('follower_count'))
        self.mapping_follower_count = Util.int(data.get('mapping_follower_count'))
        self.friends = data.get('friends')
        self.graveyard_beatmapset_count = Util.int(data.get('graveyard_beatmapset_count'))
        self.is_restricted = data.get('is_restricted')
        self.loved_beatmapset_count = Util.int(data.get('loved_beatmapset_count'))


class User(UserCompact):
    """
    Represents a User. Extends UserCompact object with additional attributes.

    **Attributes**

    cover_url: :class:`str`
        url of profile cover. Deprecated, use cover['url'] instead.

    discord: :class:`str` or :class:`NoneType`

    has_supported: :class:`bool`
        whether or not ever being a supporter in the past

    interests: :class:`str` or :class:`NoneType`

    join_date: :class:`datetime.datetime`

    kudosu: :class:`dict`
        Contains items available: :class:`int` and total: :class:`int`

    location: :class:`str` or :class:`NoneType`

    max_blocks: :class:`int`
        maximum number of users allowed to be blocked

    max_friends: :class:`int`
        maximum number of friends allowed to be added

    occupation: :class:`str` or :class:`NoneType`

    playmode: :ref:`GameMode`

    playstyle: Sequence[:class:`str`]
        Device choices of the user.

    post_count: :class:`int`
        number of forum posts

    profile_order: Sequence[:class:`str`]
        Ordered list of sections in user profile page. Sections consist of:
        me, recent_activity, beatmaps, historical, kudosu, top_ranks, medals

    title: :class:`str` or :class:`NoneType`
        user-specific title

    title_url: :class:`str` or :class:`NoneType`

    twitter: :class:`str` or :class:`NoneType`

    website: :class:`str` or :class:`NoneType`

    country: :class:`dict`
        Contains items code: :class:`str` and name: :class:`str`

    cover: :class:`dict`
        Contains items custom_url: :class:`str`, url: :class:`str`, and id: :class:`int`.

    is_restricted: :class:`bool`
        present only if this is the currently authenticated user

    **Possible Attributes**

    All possible attributes come from :class:`UserCompact`
    """
    __slots__ = (
        'cover_url', 'discord', 'has_supported', 'interests', 'join_date', 'kudosu', 'location', 'max_blocks',
        'max_friends', 'occupation', 'playmode', 'playstyle', 'post_count', 'profile_order', 'title', 'title_url',
        'twitter', 'website'
    )

    def __init__(self, data):
        super().__init__(data)
        self.cover_url = data['cover']
        self.discord = data['discord']
        self.has_supported = data['has_supported']
        self.interests = data['interests']
        self.join_date = parser.parse(data['join_date'])
        self.kudosu = data['kudosu']
        self.location = data['location']
        self.max_blocks = data['max_blocks']
        self.max_friends = data['max_friends']
        self.occupation = data['occupation']
        self.playmode = data['playmode']
        self.playstyle = data['playstyle']
        self.post_count = data['post_count']
        self.profile_order = data['profile_order']
        self.title = data['title']
        self.title_url = data['title_url']
        self.twitter = data['twitter']
        self.website = data['website']


class ProfileBanner:
    """
    **Attributes**

    id: :class:`int`

    tournament_id: :class:`int`

    image: :class:`str`
    """
    __slots__ = (
        "id", "tournament_id", "image"
    )

    def __init__(self, data):
        self.id = data['id']
        self.tournament_id = data['tournament_id']
        self.image = data['image']


class UserSilence:
    """
    **Attributes**

    id: :class:`int`
        id of this object.

    user_id: :class:`int`
        id of the User that was silenced
    """
    __slots__ = (
        "id", "user_id"
    )

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']


class UserAccountHistory:
    """
    **Attributes**

    id: :class:`int`

    type: :class:`str`
        Can be one of the following: note, restriction, or silence.

    timestamp: :class:`datetime.datetime`

    length: :class:`int`
        In seconds.
    """
    __slots__ = (
        "id", "type", "timestamp", "length"
    )

    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.timestamp = parser.parse(data['timestamp'])
        self.length = data['length']


class UserBadge:
    """
    **Attributes**

    awarded_at: :class:`datetime.datetime`

    description: :class:`str`

    image_url: :class:`str`

    url: :class:`str`
    """
    __slots__ = (
        "awarded_at", "description", "image_url", "url"
    )

    def __init__(self, data):
        self.awarded_at = parser.parse(data['awarded_at'])
        self.description = data['description']
        self.image_url = data['image_url']
        self.url = data['url']


class UserMonthlyPlaycount:
    """
    **Attributes**

    start_date: :class:`str`
        year-month-day format

    count: class:`int`
        playcount
    """
    __slots__ = (
        "start_date", "count"
    )

    def __init__(self, data):
        self.start_date = data['start_date']
        self.count = data['count']


class UserStatistics:
    """
    A summary of various gameplay statistics for a User. Specific to a :ref:`GameMode`

    **Attributes**

    grade_counts: :class:`dict`
        Below are the keys, their type, and meaning.

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

    hit_accuracy: :class:`int`
        Hit accuracy percentage

    is_ranked: :class:`bool`
        Is actively ranked

    level: :class:`dict`
        Contains keys 'current' (current level) and 'progress' (progress to next level).

    maximum_combo: :class:`int`
        Highest maximum combo.

    play_count: :class:`int`
        Number of maps played.

    play_time: :class:`int`
        Cumulative time played.

    pp: :class:`int`
        Performance points

    recommended_difficulty: :class:`float`
        Recommended difficulty for a player. This value is not received from the api, but locally calculated.

    global_rank: :class:`int` or :class:`NoneType`
        Current rank according to pp.

    country_rank: :class:`int` or :class:`NoneType`
        Current country rank according to pp.

    ranked_score: :class:`int`
        Current ranked score.

    replays_watched_by_others: :class:`int`
        Number of replays watched by other users.

    total_hits: :class:`int`
        Total number of hits.

    total_score: :class:`int`
        Total score.

    user: :class:`UserCompact`
        The associated user.
    """
    __slots__ = (
        "grade_counts", "level", "hit_accuracy", "is_ranked", "maximum_combo",
        "play_count", "play_time", "pp", "global_rank", "ranked_score",
        "replays_watched_by_others", "total_hits", "total_score", "user",
        "country_rank"
    )

    def __init__(self, data):
        self.grade_counts = data['grade_counts']
        self.level = data['level']
        self.hit_accuracy = data['hit_accuracy']
        self.is_ranked = data['is_ranked']
        self.maximum_combo = data['maximum_combo']
        self.play_count = data['play_count']
        self.play_time = data['play_time']
        self.pp = data['pp']
        self.global_rank = data['global_rank']
        self.country_rank = data.get('country_rank')
        self.ranked_score = data['ranked_score']
        self.replays_watched_by_others = data['replays_watched_by_others']
        self.total_hits = data['total_hits']
        self.total_score = data['total_score']
        self.user = UserCompact(data['user']) if data.get("user") is not None else None

    @property
    def recommended_difficulty(self):
        return math.pow(self.pp, 0.4) * 0.195


class UserStatisticsRulesets:
    """
    Object that contains statistics for each gamemode.

    **Attributes**

    osu: :class:`UserStatistics`
        statistics for osu!standard.

    taiko: :class:`UserStatistics`
        statistics for osu!taiko.

    fruits: :class:`UserStatistics`
        statistics for osu!catch.

    mania: :class:`UserStatistics`
        statistics for osu!mania.
    """
    __slots__ = ('osu', 'taiko', 'fruits', 'mania')

    def __init__(self, data):
        self.osu = UserStatistics(data['osu']) if data.get('osu') else None
        self.taiko = UserStatistics(data['taiko']) if data.get('taiko') else None
        self.fruits = UserStatistics(data['fruits']) if data.get('fruits') else None
        self.mania = UserStatistics(data['mania']) if data.get('mania') else None


class CurrentUserAttributes:
    # TODO: Name for BeatmapsetDiscussionPermissions will be changing eventually
    """
    An object listing various related permissions and states for the current user,
    related to the object it is attached to.

    **BeatmapDiscussionPermissions Attributes**

    can_destroy: :class:`bool`
        Can delete the discussion.

    can_reopen: :class:`bool`
        Can reopen the discussion.

    can_moderate_kudosu: :class:`bool`
        Can allow or deny kudosu.

    can_resolve: :class:`bool`
        Can resolve the discussion.

    vote_score: :class:`bool`
        Current vote given to the discussion.

    **ChatChannelUserAttributes Attributes**

    can_message: :class:`bool`
        Can send messages to this channel.

    can_message_error: :class:`str`
        Reason messages cannot be sent to this channel

    last_read_id: :class:`int`
        message_id of last message read.
    """
    def __init__(self, data, attr_type):
        self.type = attr_type
        if attr_type == "BeatmapsetDiscussionPermissions":
            self.can_destroy = data['can_destroy']
            self.can_reopen = data['can_reopen']
            self.can_moderate_kudosu = data['can_moderate_kudosu']
            self.can_resolve = data['can_resolve']
            self.vote_score = data['vote_score']
        elif attr_type == "ChatChannelUserAttributes":
            self.can_message = data['can_message']
            self.can_message_error = data['can_message_erorr']
            self.last_read_id = data['last_read_id']
        else:
            print(f"WARNING: Unrecognized attr_type for CurrentUserAttributes: \"{attr_type}\"")
            for k, v in data.items():
                setattr(self, k, v)
