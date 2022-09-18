from ..enums import RankStatus, GameModeStr, GameModeInt
from .user import UserCompact, CurrentUserAttributes
from dateutil import parser

from ..util import prettify


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

    status: :class:`RankStatus`

    title: :class:`str`

    title_unicode: :class:`str`

    user_id: :class:`int`

    video: :class:`str`

    **Possible Attributes**

    (Information about these attributes is lacking on the documentation)

    beatmaps: :class:`list`
        list containing objects of type :class:`Beatmap`

    converts

    current_user_attributes: :class:`CurrentUserAttributes`

    description

    discussions

    events

    genre

    has_favourited: :class:`bool`

    language

    nominations: :class:`dict`
        Contains items current: :class:`int` and required: :class:`int`

    ratings

    recent_favourites

    related_users

    user: :class:`UserCompact`
    """
    __slots__ = (
        "artist", "artist_unicode", "covers", "creator", "favourite_count", "id", "nsfw",
        "play_count", "preview_url", "source", "status", "title", "title_unicode", "user_id",
        "video", "beatmaps", "current_user_attributes", "user", "converts", "description", "discussions",
        "events", "genre", "has_favourited", "language", "nominations", "ratings", "recent_favourites",
        "related_users"
    )

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
        self.status = RankStatus[data['status'].upper()]
        self.title = data['title']
        self.title_unicode = data['title_unicode']
        self.user_id = data['user_id']
        self.video = data['video']

        # Documentation lacks information on all the possible attributes :/
        self.beatmaps = list(map(Beatmap, data['beatmaps'])) if 'beatmaps' in data else None
        self.current_user_attributes = CurrentUserAttributes(data['current_user_attributes'],
                                                             'BeatmapsetDiscussionPermissions') \
            if 'current_user_attributes' in data else None
        self.user = UserCompact(data['user']) if 'user' in data else None
        self.converts = data.get('converts')
        self.description = data.get('description')
        self.discussions = data.get('discussions')
        self.events = data.get('events')
        self.genre = data.get('genre')
        self.has_favourited = data.get('has_favourited')
        self.language = data.get('language')
        self.nominations = data.get('nominations')
        self.ratings = data.get('ratings')
        self.recent_favourites = data.get('recent_favourites')
        self.related_users = data.get('related_users')

    def __repr__(self):
        return prettify(self, 'artist', 'title', 'creator')


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
    __slots__ = (
        "cover", "cover_2x", "card", "card_2x", "list", "list_2x", "slimcover", "slimcover_2x"
    )

    def __init__(self, data):
        self.cover = data['cover']
        self.cover_2x = data['cover@2x']
        self.card = data['card']
        self.card_2x = data['card@2x']
        self.list = data['list']
        self.list_2x = data['list@2x']
        self.slimcover = data['slimcover']
        self.slimcover_2x = data['slimcover@2x']

    def __repr__(self):
        return prettify(self, 'cover')


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
        Deprecated. Is always true.

    discussion_locked: :class:`bool`

    hype: :class:`dict`
        Contains items current: :class:`int` and required: :class:`int`

    is_scoreable: :class:`bool`

    last_updated: :class:`datetime.datetime`

    legacy_thread_url: :class:`str`

    nominations: :class:`dict`
        Contains items current: :class:`int` and required: :class:`int`

    ranked: :class:`RankStatus`

    ranked_date: :class:`datetime.datetime`

    source: :class:`str`

    storyboard: :class:`bool`

    submitted_date: :class:`datetime.datetime`

    tags: :class:`str`
    """
    __slots__ = (
        "availability", "bpm", "can_be_hyped", "creator", "discussion_enabled", "discussion_locked",
        "hype", "is_scoreable", "last_updated", "legacy_thread_url", "ranked", "ranked_date", "storyboard",
        "submitted_date", "tags", "has_favourited", "nominations"
    )

    def __init__(self, data):
        super().__init__(data)
        self.availability = data['availability']
        self.bpm = data['bpm']
        self.can_be_hyped = data['can_be_hyped']
        self.creator = data['creator']
        self.discussion_enabled = True  # Deprecated, all beatmapset discussions are enabled
        self.discussion_locked = data['discussion_locked']
        self.hype = data['hype']
        self.is_scoreable = data['is_scoreable']
        self.last_updated = parser.parse(data['last_updated']) if data.get('last_updated') is not None else None
        self.legacy_thread_url = data['legacy_thread_url']
        self.ranked_date = parser.parse(data['ranked_date']) if data.get('ranked_date') is not None else None
        self.source = data['source']
        self.storyboard = data['storyboard']
        self.tags = data['tags']
        self.submitted_date = parser.parse(data['submitted_date']) if data.get('submitted_date') is not None else None
        self.has_favourited = data['has_favourited'] if 'has_favourited' in data else None
        self.ranked = RankStatus(int(data['ranked']))
        self.nominations = data['nominations'] if 'nominations' in data else None

    def __repr__(self):
        return super().__repr__()


