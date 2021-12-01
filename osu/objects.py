from .constants import int_to_status


class DataUnpacker:
    """
    I am limiting the use of this class so that IDE's can use autofill features when typing.
    When using DataUnpacker, the IDE has no idea what the attributes of the class are.
    """
    def __init__(self, data, exceptions=None, ignore=None):
        if ignore is None:
            ignore = []
        if exceptions is None:
            exceptions = []
        for key, value in data.items():
            if key in ignore:
                continue
            if key in exceptions and value is not None:
                if exceptions[key][1]:
                    setattr(self, key, [exceptions[key][0](obj_data) for obj_data in data[key]])
                else:
                    setattr(self, key, exceptions[key][0](data[key]))
                continue
            setattr(self, key, value)


class Scope:
    """
    Scope object for telling the program what scopes you are using

    **Valid scopes**

    public
        Allows reading of publicly available data on behalf of the user.
    identify (default)
        Allows reading of the public profile of the user (/me).
    friends.read
        Allows reading of the user's friend list.
    forum.write
        Allows creating and editing forum posts on a user's behalf.
    delegate
        Allows acting as the owner of a client; only available for Client Credentials Grant.
    chat.write
        Allows sending chat messages on a user's behalf.
    """
    valid_scopes = [
        'chat.write',
        'delegate',
        'forum.write',
        'friends.read',
        'identify',
        'public',
    ]

    def __init__(self, *scopes):
        for scope in scopes:
            if scope not in self.valid_scopes:
                raise NameError(f"{scope} is not a valid scope. The valid scopes consist of {','.join(self.valid_scopes)}")
        self.scopes = ' '.join(scopes)
        self.scopes_list = list(scopes)

    @classmethod
    def default(cls):
        return cls('public')

    def __str__(self):
        return ", ".join(self.scopes)

    def __contains__(self, item):
        return item in self.scopes_list


class BeatmapCompact:
    """
    Represents a beatmap.

    **Attributes**

    difficulty_rating: :class:`float`

    id: :class:`int`

    mode: :class:`GameMode`

    status: :class:`str`
        Possible values consist of graveyard, wip, pending, ranked, approved, qualified, loved

    total_length: :class:`int`

    version: :class:`str`

    **Possible Attributes**

    beatmapset: :class:`Beatmapset` | :class:`BeatmapsetCompact` | :class:`NoneType`
        Beatmapset for Beatmap object, BeatmapsetCompact for BeatmapCompact object. null if the beatmap doesn't have associated beatmapset (e.g. deleted).

    checksum: :class:`str`

    failtimes: :class:`Failtimes`

    max_combo: :class:`int`
    """
    def __init__(self, data):
        self.difficulty_rating = data['difficulty_rating']
        self.id = data['id']
        self.mode = data['mode']
        self.status = data['status']
        self.total_length = data['total_length']
        self.version = data['version']

        if 'checksum' in data:
            self.checksum = data['checksum']
        if 'max_combo' in data:
            self.max_combo = data['max_combo']
        if 'failtimes' in data:
            self.failtimes = Failtimes(data['failtimes'])

        if 'beatmapset' in data and data['beatmapset'] is not None:
            if type(self).__name__ == 'Beatmap':
                self.beatmapset = Beatmapset(data['beatmapset'])
            else:
                self.beatmapset = BeatmapsetCompact(data['beatmapset'])
        elif 'beatmapset' in data and data['beatmapset'] is None:
            self.beatmapset = None


class Failtimes:
    """
    All attributes are optional but there's always at least one attribute returned.

    **Attributes**

    exit: :class:`list`
        Contains objects of type :class:`int`. List of length 100.

    fail: :class:`list`
        Contains objects of type :class:`int`. List of length 100.
    """
    def __init__(self, data):
        if 'exit' in data:
            self.exit = data['exit']
        if 'fail' in data:
            self.fail = data['fail']

    @property
    def type(self):
        if getattr(self, 'exit', None) is None:
            return 'fail'
        if getattr(self, 'fail', None) is None:
            return 'exit'
        return 'both'


class Beatmap(BeatmapCompact):
    """
    Represent a beatmap. This extends :class:`BeatmapCompact` with additional attributes.

    **Attributes**

    accuracy: :class:`float`

    ar: :class:`float`

    beatmapset_id: :class:`int`

    bpm: :class:`float`

    convert: :class:`bool`

    count_circles: :class:`int`

    count_sliders: :class:`int`

    count_spinners: :class:`int`

    cs: :class:`float`

    deleted_at: :class:`Timestamp`
        :class:`Timestamp`

    drain: :class:`float`

    hit_length: :class:`int`

    is_scoreable: :class:`bool`

    last_updated: :class:`Timestamp`
        :class:`Timestamp`

    mode_int: :class:`int`

    passcount: :class:`int`

    playcount: :class:`int`

    ranked: :class:`str`
        Possible values consist of graveyard, wip, pending, ranked, approved, qualified, loved

    url: :class:`str`
    """
    def __init__(self, data):
        super().__init__(data)
        self.ranked = int_to_status[int(data['ranked'])]
        self.url = data['url']
        self.playcount = data['playcount']
        self.passcount = data['passcount']
        self.mode_int = data['mode_int']
        self.last_updated = data['last_updated']
        self.is_scoreable = data['is_scoreable']
        self.hit_length = data['hit_length']
        self.drain = data['drain']
        self.deleted_at = data['deleted_at']
        self.cs = data['cs']
        self.count_spinners = data['count_spinners']
        self.count_sliders = data['count_sliders']
        self.count_circles = data['count_circles']
        self.convert = data['convert']
        self.bpm = data['bpm']
        self.beatmapset_id = data['beatmapset_id']
        self.ar = data['ar']
        self.accuracy = data['accuracy']


class BeatmapPlaycount:
    """
    Represent the playcount of a beatmap.

    **Attributes**

    beatmap_id: :class:`int`

    beatmap: :class:`BeatmapCompact`

    beatmapset: :class:`BeatmapsetCompact`

    count: :class:`int`
    """
    def __init__(self, data):
        self.beatmap_id = data['beatmap_id']
        self.beatmap = BeatmapCompact(data['beatmap'])
        self.beatmapset = BeatmapsetCompact(data['beatmapset'])
        self.count = data['count']


