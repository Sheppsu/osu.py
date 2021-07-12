from .constants import int_to_status


class DataUnpacker:
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
    chat.write
        Allows sending chat messages on a user's behalf; exclusive to Chat Bots
    bot
        Chat Bot and Client Credentials Grant exclusive scope.
    """
    valid_scopes = [
        'bot',
        'chat.write',
        'forum.write',
        'friends.read',
        'identify',
        'public',
    ]

    def __init__(self, scopes):
        if type(scopes) == str:
            scopes = [scopes]
        for scope in scopes:
            if scope not in self.valid_scopes:
                raise NameError(f"{scope} is not a valid scope. The valid scopes consist of {','.join(self.valid_scopes)}")
        self.scopes = ' '.join(scopes)

    @classmethod
    def default(cls):
        return cls(['public', 'identify'])

    def __str__(self):
        return ", ".join(self.scopes)

    def __contains__(self, item):
        return item in self.scopes


class BeatmapCompact(DataUnpacker):
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
        exceptions = {'failtimes': (Failtimes, False)}
        super().__init__(data, exceptions, ('beatmapset',))
        if 'beatmapset' in data and data['beatmapset'] is not None:
            if type(self).__name__ == 'Beatmap':
                self.beatmapset = Beatmapset(data['beatmapset'])
            else:
                self.beatmapset = BeatmapsetCompact(data['beatmapset'])


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


class Score(DataUnpacker):
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
        exceptions = {'statistics': (ScoreStatistics, False), 'beatmap': (BeatmapCompact, False),
                      'beatmapset': (BeatmapsetCompact, False)}
        super().__init__(data, exceptions)


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


class BeatmapsetCompact(DataUnpacker):
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

    nominations

    ratings

    recent_favourites

    related_users

    user
    """
    def __init__(self, data):
        exceptions = {'covers': (Covers, False), 'beatmaps': (Beatmap, True)}
        super().__init__(data, exceptions)


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

    nominations: :class:`dict`
        Contains two items, current: :class:`int` and required: :class:`int`

    ranked: :class:`str`
        Possible values consist of graveyard, wip, pending, ranked, approved, qualified, loved

    ranked_date: :class:`Timestamp`

    source: :class:`str`

    storyboard: :class:`bool`

    submitted_date: :class:`Timestamp`

    tags: :class:`str`

    has_favourited
    """
    def __init__(self, data):
        super().__init__(data)
        self.ranked = int_to_status[int(data['ranked'])]


class BeatmapsetDiscussion(DataUnpacker):
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
        exceptions = {'beatmap': (BeatmapCompact, False), 'beatmapset': (BeatmapsetCompact, False),
                      'current_user_attributes': (CurrentUserAttributes, False), 'starting_post': (BeatmapsetDiscussionPost, False),
                      'posts': (BeatmapsetDiscussionPost, True), 'votes': (BeatmapsetDiscussionVote, True)}
        super().__init__(data, exceptions)


class CurrentUserAttributes:
    # TODO: Name for type will be changing so look out for that
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
    """
    def __init__(self, data, type):
        self.type = type
        self.data = data


class BeatmapsetDiscussionPost(DataUnpacker):
    """
    Represents a post in a :class:`BeatmapsetDiscussion`.

    **Attributes**

    beatmapset_discussion_id: :class:`number

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
        super().__init__(data)


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


class ChatChannel(DataUnpacker):
    """
    Represents an individual chat "channel" in the game.

    **Attributes**

    channel_id: :class:`int`

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

    last_read_id: :class:`int`
        message_id of last message read (only returned in presence responses)

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
        exceptions = {'recent_messages': (ChatMessage, True)}
        super().__init__(data, exceptions)


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


class Comment(DataUnpacker):
    """
    Represents a single comment.

    **Attributes**

    commentable_id: :class:`int`
        ID of the object the comment is attached to

    commentable_type: :class:`str`
        type of object the comment is attached to

    created_at: :class:`str`
        ISO 8601 date

    deleted_at: :class:`str`
        ISO 8601 date if the comment was deleted; null, otherwise

    edited_at: :class:`str`
        ISO 8601 date if the comment was edited; null, otherwise

    edited_by_id: :class:`
        int`user id of the user that edited the post; null, otherwise

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

    replies_count: :class:`
        int`number of replies to the comment

    updated_at: :class:`str`
        ISO 8601 date

    user_id: :class:`int`
        user ID of the poster

    votes_count: :class:`int`
        number of votes
    """
    def __init__(self, data):
        super().__init__(data)


