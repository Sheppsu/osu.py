from ..enums import GameModeStr, BeatmapsetEventType
from .discussion import BeatmapsetDiscussion
from .beatmap import BeatmapsetCompact
from dateutil import parser

from ..util import prettify


class BeatmapsetEvent:
    """
    Represent a beatmapset event. This object is relevant for the :func:`osu.Client.get_beatmapset_events` endpoint.

    **Attributes**

    id: :class:`int`

    type: :class:`BeatmapsetEventType`

    comment: Union[:class:`BeatmapsetEventComment`, :class:`NoneType`]
        Is :class:`NoneType` for the following types:
        - :class:`BeatmapsetEventType.LOVE`
        - :class:`BeatmapsetEventType.QUALIFY`
        - :class:`BeatmapsetEventType.APPROVE`
        - :class:`BeatmapsetEventType.RANK`

    created_at: :class:`datetime.datetime`

    user_id: Union[:class:`int`, :class:`NoneType`]

    beatmapset: Union[:class:`BeatmapsetCompact`, :class:`NoneType`]

    discussion: Union[:class:`BeatmapsetDiscussion`, :class:`NoneType`]
    """
    __slots__ = (
        "id", "type", "comment", "created_at", "user_id", "beatmapset", "discussion"
    )

    def __init__(self, data):
        self.id = data['id']
        self.type = BeatmapsetEventType(data['type'])
        self.comment = data['comment']
        if self.comment is not None:
            self.comment = BeatmapsetEventComment(self.comment, self.type)
        self.created_at = parser.parse(data['created_at'])
        self.user_id = data.get('user_id')
        self.beatmapset = BeatmapsetCompact(data['beatmapset']) if data.get("beatmapset") is not None else None
        self.discussion = BeatmapsetDiscussion(data['discussion']) if data.get('discussion') is not None else None

    def __repr__(self):
        return prettify(self, 'type', 'beatmapset')


class BeatmapsetEventComment:
    """
    This object holds some extra information of the event.

    **Attributes**

    beatmap_discussion_id: Union[:class:`int`, :class:`NoneType`]

    beatmap_discussion_post_id: Union[:class:`int`, :class:`NoneType`]

    event_data: Union[:class:`BeatmapsetEventNominate`, :class:`BeatmapsetEventRemoveFromLoved`,
    :class:`BeatmapsetEventDisqualify`, :class:`BeatmapsetEventKudosuGain`, :class:`BeatmapsetEventKudosuLost`,
    :class:`BeatmapsetEventKudosuRecalculate`, :class:`BeatmapsetEventDiscussionLock`,
    :class:`BeatmapsetEventNominationReset`, :class:`BeatmapsetEventNominationResetReceived`,
    :class:`BeatmapsetEventGenreEdit`, :class:`BeatmapsetEventLanguageEdit`, :class:`BeatmapsetEventNsfwToggle`,
    :class:`BeatmapsetEventOffsetEdit`, :class:`BeatmapsetEventBeatmapOwnerChange`]
        The type of this attribute depends on the type of the BeatmapsetEvent object.
    """

    __slots__ = (
        "beatmap_discussion_id", "beatmap_discussion_post_id", "event_data"
    )
    event_types = {
        BeatmapsetEventType.NOMINATE: 'BeatmapsetEventNominate',
        BeatmapsetEventType.REMOVE_FROM_LOVED: 'BeatmapsetEventRemoveFromLoved',
        BeatmapsetEventType.DISQUALIFY: 'BeatmapsetEventDisqualify',
        BeatmapsetEventType.KUDOSU_GAIN: 'BeatmapsetEventKudosuGain',
        BeatmapsetEventType.KUDOSU_LOST: 'BeatmapsetEventKudosuLost',
        BeatmapsetEventType.KUDOSU_RECALCULATE: 'BeatmapsetEventKudosuRecalculate',
        BeatmapsetEventType.DISCUSSION_LOCK: 'BeatmapsetEventDiscussionLock',
        BeatmapsetEventType.NOMINATION_RESET: 'BeatmapsetEventNominationReset',
        BeatmapsetEventType.NOMINATION_RESET_RECEIVED: 'BeatmapsetEventNominationResetReceived',
        BeatmapsetEventType.GENRE_EDIT: 'BeatmapsetEventGenreEdit',
        BeatmapsetEventType.LANGUAGE_EDIT: 'BeatmapsetEventLanguageEdit',
        BeatmapsetEventType.NSFW_TOGGLE: 'BeatmapsetEventNsfwToggle',
        BeatmapsetEventType.OFFSET_EDIT: 'BeatmapsetEventOffsetEdit',
        BeatmapsetEventType.BEATMAP_OWNER_CHANGE: 'BeatmapsetEventBeatmapOwnerChange',
    }

    def __init__(self, data, type):
        self.beatmap_discussion_id = data.get('beatmap_discussion_id')
        self.beatmap_discussion_post_id = data.get('beatmap_discussion_post_id')
        self.event_data = globals()[self.event_types[type]](data) if type in self.event_types else None

    def __repr__(self):
        return prettify(self, 'beatmap_discussion_id', 'beatmap_discussion_post_id')