class BeatmapScores:
    """
    Contains a list of scores as well as, possibly, a BeatmapUserScore object.

    **Attributes**

    scores: :class:`list`
        Contains objects of type :class:`Score`. The list of top scores for the beatmap in descending order.

    **Possible Attributes**

    user_score: :class:`BeatmapUserScore`
        The score of the current user. This is not returned if the current user does not have a score.
    """
    def __init__(self, data):
        self.scores = [Score(score) for score in data['scores']]
        if 'userScore' in data:
            self.user_score = BeatmapUserScore(data['userScore'])
        elif 'user_score' in data:  # Is being renamed to this in the future
            self.user_score = BeatmapUserScore(data['user_score'])


class Score:
    """
    Contains information about a score

    **Attributes**

    id: :class:`int`

    best_id: :class:`int`

    user_id: :class:`int`

    accuracy: :class:`float`

    mods: :class:`list`

    score: :class:`int`

    max_combo: :class:`int`

    perfect: :class:`bool`

    statistics: :class:`ScoreStatistics`

    pp: :class:`float`

    rank: :class:`int`

    created_at: :class:`Timestamp`

    mode: :class:`str`

    mode_int: :class:`int`

    replay

    **Optional Attributes**

    beatmap: :class:`BeatmapCompact`

    beatmapset: :class:`BeatmapsetCompact`

    rank_country

    rank_global

    weight

    user

    match
    """
    def __init__(self, data):
        self.id = data['id']
        self.best_id = data['best_id']
        self.user_id = data['user_id']
        self.accuracy = data['accuracy']
        self.mods = data['mods']
        self.score = data['score']
        self.max_combo = data['max_combo']
        self.perfect = data['perfect']
        self.statistics = ScoreStatistics(data['statistics'])
        self.pp = data['pp']
        self.rank = data['rank']
        self.created_at = data['created_at']
        self.mode = data['mode']
        self.mode_int = data['mode_int']
        self.replay = data['replay']

        if 'beatmap' in data:
            self.beatmap = BeatmapCompact(data['beatmap'])
        if 'beatmapset' in data:
            self.beatmapset = BeatmapsetCompact(data['beatmapset'])
        if 'rank_country' in data:
            self.rank_country = data['rank_country']
        if 'rank_global' in data:
            self.rank_global = data['rank_global']
        if 'weight' in data:
            self.weight = data['weight']
        if 'user' in data:
            self.user = UserCompact(data['user'])  # Doesn't say exactly what type it should be under so I assume UserCompact
        if 'match' in data:
            self.match = data['match']


class ScoreStatistics:
    """
    **Attributes**

    count_50: :class:`int`

    count_100: :class:`int`

    count_300: :class:`int`

    count_genki: :class:`int`

    count_katu: :class:`int`

    count_miss: :class:`int`
    """
    def __init__(self, data):
        self.count_50 = data['count_50']
        self.count_100 = data['count_100']
        self.count_300 = data['count_300']
        if 'count_genki' in data:
            self.count_genki = data['count_genki']
        self.count_katu = data['count_katu']
        self.count_miss = data['count_miss']


class BeatmapUserScore:
    """
    **Attributes**

    position: :class:`int`
        The position of the score within the requested beatmap ranking.
    score: :class:`Score`
        The details of the score.
    """
    def __init__(self, data):
        self.position = data['position']
        self.score = Score(data['score'])


class BeatmapsetCompact:
    """
    Represents a beatmapset.

    **Attributes**

    artist: :class:`str`

    artist_unicode: :class:`str`

    covers: :class:`Covers`

    creator: :class:`str`

    favourite_count: :class:`int`

    id: :class:`int`

    nsfw: :class:`bool`

    play_count: :class:`int`

    preview_url: :class:`str`

    source: :class:`str`

    status: :class:`str`

    title: :class:`str`

    title_unicode: :class:`str`

    user_id: :class:`int`

    video: :class:`str`

    **Possible Attributes**

    beatmaps: :class:`list`
        list containing objects of type :class:`Beatmap`

    converts

    current_user_attributes

    description

    discussions

    events

    genre

    has_favourited: :class:`bool`

    language

    nominations: :class:`dict`
        Contains keys current and required.

    ratings

    recent_favourites

    related_users

    user
    """
    def __init__(self, data):
        self.artist = data['artist']
        self.artist_unicode = data['artist_unicode']
        self.covers = Covers(data['covers'])
        self.creator = data['creator']
        self.favourite_count = data['favourite_count']
        self.id = data['id']
        self.nsfw = data['nsfw']
        self.play_count = data['play_count']
        self.preview_url = data['preview_url']
        self.source = data['source']
        self.status = data['status']
        self.title = data['title']
        self.title_unicode = data['title_unicode']
        self.user_id = data['user_id']
        self.video = data['video']

        # Documentation lacks information on all the possible attributes :/
        if 'beatmaps' in data:
            self.beatmaps = [Beatmap(beatmap) for beatmap in data['beatmaps']]
        if 'current_user_attributes' in data:
            self.current_user_attributes = CurrentUserAttributes(['current_user_attributes'], 'BeatmapsetDiscussionPermissions')
        if 'user' in data:
            self.user = UserCompact(data['user'])
        for attr in ("converts", "description", "discussions", "events", "genre", "has_favourited", "language", "nominations", 'ratings', 'recent_favourites', 'related_users'):
            if attr in data:
                setattr(self, attr, data[attr])


class Covers:
    """
    **Attributes**

    cover: :class:`str`

    cover_2x: :class:`str`

    card: :class:`str`

    card_2x: :class:`str`

    list: :class:`str`

    list_2x: :class:`str`

    slimcover: :class:`str`

    slimcover_2x: :class:`str`
    """
    def __init__(self, data):
        self.cover = data['cover']
        self.cover_2x = data['cover@2x']
        self.card = data['card']
        self.card_2x = data['card@2x']
        self.list = data['list']
        self.list_2x = data['list@2x']
        self.slimcover = data['slimcover']
        self.slimcover_2x = data['slimcover@2x']