class BeatmapCompact:
    """
    Represents a beatmap.

    **Attributes**

    beatmapset_id: :class:`int`

    difficulty_rating: :class:`float`

    id: :class:`int`

    mode: :class:`GameModeStr`

    status: :class:`RankStatus`

    total_length: :class:`int`

    user_id: :class:`int`

    version: :class:`str`

    **Possible Attributes**

    beatmapset: :class:`Beatmapset` | :class:`BeatmapsetCompact` | :class:`NoneType`
        Beatmapset for Beatmap object, BeatmapsetCompact for BeatmapCompact object.
        null if the beatmap doesn't have associated beatmapset (e.g. deleted).

    checksum: :class:`str` or :class:`NoneType`

    failtimes: :class:`Failtimes`

    max_combo: :class:`int`
    """
    __slots__ = (
        "difficulty_rating", "id", "mode", "status", "total_length", "user_id", "version",
        "checksum", "max_combo", "failtimes", "beatmapset"
    )

    def __init__(self, data):
        self.difficulty_rating = data['difficulty_rating']
        self.id = data['id']
        self.mode = GameModeStr(data['mode'])
        self.status = RankStatus[data['status'].upper()]
        self.total_length = data['total_length']
        self.user_id = data['user_id']
        self.version = data['version']
        self.checksum = data.get("checksum", None)
        self.max_combo = data.get("max_combo", None)
        self.failtimes = Failtimes(data['failtimes']) if "failtimes" in data else None

        if 'beatmapset' in data and data['beatmapset'] is not None:
            if type(self).__name__ == 'Beatmap':
                self.beatmapset = Beatmapset(data['beatmapset'])
            else:
                self.beatmapset = BeatmapsetCompact(data['beatmapset'])
        else:
            self.beatmapset = None

    def __repr__(self):
        return prettify(self, 'version', 'beatmapset')


class BeatmapDifficultyAttributes:
    """
    Represent beatmap difficulty attributes. Following fields are always present and
    then there are additional fields for different rulesets.

    **Attributes**

    The parameters depend on the ruleset, but the following two attributes are present in all rulesets.

    max_combo: :class:`int`

    star_rating: :class:`float`

    mode_attributes: Union[:class:`OsuBeatmapDifficultyAttributes`, :class:`TaikoBeatmapDifficultyAttributes`,
    :class:`FruitsBeatmapDifficultyAttributes`, :class:`ManiaBeatmapDifficultyAttributes`, :class:`None`]
        Can be none for some beatmaps that are bugged and have no difficulty attributes.

    osu
        aim_difficulty: :class:`float`

        approach_rate: :class:`float`

        flashlight_difficulty: :class:`float`

        overall_difficulty: :class:`float`

        slider_factor: :class:`float`

        speed_difficulty: :class:`float`

    taiko
        stamina_difficulty: :class:`float`

        rhythm_difficulty: :class:`float`

        colour_difficulty: :class:`float`

        approach_rate: :class:`float`

        great_hit_window: :class:`float`

    fruits
        approach_rate: :class:`float`

    mania
        great_hit_window: :class:`float`

        score_multiplier: :class:`float`
    """
    __slots__ = (
        "max_combo", "star_rating", "type", "mode_attributes"
    )

    def __init__(self, data):
        data = data['attributes']
        self.max_combo = data['max_combo']
        self.star_rating = data['star_rating']
        if "aim_difficulty" in data:
            self.type = "osu"
            self.mode_attributes = OsuBeatmapDifficultyAttributes(data)
        elif "stamina_difficulty" in data:
            self.type = "taiko"
            self.mode_attributes = TaikoBeatmapDifficultyAttributes(data)
        elif "score_multiplier" in data:
            self.type = "mania"
            self.mode_attributes = ManiaBeatmapDifficultyAttributes(data)
        elif "approach_rate" in data:
            self.type = 'fruits'
            self.mode_attributes = FruitsBeatmapDifficultyAttributes(data)
        else:
            self.type = None
            self.mode_attributes = None

    def __getattr__(self, item):
        return getattr(self.mode_attributes, item)

    def __repr__(self):
        return prettify(self, 'star_rating', 'type', 'mode_attributes')


class OsuBeatmapDifficultyAttributes:
    """
    osu!standard beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    aim_difficulty: :class:`float`

    approach_rate: :class:`float`

    flashlight_difficulty: :class:`float`

    overall_difficulty: :class:`float`

    slider_factor: :class:`float`

    speed_difficulty: :class:`float`
    """
    __slots__ = (
        "aim_difficulty", "approach_rate", "flashlight_difficulty",
        "overall_difficulty", "slider_factor", "speed_difficulty"
    )

    def __init__(self, data):
        self.aim_difficulty = data['aim_difficulty']
        self.approach_rate = data['approach_rate']
        self.flashlight_difficulty = data['flashlight_difficulty']
        self.overall_difficulty = data['overall_difficulty']
        self.slider_factor = data['slider_factor']
        self.speed_difficulty = data['speed_difficulty']

    def __repr__(self):
        return prettify(self, 'aim_difficulty', 'approach_rate', 'overall_difficulty')


