from typing import Dict, Optional, List, Union, TYPE_CHECKING

from ..enums import RankStatus, GameModeStr, GameModeInt
from ..util import prettify, get_optional, get_optional_list, get_required, fromisoformat
from .user import UserCompact
from .current_user_attributes import BeatmapsetPermissions


if TYPE_CHECKING:
    from datetime import datetime


__all__ = (
    "BeatmapsetCompact",
    "Beatmapset",
    "BeatmapCompact",
    "Beatmap",
    "BeatmapDifficultyAttributes",
    "OsuBeatmapDifficultyAttributes",
    "TaikoBeatmapDifficultyAttributes",
    "ManiaBeatmapDifficultyAttributes",
    "FruitsBeatmapDifficultyAttributes",
    "Failtimes",
    "Covers",
    "BaseNominations",
    "LegacyNominations",
    "Nominations",
    "CurrentNomination",
    "BeatmapPlaycount",
    "BeatmapsetRequiredNominations",
    "BeatmapsetRequirement",
    "BeatmapsetAvailability",
    "MetadataAttribute",
)


class BeatmapsetCompact:
    """
    Represents a beatmapset.

    **Attributes**

    artist: str

    artist_unicode: str

    background_url: str
        Not given by api but created locally based on beatmapset id.

    covers: :class:`Covers`

    creator: str

    favourite_count: int

    hype: Optional[:class:`BeatmapsetRequirement`]

    id: int

    nsfw: bool

    offset: int

    play_count: int

    preview_url: str

    source: str

    spotlight: bool

    status: :class:`RankStatus`

    title: str

    title_unicode: str

    track_id: Optional[int]

    user_id: int

    video: bool

    availability: Optional[:class:`BeatmapsetAvailability`]

    beatmaps: Optional[List[:class:`BeatmapCompact`]]
        Beatmaps contained in the beatmapset

    converts: Optional[List[:class:`Beatmap`]]

    current_nominations: Optional[List[:class:`CurrentNomination`]]

    current_user_attributes: Optional[:class:`BeatmapsetDiscussionPermissions`]

    description: Optional[str]

    description_bbcode: Optional[str]

    discussions: Optional[:class:`BeatmapsetDiscussion`]

    events: Optional[List[:class:`BeatmapsetEvent`]]

    genre: Optional[:class:`MetadataAttribute`]

    has_favourited: Optional[bool]

    language: Optional[:class:`MetadataAttribute`]

    nominations: Optional[Union[:class:`LegacyNominations`, :class:`Nominations`]]

    ratings: Optional[List[int]]

    recent_favourites: Optional[List[:class:`UserCompact`]]

    related_users: Optional[List[:class:`UserCompact`]]

    user: Optional[:class:`UserCompact`]
    """

    __slots__ = (
        "artist",
        "artist_unicode",
        "covers",
        "creator",
        "favourite_count",
        "hype",
        "id",
        "nsfw",
        "offset",
        "play_count",
        "preview_url",
        "source",
        "spotlight",
        "status",
        "title",
        "title_unicode",
        "track_id",
        "user_id",
        "video",
        "background_url",
        "availability",
        "beatmaps",
        "converts",
        "current_nominations",
        "current_user_attributes",
        "description",
        "description_bbcode",
        "discussions",
        "events",
        "genre",
        "has_favourited",
        "language",
        "nominations",
        "ratings",
        "recent_favourites",
        "related_users",
        "user",
    )

    def __init__(self, data):
        from .discussion import BeatmapsetDiscussion
        from .beatmapset_event import BeatmapsetEvent

        self.artist: str = get_required(data, "artist")
        self.artist_unicode: str = get_required(data, "artist_unicode")
        self.covers: Covers = Covers(get_required(data, "covers"))
        self.creator: str = get_required(data, "creator")
        self.favourite_count: int = get_required(data, "favourite_count")
        self.hype: Optional[BeatmapsetRequirement] = get_optional(data, "hype", BeatmapsetRequirement)
        self.id: int = get_required(data, "id")
        self.nsfw: bool = get_required(data, "nsfw")
        self.offset: int = get_required(data, "offset")
        self.play_count: int = get_required(data, "play_count")
        self.preview_url: str = get_required(data, "preview_url")
        self.source: str = get_required(data, "source")
        self.spotlight: bool = get_required(data, "spotlight")
        self.status: RankStatus = RankStatus[get_required(data, "status").upper()]
        self.title: str = get_required(data, "title")
        self.title_unicode: str = get_required(data, "title_unicode")
        self.track_id: Optional[int] = get_required(data, "track_id")
        self.user_id: int = get_required(data, "user_id")
        self.video: bool = get_required(data, "video")

        self.background_url: str = f"https://assets.ppy.sh/beatmaps/{self.id}/covers/raw.jpg"

        self.availability: BeatmapsetAvailability = get_optional(data, "availability", BeatmapsetAvailability)
        self.beatmaps: Optional[List[BeatmapCompact]] = get_optional_list(data, "beatmaps", BeatmapCompact)
        self.converts: Optional[List[Beatmap]] = get_optional_list(data, "converts", Beatmap)
        self.current_nominations: Optional[List[CurrentNomination]] = get_optional_list(
            data, "current_nominations", CurrentNomination
        )
        self.current_user_attributes: Optional[BeatmapsetPermissions] = get_optional(
            data, "current_user_attributes", BeatmapsetPermissions
        )
        self.description: Optional[str] = get_optional(data, "description", lambda value: value["description"])
        self.description_bbcode: Optional[str] = get_optional(data, "description", lambda value: value.get("bbcode"))
        self.discussions: Optional[List[BeatmapsetDiscussion]] = get_optional_list(
            data, "discussions", BeatmapsetDiscussion
        )
        self.events: Optional[List[BeatmapsetEvent]] = get_optional_list(data, "events", BeatmapsetEvent)
        self.genre: Optional[MetadataAttribute] = get_optional(data, "genre", MetadataAttribute)
        self.has_favourited: Optional[bool] = data.get("has_favourited")
        self.language: Optional[MetadataAttribute] = get_optional(data, "language", MetadataAttribute)
        self.nominations: Optional[_NOMINATIONS_TYPE] = get_optional(data, "nominations", get_beatmapset_nominations)
        self.ratings: Optional[List[int]] = data.get("ratings")
        self.recent_favourites: Optional[List[UserCompact]] = get_optional_list(data, "recent_favourites", UserCompact)
        self.related_users: Optional[List[UserCompact]] = get_optional_list(data, "related_users", UserCompact)
        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)

    def __repr__(self):
        return prettify(self, "artist", "title", "creator")