class Beatmapset(BeatmapsetCompact):
    """
    Represents a beatmapset. This extends :class:`BeatmapsetCompact` with additional attributes.

    **Attributes**

    availability: :class:`dict`
        Contains two items, download_disabled: :class:`bool` and more_information: :class:`str`

    bpm: :class:`float`

    can_be_hyped: :class:`bool`

    creator: :class:`str`
        Username of the mapper at the time of beatmapset creation.

    discussion_enabled: :class:`bool`

    discussion_locked: :class:`bool`

    hype: :class:`dict`
        Contains two items, current: :class:`int` and required: :class:`int`

    is_scoreable: :class:`bool`

    last_updated: :class:`Timestamp`

    legacy_thread_url: :class:`str`

    ranked: :class:`str`
        Possible values consist of graveyard, wip, pending, ranked, approved, qualified, loved

    ranked_date: :class:`Timestamp`

    source: :class:`str`

    storyboard: :class:`bool`

    submitted_date: :class:`Timestamp`

    tags: :class:`str`
    """

    # nominations: :class:`dict`
    #         Contains two items, current: :class:`int` and required: :class:`int`
    def __init__(self, data):
        super().__init__(data)
        self.availability = data['availability']
        self.bpm = data['bpm']
        self.can_be_hyped = data['can_be_hyped']
        self.creator = data['creator']
        self.discussion_enabled = data['discussion_enabled']
        self.discussion_locked = data['discussion_locked']
        self.hype = data['hype']
        self.is_scoreable = data['is_scoreable']
        self.last_updated = data['last_updated']
        self.legacy_thread_url = data['legacy_thread_url']
        # self.nominations = data['nominations']  # docs says this should be there but it's not ?
        self.ranked = data['ranked']
        self.ranked_date = data['ranked_date']
        self.source = data['source']
        self.storyboard = data['storyboard']
        self.tags = data['tags']
        # self.has_favourited = data['has_favourited']  # should be included but it's not ?
        self.ranked = int_to_status[int(data['ranked'])]


class BeatmapsetDiscussion:
    """
    Represents a Beatmapset modding discussion

    **Attributes**

    beatmap: :class:`BeatmapCompact`

    beatmap_id: :class:`int`

    beatmapset: :class:`BeatmapsetCompact`

    beatmapset_id: :class:`int`

    can_be_resolved: :class:`bool`

    can_grant_kudosu: :class:`bool`

    created_at: :class:`Timestamp`

    current_user_attributes: :class:`CurrentUserAttributes`

    deleted_at: :class:`Timestamp`

    deleted_by_id: :class:`int`

    id: :class:`int`

    kudosu_denied: :class:`bool`

    last_post_at: :class:`Timestamp`

    message_type: :class:`MessageType`
        :class:`MessageType` can be one of the following, all of which being :class:`str`, hype, mapper_note, praise, review, suggestion

    parent_id: :class:`int`

    posts: :class:`list`
        list contains objects of type :class:`BeatmapsetDiscussionPost`

    resolved: :class:`bool`

    starting_post: :class:`BeatmapsetDiscussionPost`

    timestamp: :class:`int`

    updated_at: :class:`Timestamp`

    user_id: :class:`int`

    votes: :class:`list`
        list containing objects of type :class:`BeatmapsetDiscussionVote`
    """
    def __init__(self, data):
        self.beatmap = BeatmapCompact(data['beatmap'])
        self.beatmap_id = data['beatmap_id']
        self.beatmapset = BeatmapsetCompact(data['beatmapset'])
        self.beatmapset_id = data['beatmapset_id']
        self.can_be_resolved = data['can_be_resolved']
        self.can_grant_kudosu = data['can_grant_kudosu']
        self.created_at = data['created_at']
        self.current_user_attributes = CurrentUserAttributes(data['current_user_attributes'], 'BeatmapsetDiscussionPermissions')
        self.deleted_at = data['deleted_at']
        self.deleted_by_id = data['deleted_by_id']
        self.id = data['id']
        self.kudosu_denied = data['kudosu_denied']
        self.last_post_at = data['last_post_at']
        self.message_type = MessageType(data['message_type'])
        self.parent_id = data['parent_id']
        self.posts = [BeatmapsetDiscussionPost(post) for post in data['posts']]
        self.resolved = data['resolved']
        self.starting_post = BeatmapsetDiscussionPost(data['starting_post'])
        self.timestamp = data['timestamp']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.votes = [BeatmapsetDiscussionVote(vote) for vote in data['votes']]


class MessageType:
    """
    **Attributes**

    hype

    mapper_note

    praise

    problem

    review

    suggestion
    """

    def __init__(self, data):
        self.hype = data['hype']
        self.mapper_note = data['mapper_note']
        self.praise = data['praise']
        self.problem = data['problem']
        self.review = data['review']
        self.suggestion = data['suggestion']


class CurrentUserAttributes:
    # Note: Name for BeatmapsetDiscussionPermissions will be changing eventually
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
            self.last_read_id = data['last_read_id']
        else:
            print(f"WARNING: Unrecognized attr_type \"{attr_type}\"")
            for k, v in data.items():
                setattr(self, k, v)


class BeatmapsetDiscussionPost:
    """
    Represents a post in a :class:`BeatmapsetDiscussion`.

    **Attributes**

    beatmapset_discussion_id: :class:`int`

    created_at: :class:`Timestamp`

    deleted_at: :class:`Timestamp`

    deleted_by_id: :class:`int`

    id: :class:`int`

    last_editor_id: :class:`int`

    message: :class:`str`

    system: :class:`bool`

    updated_at: :class:`Timestamp`

    user_id: :class:`int`
    """
    def __init__(self, data):
        self.beatmapset_discussion_id = data['beatmapset_discussion_id']
        self.created_at = data['created_at']
        self.deleted_at = data['deleted_at']
        self.deleted_by_id = data['deleted_by_id']
        self.id = data['id']
        self.last_editor_id = data['last_editor_id']
        self.message = data['message']
        self.system = data['system']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


