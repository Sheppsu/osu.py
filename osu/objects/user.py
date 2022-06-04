from .group import UserGroup
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

    last_visit: :ref:`Timestamp`
        null if the user hides online presence

    pm_friends_only: :class:`bool`
        whether or not the user allows PM from other than friends

    profile_colour: :class:`str`
        colour of username/profile highlight, hex code (e.g. #333333)

    username: :class:`str`
        user's display name

    **Possible Attributes**

    account_history: :class:`list`
        list containing objects of type :class:`UserAccountHistory`

    active_tournament_banner: :class:`ProfileBanner`

    badges: :class:`list`
        list containing objects of type :class:`UserBadge`

    beatmap_playcounts_count: :class:`int`

    blocks

    country

    cover

    favourite_beatmapset_count: :class:`int`

    follower_count: :class:`int`

    friends

    graveyard_beatmapset_count: :class:`int`

    groups: :class:`list`
        list containing objects of type :class:`UserGroup`

    is_restricted: :class:`bool`

    loved_beatmapset_count: :class:`int`

    monthly_playcounts: :class:`list`
        list containing objects of type :class:`UserMonthlyPlaycount`

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
        self.last_visit = data['last_visit']
        self.pm_friends_only = data['pm_friends_only']
        self.profile_colour = data['profile_colour']
        self.username = data['username']

        # Optional attributes
        if 'active_tournament_banner' in data:
            self.active_tournament_banner = ProfileBanner(data['active_tournament_banner']) if data['active_tournament_banner'] is not None else None
        else:
            self.active_tournament_banner = None
        self.account_history = [UserAccountHistory(acc_his) for acc_his in data['account_history']] if 'account_history' in data else None
        self.badges = list(map(UserBadge, data['badges'])) if 'badges' in data else None
        self.groups = list(map(UserGroup, data['groups'])) if 'groups' in data else None
        self.monthly_playcounts = list(map(UserMonthlyPlaycount, data['monthly_playcounts'])) if 'monthly_playcounts' in data else None
        self.statistics = UserStatistics(data['statistics']) if 'statistics' in data else None
        for attr in ('page', 'pending_beatmapset_count', 'previous_usernames', 'rank_history', 'ranked_beatmapset_counts',
                     'replays_watched_counts', 'scores_best_count', 'scores_first_count', 'scores_recent_count',
                     'statistics_rulesets', 'support_level', 'unread_pm_count', 'user_achievement', 'user_preferences',
                     'beatmap_playcounts_count', 'blocks', 'country', 'cover', 'favourite_beatmapset_count', 'follower_count',
                     'friends', 'graveyard_beatmapset_count', 'is_restricted', 'loved_beatmapset_count'):
            setattr(self, attr, data.get(attr, None))


class User(UserCompact):
    """
    Represents a User. Extends UserCompact object with additional attributes.

    **Attributes**

    discord: :class:`str`

    has_supported: :class:`bool`
        whether or not ever being a supporter in the past

    interests: :class:`str`

    join_date: :ref:`Timestamp`

    kudosu: :class:`dict`
        a map containing keys total and available

    location: :class:`str`

    max_blocks: :class:`int`
        maximum number of users allowed to be blocked

    max_friends: :class:`int`
        maximum number of friends allowed to be added

    occupation: :class:`str`

    playmode: :ref:`GameMode`

    playstyle: :class:`list`
        list containing objects of type :class:`str`. Device choices of the user.

    post_count: :class:`int`
        number of forum posts

    profile_order: :class:`list`
        list containing objects of type :class:`ProfilePage`. ordered list of sections in user profile page

    title: :class:`str`
        user-specific title

    title_url: :class:`str`

    twitter: :class:`str`

    website: :class:`str`

    country: :class:`dict`
        Contains keys 'code' and 'name', each representing the country.

    cover_url: :class:`str`
        url of profile cover. Deprecated, use cover['url'] instead.

    cover: :class:`dict`
        map containing keys custom_url, url, and id.

    country: :class:`dict`
        map containing keys code and name.

    is_restricted: :class:`bool`
        present only if this is the currently authenticated user

    **Possible Attributes**

    All possible attributes come from :class:`UserCompact`
    """
    __slots__ = (
        "has_supported", "join_date", "kudosu", "location", "max_blocks", "max_friends", "playmode",
        "playstyle", "post_count", "profile_order", "discord", "interests", "location", "occupation", "title",
        "title_url", "twitter", "website"
    )

    def __init__(self, data):
        super().__init__(data)
        self.has_supported = data['has_supported']
        self.join_date = data['join_date']
        self.kudosu = data['kudosu']
        self.location = data['location']
        self.max_blocks = data['max_blocks']
        self.max_friends = data['max_friends']
        self.playmode = data['playmode']
        self.playstyle = data['playstyle']
        self.post_count = data['post_count']
        self.profile_order = data['profile_order']
        self.discord = data['discord']
        self.interests = data['interests']
        self.location = data['location']
        self.occupation = data['occupation']
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

    timestamp: :ref:`Timestamp`

    length: :class:`int`
        In seconds.
    """
    __slots__ = (
        "id", "type", "timestamp", "length"
    )

    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.timestamp = data['timestamp']
        self.length = data['length']


class UserBadge:
    """
    **Attributes**

    awarded_at: :ref:`Timestamp`

    description: :class:`str`

    image_url: :class:`str`

    url: :class:`str`
    """
    __slots__ = (
        "awarded_at", "description", "image_url", "url"
    )

    def __init__(self, data):
        self.awarded_at = data['awarded_at']
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

    global_rank: :class:`int`
        Current rank according to pp.

    country_rank: :class:`int`
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
        "replays_watched_by_others", "total_hits", "total_score", "user"
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
        self.ranked_score = data['ranked_score']
        self.replays_watched_by_others = data['replays_watched_by_others']
        self.total_hits = data['total_hits']
        self.total_score = data['total_score']

        self.user = UserCompact(data['user']) if 'user' in data else None

    @property
    def recommended_difficulty(self):
        return math.pow(self.pp, 0.4) * 0.195


class CurrentUserAttributes:
    # TODO: Name for BeatmapsetDiscussionPermissions will be changing eventually
    """
    Represents user permissions related to an object, which decides what type it is.
    Valid types consist of BeatmapsetDiscussionPermissions

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
            print(f"WARNING: Unrecognized attr_type for CurrentUserAttributes \"{attr_type}\"")
            for k, v in data.items():
                setattr(self, k, v)