class CommentBundle(DataUnpacker):
    """
    Comments and related data.

    **Attributes**

    commentable_meta: :class:`list`
        list containing objects of type :class:`CommentableMeta`. ID of the object the comment is attached to

    comments: :class:`list`
        list containing objects of type :class:`Comment`. List of comments ordered according to sort

    cursor	Cursor

    has_more: :class:`bool`
        If there are more comments or replies available

    has_more_id: :class:

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
        exceptions = {'commentable_meta': (CommentableMeta, True), 'comments': (Comment, True),
                      'cursor': (Cursor, False), 'included_comments': (Comment, True),
                      'pinned_comments': (Comment, True), 'users': (UserCompact, True)}
        super().__init__(data, exceptions)


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


class Cursor:
    """
    A structure included in some API responses containing the parameters to get the next set of results.
    The values of the cursor should be provided to next request of the same endpoint to get the next set of results.
    If there are no more results available, a cursor with a value of null is returned: "cursor": null.
    Note that sort option should also be specified for it to work.

    **Attributes**

    _id: :class:`int`

    _score: :class:`float`

    page: :class:`int`

    more_results: :class:`bool`
        Variable telling whether or not there are more results available.
    """
    def __init__(self, data):
        if not data:
            self.more_results = False
            return

        self.more_results = True
        if '_id' in data:
            self._id = data['_id']
            if '_score' in data:
                self._score = data['_score']
        else:
            self.page = data['page']

    @property
    def pagination_info(self):
        if hasattr(self, 'page'):
            info = f'cursor[page]={self.page}'
        else:
            info = f'cursor[_id]={self._id}'
            if hasattr(self, '_score'):
                info += f'&cursor[_score]={self._score}'
        return info


class Event(DataUnpacker):
    """
    The object has different attributes depending on its type. Following are attributes available to all types.

    **Attributes**

    created_at: :class:`Timestamp`

    id: :class:`int`

    type: :class:`Event.type`
        All types are listed under 'Event Types'

    **Event Types**

    :class:`Achievement`

    :class:`BeatmapPlaycount`

    :class:`BeatmapsetApprove`

    :class:`BeatmapsetDelete`

    :class:`BeatmapsetRevive`

    :class:`BeatmapsetUpdate`

    :class:`BeatmapsetUpload`

    :class:`Rank`

    :class:`RankLost`

    :class:`UserSupportAgain`

    :class:`UserSupportFirst`

    :class:`UserSupportGift`

    :class:`UsernameChange`

    **Event Objects**

    :class:`EventBeatmap`

    :class:`EventBeatmapset`

    :class:`EventUser`
    """
    def __init__(self, data):
        super().__init__(data)


class Achievement:
    """
    When user obtained an achievement.

    **Attributes**

    achievement: :class:`str`

    user: :class:`EventUser`
    """
    def __init__(self, data):
        self.achievement = data['achievement']
        self.user = EventUser(data['user'])


class BeatmapPlaycount:
    """
    When a beatmap has been played for certain number of times.

    **Attributes**

    beatmap: :class:`EventBeatmap`

    count: :class:`int`
    """
    def __init__(self, data):
        self.beatmap = EventBeatmap(data['beatmap'])
        self.count = data['count']


class BeatmapsetApprove:
    """
    When a beatmapset changes state.

    **Attributes**

    approval: :class:`str`
        Can be on of the following: ranked, approved, qualified, loved

    beatmapset: :class:`EventBeatmapset`

    user: :class:`EventUser`
        Beatmapset owner.
    """
    def __init__(self, data):
        self.approval = data['approval']
        self.beatmapset = EventBeatmapset(data['beatmapset'])
        self.user = EventUser(data['user'])


class BeatmapsetDelete:
    """
    When a beatmapset is deleted.

    **Attributes**

    beatmapset: :class:`EventBeatmapset`
    """
    def __init__(self, data):
        self.beatmapset = EventBeatmapset(data['beatmapset'])


class BeatmapsetRevive:
    """
    When a beatmapset in graveyard state is updated.

    **Attributes**

    beatmapset: :class:`EventBeatmapset`

    user: :class:`EventUser`
        Beatmapset owner.
    """
    def __init__(self, data):
        self.beatmapset = EventBeatmapset(data['beatmapset'])
        self.user = EventUser(data['user'])


class BeatmapsetUpdate:
    """
    When a beatmapset is updated.

    **Attributes**

    beatmapset: :class:`EventBeatmapset`

    user: :class:`EventUser`
        Beatmapset owner.
    """
    def __init__(self, data):
        self.beatmapset = EventBeatmapset(data['beatmapset'])
        self.user = EventUser(data['user'])


class BeatmapsetUpload:
    """
    When a new beatmapset is uploaded.

    **Attributes**

    beatmapset: :class:`EventBeatmapset`

    user: :class:`EventUser`
        Beatmapset owner.
    """
    def __init__(self, data):
        self.beatmapset = EventBeatmapset(data['beatmapset'])
        self.user = EventUser(data['user'])


class Rank:
    """
    When a user achieves a certain rank on a beatmap.

    **Attributes**

    scoreRank: :class:`str`

    rank: :class:`int`

    mode: :class:`GameMode`

    beatmap: :class:`EventBeatmap`

    user: :class:`EventUser`
    """
    def __init__(self, data):
        self.scoreRank = data['scoreRank']
        self.rank = data['rank']
        self.mode = data['mode']
        self.beatmap = EventBeatmap(data['beatmap'])
        self.user = EventUser(data['user'])


class RankLost:
    """
    When a user loses first place to another user.

    **Attributes**

    mode: :class:`GameMode`

    beatmap: :class:`EventBeatmap`

    user: :class:`EventUser`
    """
    def __init__(self, data):
        self.mode = data['mode']
        self.beatmap = EventBeatmap(data['beatmap'])
        self.user = EventUser(data['user'])


class UserSupportAgain:
    """
    When a user supports osu_api! for the second and onwards.

    **Attributes**

    user: :class:`EventUser`
    """
    def __init__(self, data):
        self.user = EventUser(data['user'])


class UserSupportFirst:
    """
    When a user becomes a supporter for the first time.

    **Attributes**

    user: :class:`EventUser`
    """
    def __init__(self, data):
        self.user = EventUser(data['user'])


class UserSupportGift:
    """
    When a user is gifted a supporter tag by another user.

    **Attributes**

    user: :class:`EventUser`

    """
    def __init__(self, data):
        self.user = EventUser(data['user'])


class UsernameChange:
    """
    When a user changes their username.

    **Attributes**

    user: :class:`EventUser`
        Includes previousUsername.
    """
    def __init__(self, data):
        self.user = EventUser(data['user'])


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


class EventUser:
    """
    **Attributes**

    username: :class:`str`

    url: :class:`str`

    previousUsername: :class:`str`
        Only for :class:`UsernameChange` event.
    """
    def __init__(self, data):
        self.username = data['username']
        self.url = data['url']
        if 'previousUsername' in data:
            self.previousUsername = data['previousUsername']


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

    description: :class:`str`

    colour: :class:`str`
    """
    def __init__(self, data):
        self.id = data['id']
        self.identifier = data['identifier']
        self.is_probationary = data['is_probationary']
        self.has_playmodes = data['has_playmodes']
        self.name = data['name']
        self.short_name = data['short_name']
        self.description = data['description']
        self.colour = data['colour']


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