class BeatmapsetDiscussionVote:
    """
    Represents a vote on a :class:`BeatmapsetDiscussion`.

    **Attributes**

    beatmapset_discussion_id: :class:`int`

    created_at: :class:`Timestamp`

    id: :class:`int`

    score: :class:`int`

    updated_at: :class:`Timestamp`

    user_id: :class:`int`
    """
    def __init__(self, data):
        self.beatmapset_discussion_id = data['beatmapset_discussion_id']
        self.created_at = data['created_at']
        self.id = data['id']
        self.score = data['score']
        self.updated_at = data['updated_at']
        self.user_id = data['user']


class ChatChannel:
    """
    Represents an individual chat "channel" in the game.

    **Attributes**

    channel_id: :class:`int`

    current_user_attributes: :class:`CurrentUserAttributes`
        only present on some responses

    name: :class:`str`

    description: :class:`str`

    icon: :class:`str`
        display icon for the channel

    type: :class:`str`
        Below are the channel types and their permission checks for joining/messaging:
        PUBLIC
            None
        PRIVATE
            is player in the allowed groups? (channel.allowed_groups)
        MULTIPLAYER
            is player currently in the mp game?
        SPECTATOR
            None
        TEMPORARY
            deprecated
        PM
            Is either user blocking the other? If so, deny.
            Does the target only accept PMs from friends? Is the current user a friend? If not, deny.
        GROUP
            is player in channel? (user_channels)

    first_message_id: :class:`int`
        message_id of first message (only returned in presence responses)

    last_message_id: :class:`int`
        message_id of last known message (only returned in presence responses)

    recent_messages: class:`list`
        list containing objects of type :class:`ChatMessage`. Up to 50 most recent messages.

    moderated: :class:`bool`
        user can't send message when the value is true (only returned in presence responses)

    users: :class:`list`
        list of user_id that are in the channel (not included for PUBLIC channels)
    """
    def __init__(self, data):
        self.channel_id = data['channel_id']
        self.current_user_attributes = CurrentUserAttributes(data['current_user_attributes'], "ChatChannelUserAttributes")
        self.name = data['name']
        self.description = data['description']
        self.icon = data['icon']
        self.type = data['type']
        self.first_message_id = data['first_message_id']
        self.last_message_id = data['last_message_id']
        self.recent_messages = [ChatMessage(message) for message in data['recent_messages']]
        self.moderated = data['moderated']
        self.users = data['users']


class ChatMessage:
    """
    Represents an individual Message within a :class:`ChatChannel`.

    **Attributes**

    message_id: :class:`int`
        unique identifier for message

    sender_id: :class:`int`
        user_id of the sender

    channel_id: :class:`int`
        channel_id of where the message was sent

    timestamp: :class:`str`
        when the message was sent, ISO-8601

    content: :class:`str`
        message content

    is_action: :class:`bool`
        was this an action? i.e. /me dances

    sender: :class:`UserCompact`
        embeded :class:`UserCompact` object to save additional api lookups
    """
    def __init__(self, data):
        self.message_id = data['message_id']
        self.sender_id = data['sender_id']
        self.channel_id = data['channel_id']
        self.timestamp = data['timestamp']
        self.content = data['content']
        self.is_action = data['is_action']
        self.sender = UserCompact(data['sender'])


class Comment:
    """
    Represents a single comment.

    **Attributes**

    commentable_id: :class:`int`
        ID of the object the comment is attached to

    commentable_type: :class:`str`
        type of object the comment is attached to

    created_at: :class:`Timestamp`
        ISO 8601 date

    deleted_at: :class:`Timestamp`
        ISO 8601 date if the comment was deleted; null, otherwise

    edited_at: :class:`Timestamp`
        ISO 8601 date if the comment was edited; null, otherwise

    edited_by_id: :class:`int`
        user id of the user that edited the post; null, otherwise

    id: :class:`int`
        the ID of the comment

    legacy_name: :class:`str`
        username displayed on legacy comments

    message: :class:`str`
        markdown of the comment's content

    message_html: :class:`str`
        html version of the comment's content

    parent_id: :class:`int`
        ID of the comment's parent

    pinned: :class:`bool`
        Pin status of the comment

    replies_count: :class:`int`
        number of replies to the comment

    updated_at: :class:`Timestamp`
        ISO 8601 date

    user_id: :class:`int`
        user ID of the poster

    votes_count: :class:`int`
        number of votes
    """
    def __init__(self, data):
        self.commentable_id = data['commentable_id']
        self.commentable_type = data['commentable_type']
        self.created_at = data['created_at']
        self.deleted_at = data['deleted_at']
        self.edited_at = data['edited_at']
        self.edited_by_id = data['edited_by_id']
        self.id = data['id']
        self.legacy_name = data['legacy_name']
        self.message = data['message']
        self.message_html = data['message_html']
        self.parent_id = data['parent_id']
        self.pinned = data['pinned']
        self.replies_count = data['replies_count']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.votes_count = data['votes_count']