class Beatmapset(BeatmapsetCompact):
    """
    Represents a beatmapset. This extends :class:`BeatmapsetCompact` with additional attributes.
    Also overrides the type of `beatmaps` attribute.

    **Attributes**

    availability: :class:`BeatmapsetAvailability`

    beatmaps: Optional[List[:class:`Beatmap`]]
        null when this :class:`Beatmapset` object comes from a :class:`Beatmap` object

    bpm: float

    can_be_hyped: bool

    deleted_at: :py:class:`datetime.datetime`

    discussion_enabled: bool
        Deprecated. Is always true.

    discussion_locked: bool

    is_scoreable: bool

    last_updated: Optional[:py:class:`datetime.datetime`]

    legacy_thread_url: str

    nominations_summary: :class:`BeatmapsetRequirement`

    ranked: :class:`RankStatus`

    ranked_date: Optional[:py:class:`datetime.datetime`]

    storyboard: bool

    submitted_date: Optional[:py:class:`datetime.datetime`]

    tags: str
    """

    __slots__ = (
        "availability",
        "bpm",
        "can_be_hyped",
        "deleted_at",
        "discussion_enabled",
        "discussion_locked",
        "is_scoreable",
        "last_updated",
        "legacy_thread_url",
        "nominations_summary",
        "ranked",
        "ranked_date",
        "storyboard",
        "submitted_date",
        "tags",
    )

    def __init__(self, data):
        super().__init__(data)

        self.availability: BeatmapsetAvailability = BeatmapsetAvailability(get_required(data, "availability"))
        self.beatmaps: Optional[List[Beatmap]] = get_optional_list(data, "beatmaps", Beatmap)
        self.bpm: float = get_required(data, "bpm")
        self.can_be_hyped: bool = get_required(data, "can_be_hyped")
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", fromisoformat)
        self.discussion_enabled: bool = True  # Deprecated, all beatmapset discussions are enabled
        self.discussion_locked: bool = get_required(data, "discussion_locked")
        self.is_scoreable: bool = get_required(data, "is_scoreable")
        self.last_updated: Optional[datetime] = get_optional(data, "last_updated", fromisoformat)
        self.legacy_thread_url: Optional[str] = get_required(data, "legacy_thread_url")
        self.nominations_summary: BeatmapsetRequirement = BeatmapsetRequirement(
            get_required(data, "nominations_summary")
        )
        self.ranked: RankStatus = RankStatus(get_required(data, "ranked"))
        self.ranked_date: Optional[datetime] = get_optional(data, "ranked_date", fromisoformat)
        self.storyboard: bool = get_required(data, "storyboard")
        self.submitted_date: Optional[datetime] = get_optional(data, "submitted_date", fromisoformat)
        self.tags: str = get_required(data, "tags")