class MultiplayerScore(DataUnpacker):
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
        exceptions = {'scores_around': (MultiplayerScoresAround, False),
                      'user': (User, False), 'statistics': (ScoreStatistics, False)}
        super().__init__(data, exceptions)


class MultiplayerScores:
    """
    An object which contains scores and related data for fetching next page of the result.
    To fetch the next page, make request to scores index (Client.get_scores) with relevant
    room and playlist, use the data in attribute next_page_query to fill in the 3 other optional queries.

    **Attributes**

    next_page_query: :class:`dict`
        Combines the data of cursor and params for easy use in querying the next page.

    cursor: :class:`MultiplayerScoresCursor`
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
        self.cursor = MultiplayerScoresCursor(data['cursor'])
        self.params = data['params']
        self.scores = [MultiplayerScore(score) for score in data['scores']]
        if 'total' in data:
            self.total = data['total']
        if 'user_score' in data:
            self.user_score = MultiplayerScore(data['user_score'])
        self.next_page_query = "&".join([f'{key}={value}' for key, value in {
            'sort': self.params['sort'],
            'limit': self.params['limit'],
            'cursor': {
                'score_id': self.cursor.score_id,
                'total_score': self.cursor.total_score
            }
        }])


class MultiplayerScoresAround:
    """
    **Attributes**

    higher: :class:`MultiplayerScores`

    lower: :class:`MultiplayerScores`
    """
    def __init__(self, data):
        self.higher = MultiplayerScores(data['higher'])
        self.lower = MultiplayerScores(data['lower'])


class MultiplayerScoresCursor:
    """
    An object which contains pointer for fetching further results of a request. It depends on the sort option.

    **Attributes**

    score_id: :class:`int`
        Last score id of current result (score_asc, score_desc).

    total_score: :class:`int`
        Last score's total score of current result (score_asc, score_desc).
    """
    def __init__(self, data):
        self.score_id = data['score_id']
        self.total_score = data['total_score']

    @property
    def pagination_info(self):
        return f"cursor[score_id]={self.score_id}&cursor[total_score]={self.total_score}"


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
            self.details = Details(data['details'])


class Details(DataUnpacker):
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
    def __init__(self, data):
        super().__init__(data)


class Rankings:
    """
    **Attributes**

    beatmapsets: :class:`list`
        list containing objects of type :class:`Beatmapset`. The list of beatmaps in the requested spotlight for the given mode; only available if type is charts

    cursor: :class:`Cursor`
        A cursor

    ranking: :class:`list`
        list containing objects of type :class:`UserStatistics`. Score details ordered by rank in descending order.

    spotlight: :class:`Spotlight`
        Spotlight details; only available if type is charts

    total: :class:`int`
        An approximate count of ranks available
    """
    def __init__(self, data):
        self.cursor = Cursor(data['cursor'])
        self.ranking = UserStatistics(data['ranking'])
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


class UserCompact(DataUnpacker):
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

    is_admin: :class:`bool`

    is_bng: :class:`bool`

    is_full_bn: :class:`bool`

    is_gmt: :class:`bool`

    is_limited_bn: :class:`bool`

    is_moderator: :class:`bool`

    is_nat: :class:`bool`

    is_restricted: :class:`bool`

    is_silenced: :class:`bool`

    loved_beatmapset_count: :class:`int`

    monthly_playcounts: :class:`list`
        list containing objects of type :class:`UserMonthlyPlaycount`

    page

    previous_usernames

    ranked_and_approved_beatmapset_count

    replays_watched_counts

    scores_best_count: :class:`int`

    scores_first_count: :class:`int`

    scores_recent_count: :class:`int`

    statistics

    statistics_rulesets: :class:`UserStatisticsRulesets`

    support_level

    unranked_beatmapset_count

    unread_pm_count

    user_achievements

    user_preferences

    rank_history
    """
    def __init__(self, data):
        exceptions = {'active_tournament_banner': (ProfileBanner, False),
                      'account_history': (UserAccountHistory, True),
                      'badges': (UserBadge, True), 'monthly_playcount': (UserMonthlyPlaycount, True),
                      'groups': (UserGroup, True)}
        super().__init__(data, exceptions)