class BeatmapsetEventNominate:
    """
    **Attributes**

    modes: Sequence[:class:`GameModeStr`]
    """
    __slots__ = ("modes",)

    def __init__(self, data):
        self.modes = [GameModeStr(mode) for mode in data['modes']]

    def __repr__(self):
        return prettify(self, 'modes')


class BeatmapsetEventRemoveFromLoved:
    """
    **Attributes**

    reason: :class:`str`
    """
    __slots__ = ("reason",)

    def __init__(self, data):
        self.reason = data['reason']

    def __repr__(self):
        return prettify(self, 'reason')


class BeatmapsetEventDisqualify:
    """
    **Attributes**

    nominator_ids: Sequence[:class:`int`]
    """
    __slots__ = ("nominator_ids",)

    def __init__(self, data):
        self.nominator_ids = data['nominator_ids']

    def __repr__(self):
        return prettify(self, 'nominator_ids')


class BeatmapsetEventVote:
    """
    **Attributes**

    user_id: :class:`int`

    score: :class:`int`
    """
    __slots__ = ("user_id", "score")

    def __init__(self, data):
        self.user_id = data['user_id']
        self.score = data['score']

    def __repr__(self):
        return prettify(self, 'user_id', 'score')


class BeatmapsetEventKudosuChange:
    """
    **Attributes**

    new_votes: Union[:class:`BeatmapsetEventVote`, :class:`NoneType`]

    votes: Union[Sequence[:class:`BeatmapsetEventVote`], :class:`NoneType`]
    """
    __slots__ = ("new_votes", "votes")

    def __init__(self, data):
        self.new_votes = BeatmapsetEventVote(data['new_votes']) if data.get('new_votes') is not None else None
        self.votes = list(map(BeatmapsetEventVote, data['votes'])) if data.get('votes') is not None else None

    def __repr__(self):
        return prettify(self, 'new_votes', 'votes')


class BeatmapsetEventKudosuGain(BeatmapsetEventKudosuChange):
    __doc__ = BeatmapsetEventKudosuChange.__doc__


class BeatmapsetEventKudosuLost(BeatmapsetEventKudosuChange):
    __doc__ = BeatmapsetEventKudosuChange.__doc__


class BeatmapsetEventKudosuRecalculate:
    """
    **Attributes**

    new_votes: Union[:class:`BeatmapsetEventVote`, :class:`NoneType`]
    """
    __slots__ = ("new_votes",)

    def __init__(self, data):
        self.new_votes = BeatmapsetEventVote(data['new_votes']) if data.get('new_votes') is not None else None

    def __repr__(self):
        return prettify(self, 'new_votes')


class BeatmapsetEventDiscussionLock:
    """
    **Attributes**

    reason: :class:`str`
    """
    __slots__ = ("reason",)

    def __init__(self, data):
        self.reason = data['reason']

    def __repr__(self):
        return prettify(self, 'reason')


class BeatmapsetEventNominationReset:
    """
    **Attributes**

    nominator_ids: Sequence[:class:`int`]
    """
    __slots__ = ("nominator_ids",)

    def __init__(self, data):
        self.nominator_ids = data['nominator_ids']

    def __repr__(self):
        return prettify(self, 'nominator_ids')


class BeatmapsetEventNominationResetReceived:
    """
    **Attributes**

    source_user_id: :class:`int`

    source_user_name: :class:`str`
    """
    __slots__ = ("source_user_id", "source_user_username")

    def __init__(self, data):
        self.source_user_id = data['source_user_id']
        self.source_user_username = data['source_user_username']

    def __repr__(self):
        return prettify(self, 'source_user_id', 'source_user_username')


class BeatmapsetEventEdit:
    """
    **Attributes**

    old: :class:`str`

    new: :class:`str`
    """
    __slots__ = ("old", "new")

    def __init__(self, data):
        self.old = data['old']
        self.new = data['new']

    def __repr__(self):
        return prettify(self, 'old', 'new')


class BeatmapsetEventGenreEdit(BeatmapsetEventEdit):
    __doc__ = BeatmapsetEventEdit.__doc__


class BeatmapsetEventLanguageEdit(BeatmapsetEventEdit):
    __doc__ = BeatmapsetEventEdit.__doc__


class BeatmapsetEventNsfwToggle(BeatmapsetEventEdit):
    """
    **Attributes**

    old: :class:`bool`

    new: :class:`bool`
    """


class BeatmapsetEventOffsetEdit(BeatmapsetEventEdit):
    """
    **Attributes**

    old: :class:`int`

    new: :class:`int`
    """


class BeatmapsetEventBeatmapOwnerChange:
    """
    **Attributes**

    beatmap_id: :class:`int`

    beatmap_version: :class:`str`

    new_user_id: :class:`int`

    new_user_username: :class:`str`
    """
    __slots__ = ("beatmap_id", "beatmap_version", "new_user_id", "new_user_username")

    def __init__(self, data):
        self.beatmap_id = data['beatmap_id']
        self.beatmap_version = data['beatmap_version']
        self.new_user_id = data['new_user_id']
        self.new_user_username = data['new_user_username']

    def __repr__(self):
        return prettify(self, 'beatmap_id', 'new_user_username')