class BeatmapCompact:
    """
    Represents a beatmap.

    **Attributes**

    beatmapset_id: int

    difficulty_rating: float

    id: int

    mode: :class:`GameModeStr`

    status: :class:`RankStatus`

    total_length: int

    user_id: int

    version: str

    beatmapset: Optional[:class:`BeatmapsetCompact`]

    checksum: Optional[str]

    failtimes: Optional[:class:`Failtimes`]

    max_combo: Optional[int]

    owners: Optional[List[:class:`BeatmapOwner`]]
        List of owners (mappers) for the Beatmap.
    """

    __slots__ = (
        "beatmapset_id",
        "difficulty_rating",
        "id",
        "mode",
        "status",
        "total_length",
        "user_id",
        "version",
        "beatmapset",
        "checksum",
        "failtimes",
        "max_combo",
        "user",
        "owners",
    )

    def __init__(self, data):
        self.beatmapset_id: int = get_required(data, "beatmapset_id")
        self.difficulty_rating: float = get_required(data, "difficulty_rating")
        self.id: int = get_required(data, "id")
        self.mode: GameModeStr = GameModeStr(get_required(data, "mode"))
        self.status: RankStatus = RankStatus[get_required(data, "status").upper()]
        self.total_length: int = get_required(data, "total_length")
        self.user_id: int = get_required(data, "user_id")
        self.version: str = get_required(data, "version")

        self.beatmapset: Optional[BeatmapsetCompact] = get_optional(data, "beatmapset", BeatmapsetCompact)
        self.checksum: Optional[str] = data.get("checksum")
        self.failtimes: Optional[Failtimes] = get_optional(data, "failtimes", Failtimes)
        self.max_combo: Optional[int] = data.get("max_combo")
        self.owners: Optional[List[BeatmapOwner]] = get_optional_list(data, "owners", BeatmapOwner)

        # no longer used, but kept for backwards compatibility
        # TODO: remove in the next major version update
        self.user: Optional[UserCompact] = None

    def __repr__(self):
        return prettify(
            self,
            "beatmapset_id" if self.beatmapset is None else "beatmapset",
            "version",
        )


class Beatmap(BeatmapCompact):
    """
    Represent a beatmap. This extends :class:`BeatmapCompact` with additional attributes.
    Also overrides the type of `beatmapset`

    **Attributes**

    accuracy: float

    ar: float

    beatmapset: Optional[:class:`Beatmapset`]

    bpm: float

    convert: Optional[bool]

    count_circles: int

    count_sliders: int

    count_spinners: int

    cs: float

    deleted_at: Optional[:py:class:`datetime.datetime`]

    drain: float

    hit_length: int

    is_scoreable: bool

    last_updated: :py:class:`datetime.datetime`

    mode_int: :class:`GameModeInt`

    passcount: int

    playcount: int

    ranked: :class:`RankStatus`

    url: str
    """

    __slots__ = (
        "accuracy",
        "ar",
        "bpm",
        "convert",
        "count_circles",
        "count_sliders",
        "count_spinners",
        "cs",
        "deleted_at",
        "drain",
        "hit_length",
        "is_scoreable",
        "last_updated",
        "mode_int",
        "passcount",
        "playcount",
        "ranked",
        "url",
    )

    def __init__(self, data):
        super().__init__(data)

        self.accuracy: float = get_required(data, "accuracy")
        self.ar: float = get_required(data, "ar")
        self.beatmapset: Optional[Beatmapset] = get_optional(data, "beatmapset", Beatmapset)
        self.bpm: float = get_required(data, "bpm")
        self.convert: Optional[bool] = get_required(data, "convert")
        self.count_circles: int = get_required(data, "count_circles")
        self.count_sliders: int = get_required(data, "count_sliders")
        self.count_spinners: int = get_required(data, "count_spinners")
        self.cs: float = get_required(data, "cs")
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", fromisoformat)
        self.drain: float = get_required(data, "drain")
        self.hit_length: int = get_required(data, "hit_length")
        self.is_scoreable: bool = get_required(data, "is_scoreable")
        self.last_updated: datetime = fromisoformat(get_required(data, "last_updated"))
        self.mode_int: GameModeInt = GameModeInt(get_required(data, "mode_int"))
        self.passcount: int = get_required(data, "passcount")
        self.playcount: int = get_required(data, "playcount")
        self.ranked: RankStatus = RankStatus(get_required(data, "ranked"))
        self.url: str = get_required(data, "url")