class CommentBundle:
    """
    Comments and related data.

    **Attributes**

    commentable_meta: :class:`list`
        list containing objects of type :class:`CommentableMeta`. ID of the object the comment is attached to

    comments: :class:`list`
        list containing objects of type :class:`Comment`. List of comments ordered according to sort

    cursor:	:class:`dict`
        To be used to query the next page

    has_more: :class:`bool`
        If there are more comments or replies available

    has_more_id: :class:`id`

    included_comments: :class:`list`
        list containing objects of type :class:`Comment`. Related comments; e.g. parent comments and nested replies

    pinned_comments: :class:`list`
        list containing objects of type :class:`Comment`. Pinned comments

    sort: :class:`str`
        one of the following:
            new (created_at (descending), id (descending))
            old (created_at (ascending), id (ascending))
            top (votes_count (descending), created_at (descending), id (descending))

    top_level_count: :class:`int`
        Number of comments at the top level. Not returned for replies.

    total: :class:`int`
        Total number of comments. Not retuned for replies.

    user_follow: :class:`bool`
        is the current user watching the comment thread?

    user_votes: :class:`list`
        list containing objects of type :class:`int`.IDs of the comments in the bundle the current user has upvoted

    users: :class:`list`
        list containing objects of type :class:`UserCompact`. list of users related to the comments
    """
    def __init__(self, data):
        self.commentable_meta = [CommentableMeta(comment) for comment in data['commentable_meta']]
        self.comments = [Comment(comment) for comment in data['comments']]
        self.cursor = data['cursor']
        self.has_more = data['has_more']
        self.has_more_id = data['has_more_id']
        self.included_comments = [Comment(comment) for comment in data['included_comments']]
        self.pinned_comments = [Comment(comment) for comment in data['pinned_comments']]
        self.sort = data['sort']
        self.top_level_count = data['top_level_count']
        self.total = data['total']
        self.user_follow = data['user_follow']
        self.user_votes = data['user_votes']
        self.users = [UserCompact(user) for user in data['users']]


class CommentableMeta:
    """
    Metadata of the object that a comment is attached to.

    **Attributes**

    id: :class:`int`
        the ID of the object

    title: :class:`str`
        display title

    type: :class:`str`
        the type of the object

    url: :class:`str`
        url of the object
    """
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.type = data['type']
        self.url = data['url']


class Event:
    """
    The object has different attributes depending on its type. Following are attributes available to all types.

    **Attributes**

    created_at: :class:`Timestamp`

    id: :class:`int`

    type:
        All types and the additional attributes they provide are listed under 'Event Types'

    **Event Types**

    :class:`achievement`
        achievement: :class:`Achievement`
        user: :class:`EventUser`

    :class:`beatmapPlaycount`
        beatmap: :class:`EventBeatmap`
        count: :class:`int`

    :class:`beatmapsetApprove`
        approval: :class:`str`
        beatmapset: :class:`EventBeatmapset`
        user: :class:`EventUser`

    :class:`beatmapsetDelete`
        beatmapset: :class:`EventBeatmapset`

    :class:`beatmapsetRevive`
        beatmapset: :class:`EventBeatmapset`
        user: :class:`EventUser`

    :class:`beatmapsetUpdate`
        beatmapset: :class:`EventBeatmapset`
        user: :class:`EventUser`

    :class:`beatmapsetUpload`
        beatmapset: :class:`EventBeatmapset`
        user: :class:`EventUser`

    :class:`rank`
        score_rank: :class:`str`
        rank: :class:`int`
        mode: :class:`GameMode`
        beatmap: :class:`EventBeatmap`
        user: :class:`EventUser`

    :class:`rankLost`
        mode: :class:`GameMode`
        beatmap: :class:`EventBeatmap`
        user: :class:`EventUser`

    :class:`userSupportAgain`
        user: :class:`EventUser`

    :class:`userSupportFirst`
        user: :class:`EventUser`

    :class:`userSupportGift`
        user: :class:`EventUser`

    :class:`usernameChange`
        user: :class:`EventUser`
    """
    def __init__(self, data):
        self.created_at = data['created_at']
        self.id = data['id']
        self.type = data['type']

        if self.type == 'achievement':
            self.achievement = data['achievement']
            self.user = EventUser(data['user'])
        elif self.type == 'beatmapPlaycount':
            self.beatmap = EventBeatmap(data['beatmap'])
            self.count = data['count']
        elif self.type == 'beatmapsetApprove':
            self.approval = data['approval']
            self.beatmapset = EventBeatmapset(data['beatmapset'])
            self.user = EventUser(data['user'])
        elif self.type == 'beatmapsetDelete':
            self.beatmapset = EventBeatmapset(data['beatmapset'])
        elif self.type in ("beatmapsetRevive", "beatmapsetUpdate", "beatmapsetUpload"):
            self.beatmapset = EventBeatmapset(data['beatmapset'])
            self.user = EventUser(data['user'])
        elif self.type == 'rank':
            self.score_rank = data['scoreRank']
            self.rank = data['rank']
            self.mode = data['mode']
            self.beatmap = EventBeatmap(data['beatmap'])
            self.user = EventUser(data['user'])
        elif self.type == 'rankLost':
            self.mode = data['mode']
            self.beatmap = EventBeatmap(data['beatmap'])
            self.user = EventUser(data['user'])
        elif self.type in ("userSupportAgain", "userSupportFirst", "userSupportGift", "usernameChange"):
            self.user = EventUser(data['user'])


class EventUser:
    """
    **Attributes**

    username: :class:`str`

    url: :class:`str`

    previous_username: :class:`str`
    """
    def __init__(self, data):
        self.username = data['username']
        self.url = data['url']
        self.previous_username = data['previous_username']


class EventBeatmap:
    """
    **Attributes**

    title: :class:`str`

    url: :class:`str`
    """
    def __init__(self, data):
        self.title = data['title']
        self.url = data['url']


class EventBeatmapset:
    """
    **Attributes**

    title: :class:`str`

    url: :class:`str`
    """
    def __init__(self, data):
        self.title = data['title']
        self.url = data['url']


class ForumPost:
    """
    **Attributes**

    created_at: :class:`Timestamp`

    deleted_at: :class:`Timestamp`

    edited_at: :class:`Timestamp`

    edited_by_id: :class:`int`

    forum_id: :class:`int`

    id: :class:`int`

    topic_id: :class:`int`

    user_id: :class:`int`

    **Possible Attributes**

    body.html: :class:`str`
        Post content in HTML format.

    body.raw: :class:`str`
        content in BBCode format.
    """
    def __init__(self, data):
        self.created_at = data['created_at']
        self.deleted_at = data['deleted_at']
        self.edited_at = data['edited_at']
        self.edited_by_id = data['edited_by_id']
        self.forum_id = data['forum_id']
        self.id = data['id']
        self.topic_id = data['topic_id']
        self.user_id = data['user_id']
        if 'body.html' in data:
            self.body_html = data['body.html']
        if 'body.raw' in data:
            self.body_raw = data['body.raw']