class User(UserCompact):
    """
    Represents a User. Extends UserCompact object with additional attributes.

    **Attributes**

    cover_url: :class:`str`
        url of profile cover

    discord: :class:`str`

    has_supported: :class:`bool`
        whether or not ever being a supporter in the past

    interests: :class:`str`

    join_date: :class:`Timestamp`

    kudosu['available']: :class:`int`

    kudosu['total']: :class:`int`

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

    cover: :class:`dict`
        Contains keys 'custom_url', 'url', and 'id'.

    is_admin: :class:`bool`

    is_bng: :class:`bool`

    is_full_bn: :class:`bool`

    is_gmt: :class:`bool`

    is_limited_bn: :class:`bool`

    is_moderator: :class:`bool`

    is_nat: :class:`bool`

    is_restricted: :class:`bool`

    is_silenced: :class:`bool`
    """
    def __init__(self, data):
        super().__init__(data)


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


class UserMonthlyPlaycount(DataUnpacker):
    """
    Not documented
    """
    def __init__(self, data):
        super().__init__(data)


class UserGroup:
    """
    Describes the :class:`Group` membership of a :class:`User` - most of the attributes will be the same as the relevant :class:`Group`

    **Attributes**

    id: :class:`int`
        ID (of Group)

    identifier: :class:`str`
        Unique string to identify the group.

    is_probationary: :class:`bool`
        Whether members of this group are considered probationary.

    name: :class:`str`

    short_name: :class:`str`
        Short name of the group for display.

    description: :class:`str`

    colour: :class:`str`

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

    level.current: :class:`int`
        Current level.

    level.progress: :class:`int`
        Progress to next level.

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
        self.level_current = data['level.current']
        self.level_progress = data['level.progress']
        self.hit_accuracy = data['hit_accuracy']
        self.is_ranked = data['is_ranked']
        self.maximum_combo = data['maximum_combo']
        self.play_count = data['play_count']
        self.play_time = data['play_time']
        self.pp = data['pp']
        self.global_rank = data['global_rank']
        self.country_rank = data['country_rank']
        self.ranked_score = data['ranked_score']
        self.replays_watched_by_others = data['replays_watched_by_others']
        self.total_hits = data['total_hits']
        self.total_score = data['total_score']
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