class MetadataAttribute:
    """
    Genre of a beatmapset

    **Attributes**

    id: Optional[int]

    name: str
    """

    __slots__ = ("id", "name")

    def __init__(self, data):
        self.id: Optional[int] = get_required(data, "id")
        self.name: str = get_required(data, "name")


class OsuBeatmapDifficultyAttributes:
    """
    osu!standard beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    aim_difficulty: float

    approach_rate: float

    flashlight_difficulty: float

    overall_difficulty: float

    slider_factor: float

    speed_difficulty: float

    speed_note_count: float
    """

    __slots__ = (
        "aim_difficulty",
        "approach_rate",
        "flashlight_difficulty",
        "overall_difficulty",
        "slider_factor",
        "speed_difficulty",
        "speed_note_count",
    )

    def __init__(self, data):
        self.aim_difficulty: float = get_required(data, "aim_difficulty")
        self.approach_rate: float = get_required(data, "approach_rate")
        self.flashlight_difficulty: float = get_required(data, "flashlight_difficulty")
        self.overall_difficulty: float = get_required(data, "overall_difficulty")
        self.slider_factor: float = get_required(data, "slider_factor")
        self.speed_difficulty: float = get_required(data, "speed_difficulty")
        self.speed_note_count: float = get_required(data, "speed_note_count")

    def __repr__(self):
        return prettify(self, "aim_difficulty", "speed_difficulty")


class TaikoBeatmapDifficultyAttributes:
    """
    osu!taiko beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    stamina_difficulty: float

    rhythm_difficulty: float

    colour_difficulty: float

    great_hit_window: float

    peak_difficulty: float
    """

    __slots__ = (
        "stamina_difficulty",
        "rhythm_difficulty",
        "colour_difficulty",
        "great_hit_window",
        "peak_difficulty",
    )

    def __init__(self, data):
        self.stamina_difficulty: float = get_required(data, "stamina_difficulty")
        self.rhythm_difficulty: float = get_required(data, "rhythm_difficulty")
        self.colour_difficulty: float = get_required(data, "colour_difficulty")
        self.great_hit_window: float = get_required(data, "great_hit_window")
        self.peak_difficulty: float = get_required(data, "peak_difficulty")

    def __repr__(self):
        return prettify(self, "stamina_difficulty")


class FruitsBeatmapDifficultyAttributes:
    """
    osu!catch beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    approach_rate: float
    """

    __slots__ = "approach_rate"

    def __init__(self, data):
        self.approach_rate: float = get_required(data, "approach_rate")

    def __repr__(self):
        return prettify(self, "approach_rate")


class ManiaBeatmapDifficultyAttributes:
    """
    osu!mania beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    great_hit_window: float

    score_multiplier: float
    """

    __slots__ = ("great_hit_window", "score_multiplier")

    def __init__(self, data):
        self.great_hit_window: float = get_required(data, "great_hit_window")
        self.score_multiplier: float = get_required(data, "score_multiplier")

    def __repr__(self):
        return prettify(self, "great_hit_window")