class ForumTopic:
    """
    **Attributes**

    created_at: :class:`Timestamp`

    deleted_at: :class:`Timestamp`

    first_post_id: :class:`int`

    forum_id: :class:`int`

    id: :class:`int`

    is_locked: :class:`bool`

    last_post_id: :class:`int`

    post_count: :class:`int`

    title: :class:`str`

    type: :class:`str`
        normal, sticky, or announcement

    updated_at: :class:`Timestamp`

    user_id: :class:`int`
    """
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


class Group:
    """
    This object isn't returned by any endpoints yet, it is here purely as a reference for :class:`UserGroup`

    **Attributes**

    id: :class:`int`

    identifier: :class:`str`
        Unique string to identify the group.

    is_probationary: :class:`str`
        Whether members of this group are considered probationary.

    has_playmodes: :class:`bool`
        If this group associates GameModes with a user's membership, e.g. BN/NAT members

    name: :class:`str`

    short_name: :class:`str`
        Short name of the group for display.

    colour: :class:`str`

    **Optional Attributes**

    description: :class:`Description`
        A dictionary with keys html and markdown.
    """
    def __init__(self, data):
        self.id = data['id']
        self.identifier = data['identifier']
        self.is_probationary = data['is_probationary']
        self.has_playmodes = data['has_playmodes']
        self.name = data['name']
        self.short_name = data['short_name']
        self.colour = data['colour']
        if 'description' in data:
            self.description = data['description']


class KudosuHistory:
    """
    **Attributes**

    id: :class:`int`

    action: :class:`str`
        Either give, reset, or revoke.

    amount: :class:`int`

    model: :class:`str`
        Object type which the exchange happened on (forum_post, etc).

    created_at: :class:`Timestamp`

    giver: :class:`Giver`
        Simple detail of the user who started the exchange.

    post: :class:`Post`
        Simple detail of the object for display.
    """
    def __init__(self, data):
        self.id = data['id']
        self.action = data['action']
        self.amount = data['amount']
        self.model = data['model']
        self.created_at = data['created_at']
        self.giver = Giver(data['giver'])
        self.post = Post(data['post'])


class Post:
    """
    **Attributes**

    url: :class:`str`
        Url of the object.

    title: :class:`str`
        Title of the object. It'll be "[deleted beatmap]" for deleted beatmaps.
    """
    def __init__(self, data):
        self.url = data['url']
        self.title = data['title']


class Giver:
    """
    **Attributes**

    url: :class:`str`

    username: :class:`str`
    """
    def __init__(self, data):
        self.url = data['url']
        self.username = data['username']


class MultiplayerScore:
    """
    Score data.

    **Attributes**

    id: :class:`int`

    user_id: :class:`int`

    room_id: :class:`int`

    playlist_item_id: :class:`int`

    beatmap_id: :class:`int`

    rank: :class:`str`
        Can be one of the following: charts (Spotlight), country (Country), performance (Performance), score (Score)

    total_score: :class:`int`

    accuracy: :class:`int`

    max_combo: :class:`int`

    mods: :class:`list`
        list containing objects of type :class:`str`

    statistics: :class:`ScoreStatistics`

    passed: :class:`bool`

    position: :class:`int`

    scores_around: :class:`MultiplayerScoresAround`
        Scores around the specified score.

    user: :class:`User`
    """
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.room_id = data['room_id']
        self.playlist_item_id = data['playlist_item_id']
        self.beatmap_id = data['beatmap_id']
        self.rank = data['rank']
        self.total_score = data['total_score']
        self.accuracy = data['accuracy']
        self.max_combo = data['max_combo']
        self.mods = data['mods']
        self.statistics = ScoreStatistics(data['statistics'])
        self.passed = data['passed']
        self.position = data['position']
        self.scores_around = MultiplayerScoresAround(data['scores_around'])


class MultiplayerScores:
    """
    An object which contains scores and related data for fetching next page of the result.
    To fetch the next page, make request to scores index (Client.get_scores) with relevant
    room and playlist, use the data in attribute params and cursor to fill in the 3 other optional queries.

    **Attributes**

    cursor: :class:`dict`
        To be used to fetch the next page.

    params: :class:`dict`
        To be used to fetch the next page.

    scores: :class:`list`
        list containing objects of type :class:`MultiplayerScore`

    total: :class:`int`
        Index only. Total scores of the specified playlist item.

    user_score: :class:`MultiplayerScore`
        Index only. Score of the accessing user if exists.
    """
    def __init__(self, data):
        self.cursor = data['cursor']
        self.params = data['params']
        self.scores = [MultiplayerScore(score) for score in data['scores']]
        if 'total' in data:
            self.total = data['total']
        if 'user_score' in data:
            self.user_score = MultiplayerScore(data['user_score'])


class MultiplayerScoresAround:
    """
    **Attributes**

    higher: :class:`MultiplayerScores`

    lower: :class:`MultiplayerScores`
    """
    def __init__(self, data):
        self.higher = MultiplayerScores(data['higher'])
        self.lower = MultiplayerScores(data['lower'])


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
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.object_type = data['object_type']
        self.object_id = data['object_id']
        self.is_read = data['is_read']
        if 'source_user_id' in data:
            self.source_user_id = data['source_user_id']
        if 'details' in data:
            self.details = Details(data['details'], self.name)


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
        if event_name in ('beatmapset_discussion_lock', 'beatmapset_discussion_unlock', 'beatmapset_disqualify', 'beatmapset_love', 'beatmapset_nominate', 'beatmapset_qualify', 'beatmapset_remove_from_loved', 'beatmapset_reset_nominations', 'channel_message'):
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