class TaikoBeatmapDifficultyAttributes:
    """
    osu!taiko beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    stamina_difficulty: :class:`float`

    rhythm_difficulty: :class:`float`

    colour_difficulty: :class:`float`

    approach_rate: :class:`float`

    great_hit_window: :class:`float`
    """

    __slots__ = (
        "stamina_difficulty", "approach_rate", "rhythm_difficulty",
        "colour_difficulty", "great_hit_window"
    )

    def __init__(self, data):
        self.stamina_difficulty = data['stamina_difficulty']
        self.approach_rate = data['approach_rate']
        self.rhythm_difficulty = data['rhythm_difficulty']
        self.colour_difficulty = data['colour_difficulty']
        self.great_hit_window = data['great_hit_window']

    def __repr__(self):
        return prettify(self, 'approach_rate', 'great_hit_window')


class FruitsBeatmapDifficultyAttributes:
    """
    osu!catch beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    approach_rate: :class:`float`
    """

    __slots__ = (
        "approach_rate"
    )

    def __init__(self, data):
        self.approach_rate = data['approach_rate']

    def __repr__(self):
        return prettify(self, 'approach_rate')


class ManiaBeatmapDifficultyAttributes:
    """
    osu!mania beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    great_hit_window: :class:`float`

    score_multiplier: :class:`float`
    """

    __slots__ = (
        "score_multiplier", "great_hit_window"
    )

    def __init__(self, data):
        self.score_multiplier = data['score_multiplier']
        self.great_hit_window = data['great_hit_window']

    def __repr__(self):
        return prettify(self, 'score_multiplier', 'great_hit_window')


class Failtimes:
    """
    All attributes are optional but there's always at least one attribute present.

    **Attributes**

    exit: Sequence[:class:`int`]
        Sequence of integers. List is length 100.

    fail: Sequence[:class:`int`]
        Sequence of integers. List is length 100.
    """
    def __init__(self, data):
        if 'exit' in data:
            self.exit = data['exit']
        if 'fail' in data:
            self.fail = data['fail']

    def __repr__(self):
        try:
            return prettify(self, 'exit')
        except AttributeError:
            return prettify(self, 'fail')


class Beatmap(BeatmapCompact):
    """
    Represent a beatmap. This extends :class:`BeatmapCompact` with additional attributes.

    **Attributes**

    accuracy: :class:`float`

    ar: :class:`float`

    beatmapset_id: :class:`int`

    bpm: :class:`float` or :class:`NoneType`

    convert: :class:`bool`

    count_circles: :class:`int`

    count_sliders: :class:`int`

    count_spinners: :class:`int`

    cs: :class:`float`

    deleted_at: :class:`datetime.datetime` or :class:`NoneType`

    drain: :class:`float`

    hit_length: :class:`int`

    is_scoreable: :class:`bool`

    last_updated: :class:`datetime.datetime`

    mode_int: :class:`GameModeInt`

    passcount: :class:`int`

    playcount: :class:`int`

    ranked: :class:`RankStatus`

    url: :class:`str`
    """
    __slots__ = (
        "ranked", "url", "playcount", "passcount", "mode_int", "last_updated",
        "is_scoreable", "hit_length", "drain", "deleted_at", "cs", "count_spinners",
        "count_circles", "count_sliders", "convert", "bpm", "beatmapset_id", "ar",
        "accuracy"
    )

    def __init__(self, data):
        super().__init__(data)
        self.ranked = RankStatus(int(data['ranked']))
        self.url = data['url']
        self.playcount = data['playcount']
        self.passcount = data['passcount']
        self.mode_int = GameModeInt(data['mode_int'])
        self.last_updated = parser.parse(data['last_updated'])
        self.is_scoreable = data['is_scoreable']
        self.hit_length = data['hit_length']
        self.drain = data['drain']
        self.deleted_at = parser.parse(data['deleted_at']) if data['deleted_at'] is not None else None
        self.cs = data['cs']
        self.count_spinners = data['count_spinners']
        self.count_sliders = data['count_sliders']
        self.count_circles = data['count_circles']
        self.convert = data['convert']
        self.bpm = data['bpm']
        self.beatmapset_id = data['beatmapset_id']
        self.ar = data['ar']
        self.accuracy = data['accuracy']

    def __repr__(self):
        return super().__repr__()


class BeatmapPlaycount:
    """
    Represent the playcount of a beatmap.

    **Attributes**

    beatmap_id: :class:`int`

    beatmap: :class:`BeatmapCompact` or :class:`NoneType`

    beatmapset: :class:`BeatmapsetCompact` or :class:`NoneType`

    count: :class:`int`
    """
    __slots__ = (
        "beatmap_id", "beatmap", "beatmapset", "count"
    )

    def __init__(self, data):
        self.beatmap_id = data['beatmap_id']
        self.beatmap = BeatmapCompact(data['beatmap']) if data['beatmap'] is not None else None
        self.beatmapset = BeatmapsetCompact(data['beatmapset']) if data['beatmapset'] is not None else None
        self.count = data['count']

    def __repr__(self):
        return prettify(self, 'beatmap_id', 'count')