class BeatmapDifficultyAttributes:
    """
    Represent beatmap difficulty attributes. Following fields are always present and
    then there are additional fields for different rulesets.

    **Attributes**

    max_combo: int

    star_rating: float

    mode_attributes: Optional[Union[:class:`OsuBeatmapDifficultyAttributes`, :class:`TaikoBeatmapDifficultyAttributes`,
    :class:`FruitsBeatmapDifficultyAttributes`, :class:`ManiaBeatmapDifficultyAttributes`]]

        Can be none for some beatmaps that are bugged and have no difficulty attributes.

    type: Optional[:class:`GameModeStr`]
    """

    __slots__ = ("max_combo", "star_rating", "type", "mode_attributes")
    if TYPE_CHECKING:
        type: Optional[GameModeStr]
        mode_attributes: Optional[
            Union[
                OsuBeatmapDifficultyAttributes,
                TaikoBeatmapDifficultyAttributes,
                ManiaBeatmapDifficultyAttributes,
                FruitsBeatmapDifficultyAttributes,
            ]
        ]

    def __init__(self, data):
        data = get_required(data, "attributes")
        self.max_combo: int = get_required(data, "max_combo")
        self.star_rating: float = get_required(data, "star_rating")
        if "aim_difficulty" in data:
            self.type = GameModeStr.STANDARD
            self.mode_attributes = OsuBeatmapDifficultyAttributes(data)
        elif "stamina_difficulty" in data:
            self.type = GameModeStr.TAIKO
            self.mode_attributes = TaikoBeatmapDifficultyAttributes(data)
        elif "great_hit_window" in data:
            self.type = GameModeStr.MANIA
            self.mode_attributes = ManiaBeatmapDifficultyAttributes(data)
        elif "approach_rate" in data:
            self.type = GameModeStr.CATCH
            self.mode_attributes = FruitsBeatmapDifficultyAttributes(data)
        else:
            self.type = None
            self.mode_attributes = None

    def __getattr__(self, item):
        return getattr(self.mode_attributes, item)

    def __repr__(self):
        return prettify(self, "star_rating", "type", "mode_attributes")


class Failtimes:
    """
    **Attributes**

    exit: Optional[List[int]]
        List of 100 integers.

    fail: Optional[List[int]]
        List of 100 integers.
    """

    __slots__ = ("exit", "fail")

    def __init__(self, data):
        self.exit: Optional[List[int]] = data.get("exit")
        self.fail: Optional[List[int]] = data.get("fail")

    def __repr__(self):
        return prettify(self, "exit" if self.exit is not None else "fail")


class Covers:
    """
    **Attributes**

    cover: str

    cover_2x: str

    card: str

    card_2x: str

    list: str

    list_2x: str

    slimcover: str

    slimcover_2x: str
    """

    __slots__ = (
        "cover",
        "cover_2x",
        "card",
        "card_2x",
        "list",
        "list_2x",
        "slimcover",
        "slimcover_2x",
    )

    def __init__(self, data):
        self.cover: str = get_required(data, "cover")
        self.cover_2x: str = data["cover@2x"]
        self.card: str = get_required(data, "card")
        self.card_2x: str = data["card@2x"]
        self.list: str = get_required(data, "list")
        self.list_2x: str = data["list@2x"]
        self.slimcover: str = get_required(data, "slimcover")
        self.slimcover_2x: str = data["slimcover@2x"]

    def __repr__(self):
        return prettify(self, "cover")


class BeatmapPlaycount:
    """
    Represent the playcount of a beatmap.

    **Attributes**

    beatmap_id: int

    beatmap: Optional[:class:`BeatmapCompact`]

    beatmapset: Optional[:class:`BeatmapsetCompact`]

    count: int
    """

    __slots__ = ("beatmap_id", "beatmap", "beatmapset", "count")

    def __init__(self, data):
        self.beatmap_id: int = get_required(data, "beatmap_id")
        self.beatmap: Optional[BeatmapCompact] = get_optional(data, "beatmap", BeatmapCompact)
        self.beatmapset: Optional[BeatmapsetCompact] = get_optional(data, "beatmapset", BeatmapsetCompact)
        self.count: int = get_required(data, "count")

    def __repr__(self):
        return prettify(self, "beatmap_id", "count")


class BeatmapsetRequirement:
    """
    Gives information on requirements for a beatmap

    **Attributes**

    current: int

    required: Optional[int]
        If this is None, then required_meta and eligible_main_rulesets should have values

    required_meta: Optional[:class:`BeatmapsetRequiredNominations`]

    eligible_main_rulesets: Optional[List[:class:`GameModeStr`]]
    """

    __slots__ = ("current", "required", "eligible_main_rulesets", "required_meta")

    def __init__(self, data):
        self.current: int = get_required(data, "current")
        self.required: Optional[int] = data.get("required")

        self.eligible_main_rulesets: Optional[List[GameModeStr]] = get_optional_list(
            data, "eligible_main_rulesets", GameModeStr
        )
        self.required_meta: Optional[BeatmapsetRequiredNominations] = get_optional(
            data, "required_meta", BeatmapsetRequiredNominations
        )

    def __repr__(self):
        return prettify(self, "current", "required")