class Rankings:
    """
    **Attributes**

    beatmapsets: :class:`list`
        list containing objects of type :class:`Beatmapset`. The list of beatmaps in the requested spotlight for the given mode; only available if type is charts

    cursor: :class:`dict`
        To be used to query the next page

    ranking: :class:`list`
        list containing objects of type :class:`UserStatistics`. Score details ordered by rank in descending order.

    spotlight: :class:`Spotlight`
        Spotlight details; only available if type is charts

    total: :class:`int`
        An approximate count of ranks available
    """
    def __init__(self, data):
        self.cursor = data['cursor']
        self.ranking = [UserStatistics(ranking) for ranking in data['ranking']]
        self.total = data['total']
        if 'spotlight' in data:
            self.spotlight = Spotlight(data['spotlight'])
        if 'beatmapsets' in data:
            self.beatmapsets = [Beatmapset(beatmapset) for beatmapset in data['beatmapsets']]


class Spotlight:
    """
    The details of a spotlight.

    **Attributes**

    end_date: :class:`str`
        In DateTime format. The end date of the spotlight.

    id: :class:`int`
        The ID of this spotlight.

    mode_specific: :class:`bool`
        If the spotlight has different mades specific to each GameMode.

    name: :class:`str`
        The name of the spotlight.

    start_date: :class:`str`
        In DatTime format. The starting date of the spotlight.

    type: :class:`str`
        The type of spotlight.

    **Possible Attributes((

    participant_count: :class:`int`
        The number of users participating in this spotlight. This is only shown when viewing a single spotlight.
    """
    def __init__(self, data):
        self.end_date = data['end_date']
        self.id = data['id']
        self.mode_specific = data['mode_specific']
        self.name = data['name']
        self.start_data = data['start_date']
        self.type = data['type']
        if 'participant_count' in data:
            self.participant_count = data['participant_count']


class Spotlights:
    """
    **Attributes**

    spotlights: :class:`list`
        list containing objects of type :class:`Spotlight`
    """
    def __init__(self, data):
        self.spotlights = [Spotlight(spotlight) for spotlight in data['spotlights']]


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

    last_visit: :class:`Timestamp`
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

        if 'account_history' in data:
            self.account_history = [UserAccountHistory(acc_his) for acc_his in data['account_history']]
        if 'active_tournament_banner' in data:
            if data['active_tournament_banner'] is None:
                self.active_tournament_banner = None
            else:
                self.active_tournament_banner = ProfileBanner(data['active_tournament_banner'])
        if 'badges' in data:
            self.badges = [UserBadge(badge) for badge in data['badges']]
        if 'groups' in data:
            self.groups = [UserGroup(group) for group in data['groups']]
        if 'monthly_playcounts' in data:
            self.monthly_playcounts = [UserMonthlyPlaycount(playcount) for playcount in data['monthly_playcounts']]
        if 'statistics' in data:
            self.statistics = UserStatistics(data['statistics'])
        for attr in ('page', 'pending_beatmapset_count', 'previous_usernames', 'rank_history', 'ranked_beatmapset_counts',
                     'replays_watched_counts', 'scores_best_count', 'scores_first_count', 'scores_recent_count',
                     'statistics_rulesets', 'support_level', 'unread_pm_count', 'user_achievement', 'user_preferences',
                     'beatmap_playcounts_count', 'blocks', 'country', 'cover', 'favourite_beatmapset_count', 'follower_count',
                     'friends', 'graveyard_beatmapset_count', 'is_restricted', 'loved_beatmapset_count') + \
                    ('discord', 'interests', 'location', 'occupation', 'title', 'title_url', 'twitter', 'website'):  # Second tuple is optional User attributes.
            if attr in data:
                setattr(self, attr, data[attr])


class User(UserCompact):
    """
    Represents a User. Extends UserCompact object with additional attributes.

    **Attributes**

    discord: :class:`str`

    has_supported: :class:`bool`
        whether or not ever being a supporter in the past

    interests: :class:`str`

    join_date: :class:`Timestamp`

    kudosu: :class:`dict`
        a map containing keys total and available

    location: :class:`str`

    max_blocks: :class:`int`
        maximum number of users allowed to be blocked

    max_friends: :class:`int`
        maximum number of friends allowed to be added

    occupation: :class:`str`

    playmode: :class:`GameMode`

    playstyle: :class:`list`
        list containing objects of type :class:`str`. Device choices of the user.

    post_count: :class:`int`
        number of forum posts

    profile_order: :class:`list`
        list containing objects of type :class:`ProfilePage`. ordered list of sections in user profile page

    title: :class:`str`user-specific title

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


class ProfileBanner:
    """
    **Attributes**

    id: :class:`int`

    tournament_id: :class:`int`

    image: :class:`str`
    """
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
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']


class UserAccountHistory:
    """
    **Attributes**

    id: :class:`int`

    type: :class:`str`
        Can be one of the following: note, restriction, or silence.

    timestamp: :class:`Timestamp`

    length: :class:`int`
        In seconds.
    """
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.timestamp = data['timestamp']
        self.length = data['length']


class UserBadge:
    """
    **Attributes**

    awarded_at: :class:`Timestamp`

    description: :class:`str`

    image_url: :class:`str`

    url: :class:`str`
    """
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
    def __init__(self, data):
        self.start_date = data['start_date']
        self.count = data['count']


class UserGroup:
    """
    Describes the :class:`Group` membership of a :class:`User`. It contains all of the attributes of the :class:`Group`, in addition to what is listed here.

    **Attributes**

    playmodes: :class:`list`
        list containing objects of type :class:`str`. GameModes which the member is responsible for, e.g. in the case of BN/NAT (only present when has_playmodes is set on Group)
    """
    def __init__(self, data):
        self.id = data['id']
        self.identifier = data['identifier']
        self.is_probationary = data['is_probationary']
        self.name = data['name']
        self.short_name = data['short_name']
        self.description = data['description']
        self.colour = data['colour']
        if 'playmodes' in data:
            self.playmodes = data['playmodes']


class UserStatistics:
    """
    A summary of various gameplay statistics for a User. Specific to a GameMode

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
        if 'user' in data:
            self.user = UserCompact(data['user'])