class BeatmapsetRequiredNominations:
    """
    Information of required ruleset nominations of a beatmap

    **Attributes**

    main_ruleset: int

    non_main_ruleset: int
    """

    ___slots__ = ("main_ruleset", "non_main_ruleset")

    def __init__(self, data):
        self.main_ruleset = get_required(data, "main_ruleset")
        self.non_main_ruleset = get_required(data, "non_main_ruleset")


class BeatmapsetAvailability:
    """
    Gives information on the availability of a beatmap for download.

    **Attributes**

    download_disabled: bool

    more_information: Optional[str]
    """

    __slots__ = ("download_disabled", "more_information")

    def __init__(self, data):
        self.download_disabled: bool = get_required(data, "download_disabled")
        self.more_information: Optional[str] = data.get("more_information")

    def __repr__(self):
        return prettify(self, "download_disabled", "more_information")


class BaseNominations:
    """
    Base attributes for :class:`LegacyNominations` and :class:`Nominations`

    **Attributes**

    disqualification: Optional[:class:`BeatmapsetEvent`]

    nominated: Optional[bool]

    nomination_reset: Optional[:class:`BeatmapsetEvent`]

    ranking_eta: Optional[str]

    ranking_queue_position: Optional[int]

    required_hype: int
    """

    __slots__ = (
        "disqualification",
        "nominated",
        "nomination_reset",
        "ranking_eta",
        "ranking_queue_position",
        "required_hype",
    )

    def __init__(self, data):
        from .beatmapset_event import BeatmapsetEvent

        self.disqualification: Optional[BeatmapsetEvent] = get_optional(data, "disqualification", BeatmapsetEvent)
        self.nominated: Optional[bool] = data.get("nominated")
        self.nomination_reset: Optional[BeatmapsetEvent] = get_optional(data, "nomination_reset", BeatmapsetEvent)
        self.ranking_eta: Optional[str] = data.get("ranking_eta")
        self.ranking_queue_position: Optional[int] = data.get("ranking_queue_position")
        self.required_hype: int = get_required(data, "required_hype")

    def __repr__(self):
        return prettify(self, "nominated")


class LegacyNominations(BaseNominations):
    """
    Shows info about nominations on a beatmapset, extending :class:`BaseNominations`

    **Attributes**

    is_legacy: bool
        True

    current: int

    required: int
    """

    __slots__ = ("current", "required")
    is_legacy = True

    def __init__(self, data):
        super().__init__(data)
        self.current: int = get_required(data, "current")
        self.required: int = get_required(data, "required")

    def __repr__(self):
        return prettify("current", "required")


class Nominations(BaseNominations):
    """
    Shows info about nominations on a beatmapset, extending :class:`BaseNominations`

    **Attributes**

    is_legacy: bool
        False

    current: Union[int, Dict[:class:`GameModeStr`, int]]

    required: int
    """

    __slots__ = ("current", "required")
    is_legacy = False

    def __init__(self, data):
        super().__init__(data)
        self.current: Dict[GameModeStr, int] = dict(
            zip(map(GameModeStr, (current := get_required(data, "current")).keys()), current.values())
        )
        self.required: Dict[GameModeStr, int] = dict(
            zip(
                map(GameModeStr, (required := get_required(data, "required")).keys()),
                required.values(),
            )
        )

    def __repr__(self):
        return prettify(self, "current", "required")


class CurrentNomination:
    """
    Info about a nomination

    **Attributes**

    beatmapset_id: int

    rulesets: Optional[List[:class:`GameModeStr`]]

    reset: bool

    user_id: int
    """

    def __init__(self, data):
        self.beatmapset_id: int = get_required(data, "beatmapset_id")
        self.rulesets: Optional[List[GameModeStr]] = get_optional_list(data, "rulesets", GameModeStr)
        self.reset: bool = get_required(data, "reset")
        self.user_id: int = get_required(data, "user_id")

    def __repr__(self):
        return prettify(self, "beatmapset_id", "user_id")


_NOMINATIONS_TYPE = Union[LegacyNominations, Nominations]


def get_beatmapset_nominations(data) -> _NOMINATIONS_TYPE:
    if data.get("legacy_mode", False):
        return LegacyNominations(data)
    return Nominations(data)


class BeatmapOwner:
    """
    Describes the owner of a beatmap

    **Attributes**

    id: int
        User id of the Beatmap owner.

    username: str
        Username of the Beatmap owner.
    """

    __slots__ = ("id", "username")

    def __init__(self, data):
        self.id: int = get_required(data, "id")
        self.username: str = get_required(data, "username")

    def __repr__(self):
        return prettify(self, "id", "username")