class WikiPage:
    """
    Represents a wiki article

    **Attributes**

    layout: :class:`str`
        The layout type for the page.

    locale: :class:`str`
        All lowercase BCP 47 language tag.

    markdown: :class:`str`
        Markdown content.

    path: :class:`str`
        Path of the article.

    subtitle: :class:`str`
        The article's subtitle.

    tags: :class:`list`
        list containing objects of type :class:`str`. Associated tags for the article.

    title: :class:`str`
        The article's title.
    """
    def __init__(self, data):
        self.layout = data['layout']
        self.locale = data['locale']
        self.markdown = data['markdown']
        self.path = data['path']
        self.subtitle = data['subtitle']
        self.tags = data['tags']
        self.title = data['title']


class Path:
    def __init__(self, path, scope):
        self.path = path
        if type(scope) == str:
            scope = Scope(scope)
        self.scope = scope

    @classmethod
    def beatmap_lookup(cls):
        return cls("beatmaps/lookup", 'public')

    @classmethod
    def user_beatmap_score(cls, beatmap, user):
        return cls(f"beatmaps/{beatmap}/scores/users/{user}", 'public')

    @classmethod
    def beatmap_scores(cls, beatmap):
        return cls(f"beatmaps/{beatmap}/scores", 'public')

    @classmethod
    def beatmap(cls, beatmap):
        return cls(f"beatmaps/{beatmap}", 'public')

    @classmethod
    def beatmapset_discussion_posts(cls):
        return cls('beatmapsets/discussions/posts', 'public')

    @classmethod
    def beatmapset_discussion_votes(cls):
        return cls('beatmapsets/discussions/votes', 'public')

    @classmethod
    def beatmapset_discussions(cls):
        return cls('beatmapsets/discussions', 'public')

    @classmethod
    def create_new_pm(cls):
        return cls('chat/new', 'chat.write')

    @classmethod
    def get_updates(cls):
        return cls('chat/updates', 'lazer')

    @classmethod
    def get_channel_messages(cls, channel):
        return cls(f'chat/channels/{channel}/messages', 'lazer')

    @classmethod
    def send_message_to_channel(cls, channel):
        return cls(f'chat/channels/{channel}/messages', 'lazer')

    @classmethod
    def join_channel(cls, channel, user):
        return cls(f'chat/channels/{channel}/users/{user}', 'lazer')

    @classmethod
    def leave_channel(cls, channel, user):
        return cls(f'chat/channels/{channel}/users/{user}', 'lazer')

    @classmethod
    def mark_channel_as_read(cls, channel, message):
        return cls(f'chat/channels/{channel}/mark-as-read/{message}', 'lazer')

    @classmethod
    def get_channel_list(cls):
        return cls('chat/channels', 'lazer')

    @classmethod
    def create_channel(cls):
        return cls('chat/channels', 'lazer')

    @classmethod
    def get_channel(cls, channel):
        return cls(f'chat/channels/{channel}', 'lazer')

    @classmethod
    def get_comments(cls):
        return cls('comments', None)

    @classmethod
    def post_new_comment(cls):
        return cls('comments', 'lazer')

    @classmethod
    def get_comment(cls, comment):
        return cls(f'comments/{comment}', None)

    @classmethod
    def edit_comment(cls, comment):
        return cls(f'comments/{comment}', 'lazer')

    @classmethod
    def delete_comment(cls, comment):
        return cls(f'comments/{comment}', 'lazer')

    @classmethod
    def add_comment_vote(cls, comment):
        return cls(f'comments/{comment}/vote', 'lazer')

    @classmethod
    def remove_comment_vote(cls, comment):
        return cls(f'comments/{comment}/vote', 'lazer')

    @classmethod
    def reply_topic(cls, topic):
        return cls(f'forums/topics/{topic}/reply', 'forum.write')

    @classmethod
    def create_topic(cls):
        return cls('forums/topics', 'forum.write')

    @classmethod
    def get_topic_and_posts(cls, topic):
        return cls(f'forums/topics/{topic}', 'public')

    @classmethod
    def edit_topic(cls, topic):
        return cls(f'forums/topics/{topic}', 'forum.write')

    @classmethod
    def edit_post(cls, post):
        return cls(f'forums/posts/{post}', 'forum.write')

    @classmethod
    def search(cls):
        return cls('search', 'public')

    @classmethod
    def get_user_high_score(cls, room, playlist, user):
        return cls(f'rooms/{room}/playlist/{playlist}/scores/users/{user}', 'lazer')

    @classmethod
    def get_scores(cls, room, playlist):
        return cls(f'rooms/{room}/playlist/{playlist}/scores', 'public')

    @classmethod
    def get_score(cls, room, playlist, score):
        return cls(f'rooms/{room}/playlist/{playlist}/scores/{score}', 'lazer')

    @classmethod
    def get_notifications(cls):
        return cls('notifications', 'lazer')

    @classmethod
    def mark_notifications_as_read(cls):
        return cls('notifications/mark-read', 'lazer')

    @classmethod
    def revoke_current_token(cls):
        return cls('oauth/tokens/current', 'public')

    @classmethod
    def get_ranking(cls, mode, type):
        return cls(f'rankings/{mode}/{type}', 'public')

    @classmethod
    def get_spotlights(cls):
        return cls('spotlights', 'public')

    @classmethod
    def get_own_data(cls, mode=''):
        return cls(f'me/{mode}', 'identify')

    @classmethod
    def get_user_kudosu(cls, user):
        return cls(f'users/{user}/kudosu', 'public')

    @classmethod
    def get_user_scores(cls, user, type):
        return cls(f'users/{user}/scores/{type}', 'public')

    @classmethod
    def get_user_beatmaps(cls, user, type):
        return cls(f'users/{user}/beatmapset/{type}', 'public')

    @classmethod
    def get_user_recent_activity(cls, user):
        return cls(f'users/{user}/recent_activity', 'public')

    @classmethod
    def get_user(cls, user, mode=''):
        return cls(f'users/{user}/{mode}', 'public')

    @classmethod
    def get_users(cls):
        return cls('users', 'lazer')

    @classmethod
    def get_wiki_page(cls, locale, path):
        return cls(f'wiki/{locale}/{path}', None)

    @classmethod
    def get_score_by_id(cls, mode, score):
        return cls(f'scores/{mode}/{score}', 'public')
