from dateutil import parser
from typing import Dict, Optional, List, Union, TYPE_CHECKING

from ..enums import RankStatus, GameModeStr, GameModeInt
from ..util import prettify, get_optional, get_optional_list
from .user import UserCompact
from .current_user_attributes import BeatmapsetPermissions


if TYPE_CHECKING:
    from datetime import datetime


class BeatmapsetCompact:
    """
    Represents a beatmapset.

    **Attributes**

    artist: :class:`str`

    artist_unicode: :class:`str`

    background_url: :class:`str`
        Not given by api but created locally based on beatmapset id.

    covers: :class:`Covers`

    creator: :class:`str`

    favourite_count: :class:`int`

    hype: Optional[:class:`BeatmapsetRequirement`]

    id: :class:`int`

    nsfw: :class:`bool`

    offset: :class:`int`

    play_count: :class:`int`

    preview_url: :class:`str`

    source: :class:`str`

    spotlight: :class:`bool`

    status: :class:`RankStatus`

    title: :class:`str`

    title_unicode: :class:`str`

    track_id: Optional[:class:`int`]

    user_id: :class:`int`

    video: :class:`bool`

    availability: Optional[:class:`BeatmapsetAvailability`]

    beatmaps: Optional[List[:class:`BeatmapCompact`]]
        Beatmaps contained in the beatmapset

    converts: Optional[List[:class:`Beatmap`]]

    current_nominations: Optional[List[:class:`CurrentNomination`]]

    current_user_attributes: Optional[:class:`BeatmapsetDiscussionPermissions`]

    description: Optional[:class:`str`]

    description_bbcode: Optional[:class:`str`]

    discussions: Optional[:class:`BeatmapsetDiscussion`]

    events: Optional[List[:class:`BeatmapsetEvent`]]

    genre: Optional[:class:`MetadataAttribute`]

    has_favourited: Optional[:class:`bool`]

    language: Optional[:class:`MetadataAttribute`]

    nominations: Optional[Union[:class:`LegacyNominations`, :class:`Nominations`]]

    ratings: Optional[List[:class:`int`]]

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

        self.artist: str = data["artist"]
        self.artist_unicode: str = data["artist_unicode"]
        self.covers: Covers = Covers(data["covers"])
        self.creator: str = data["creator"]
        self.favourite_count: int = data["favourite_count"]
        self.hype: Optional[BeatmapsetRequirement] = get_optional(data, "hype", BeatmapsetRequirement)
        self.id: int = data["id"]
        self.nsfw: bool = data["nsfw"]
        self.offset: int = data["offset"]
        self.play_count: int = data["play_count"]
        self.preview_url: str = data["preview_url"]
        self.source: str = data["source"]
        self.spotlight: bool = data["spotlight"]
        self.status: RankStatus = RankStatus[data["status"].upper()]
        self.title: str = data["title"]
        self.title_unicode: str = data["title_unicode"]
        self.track_id: Optional[int] = data["track_id"]
        self.user_id: int = data["user_id"]
        self.video: bool = data["video"]

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

    bpm: :class:`float`

    can_be_hyped: :class:`bool`

    deleted_at: :class:`datetime.datetime`

    discussion_enabled: :class:`bool`
        Deprecated. Is always true.

    discussion_locked: :class:`bool`

    is_scoreable: :class:`bool`

    last_updated: Optional[:class:`datetime.datetime`]

    legacy_thread_url: :class:`str`

    nominations_summary: :class:`NominationsSummary`

    ranked: :class:`RankStatus`

    ranked_date: Optional[:class:`datetime.datetime`]

    storyboard: :class:`bool`

    submitted_date: Optional[:class:`datetime.datetime`]

    tags: :class:`str`
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

        self.availability: BeatmapsetAvailability = BeatmapsetAvailability(data["availability"])
        self.beatmaps: Optional[List[Beatmap]] = get_optional_list(data, "beatmaps", Beatmap)
        self.bpm: float = data["bpm"]
        self.can_be_hyped: bool = data["can_be_hyped"]
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", parser.parse)
        self.discussion_enabled: bool = True  # Deprecated, all beatmapset discussions are enabled
        self.discussion_locked: bool = data["discussion_locked"]
        self.is_scoreable: bool = data["is_scoreable"]
        self.last_updated: Optional[datetime] = get_optional(data, "last_updated", parser.parse)
        self.legacy_thread_url: Optional[str] = data["legacy_thread_url"]
        self.nominations_summary: BeatmapsetRequirement = BeatmapsetRequirement(data["nominations_summary"])
        self.ranked: RankStatus = RankStatus(data["ranked"])
        self.ranked_date: Optional[datetime] = get_optional(data, "ranked_date", parser.parse)
        self.storyboard: bool = data["storyboard"]
        self.submitted_date: Optional[datetime] = get_optional(data, "submitted_date", parser.parse)
        self.tags: str = data["tags"]


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

    beatmapset: Optional[:class:`BeatmapsetCompact`]

    checksum: Optional[:class:`str`]

    failtimes: Optional[:class:`Failtimes`]

    max_combo: Optional[:class:`int`]

    user: Optional[:class:`UserCompact`]
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
    )

    def __init__(self, data):
        self.beatmapset_id: int = data["beatmapset_id"]
        self.difficulty_rating: float = data["difficulty_rating"]
        self.id: int = data["id"]
        self.mode: GameModeStr = GameModeStr(data["mode"])
        self.status: RankStatus = RankStatus[data["status"].upper()]
        self.total_length: int = data["total_length"]
        self.user_id: int = data["user_id"]
        self.version: str = data["version"]

        self.beatmapset: Optional[BeatmapsetCompact] = get_optional(data, "beatmapset", BeatmapsetCompact)
        self.checksum: Optional[str] = data.get("checksum")
        self.failtimes: Optional[Failtimes] = get_optional(data, "failtimes", Failtimes)
        self.max_combo: Optional[int] = data.get("max_combo")
        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)

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

    accuracy: :class:`float`

    ar: :class:`float`

    beatmapset: Optional[:class:`Beatmapset`]

    bpm: :class:`float`

    convert: Optional[:class:`bool`]

    count_circles: :class:`int`

    count_sliders: :class:`int`

    count_spinners: :class:`int`

    cs: :class:`float`

    deleted_at: Optional[:class:`datetime.datetime`]

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

        self.accuracy: float = data["accuracy"]
        self.ar: float = data["ar"]
        self.beatmapset: Optional[Beatmapset] = get_optional(data, "beatmapset", Beatmapset)
        self.bpm: float = data["bpm"]
        self.convert: Optional[bool] = data["convert"]
        self.count_circles: int = data["count_circles"]
        self.count_sliders: int = data["count_sliders"]
        self.count_spinners: int = data["count_spinners"]
        self.cs: float = data["cs"]
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", parser.parse)
        self.drain: float = data["drain"]
        self.hit_length: int = data["hit_length"]
        self.is_scoreable: bool = data["is_scoreable"]
        self.last_updated: datetime = parser.parse(data["last_updated"])
        self.mode_int: GameModeInt = GameModeInt(data["mode_int"])
        self.passcount: int = data["passcount"]
        self.playcount: int = data["playcount"]
        self.ranked: RankStatus = RankStatus(data["ranked"])
        self.url: str = data["url"]


class MetadataAttribute:
    """
    Genre of a beatmapset

    **Attributes**

    id: Optional[:class:`int`]

    name: :class:`str`
    """

    __slots__ = ("id", "name")

    def __init__(self, data):
        self.id: Optional[int] = data["id"]
        self.name: str = data["name"]


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

    speed_note_count: :class:`float`
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
        self.aim_difficulty: float = data["aim_difficulty"]
        self.approach_rate: float = data["approach_rate"]
        self.flashlight_difficulty: float = data["flashlight_difficulty"]
        self.overall_difficulty: float = data["overall_difficulty"]
        self.slider_factor: float = data["slider_factor"]
        self.speed_difficulty: float = data["speed_difficulty"]
        self.speed_note_count: float = data["speed_note_count"]

    def __repr__(self):
        return prettify(self, "aim_difficulty", "speed_difficulty")


class TaikoBeatmapDifficultyAttributes:
    """
    osu!taiko beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    stamina_difficulty: :class:`float`

    rhythm_difficulty: :class:`float`

    colour_difficulty: :class:`float`

    great_hit_window: :class:`float`

    peak_difficulty: :class:`float`
    """

    __slots__ = (
        "stamina_difficulty",
        "rhythm_difficulty",
        "colour_difficulty",
        "great_hit_window",
        "peak_difficulty",
    )

    def __init__(self, data):
        self.stamina_difficulty: float = data["stamina_difficulty"]
        self.rhythm_difficulty: float = data["rhythm_difficulty"]
        self.colour_difficulty: float = data["colour_difficulty"]
        self.great_hit_window: float = data["great_hit_window"]
        self.peak_difficulty: float = data["peak_difficulty"]

    def __repr__(self):
        return prettify(self, "stamina_difficulty")


class FruitsBeatmapDifficultyAttributes:
    """
    osu!catch beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    approach_rate: :class:`float`
    """

    __slots__ = "approach_rate"

    def __init__(self, data):
        self.approach_rate: float = data["approach_rate"]

    def __repr__(self):
        return prettify(self, "approach_rate")


class ManiaBeatmapDifficultyAttributes:
    """
    osu!mania beatmap difficulty attributes.
    See :class:`BeatmapDifficultyAttributes` for more information.

    **Attributes**

    great_hit_window: :class:`float`

    score_multiplier: :class:`float`
    """

    __slots__ = ("great_hit_window", "score_multiplier")

    def __init__(self, data):
        self.great_hit_window: float = data["great_hit_window"]
        self.score_multiplier: float = data["score_multiplier"]

    def __repr__(self):
        return prettify(self, "great_hit_window")


class BeatmapDifficultyAttributes:
    """
    Represent beatmap difficulty attributes. Following fields are always present and
    then there are additional fields for different rulesets.

    **Attributes**

    The parameters depend on the ruleset, but the following two attributes are present in all rulesets.

    max_combo: :class:`int`

    star_rating: :class:`float`

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
        data = data["attributes"]
        self.max_combo: int = data["max_combo"]
        self.star_rating: float = data["star_rating"]
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

    exit: Optional[List[:class:`int`]]
        List of 100 integers.

    fail: Optional[List[:class:`int`]]
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
        self.cover: str = data["cover"]
        self.cover_2x: str = data["cover@2x"]
        self.card: str = data["card"]
        self.card_2x: str = data["card@2x"]
        self.list: str = data["list"]
        self.list_2x: str = data["list@2x"]
        self.slimcover: str = data["slimcover"]
        self.slimcover_2x: str = data["slimcover@2x"]

    def __repr__(self):
        return prettify(self, "cover")


class BeatmapPlaycount:
    """
    Represent the playcount of a beatmap.

    **Attributes**

    beatmap_id: :class:`int`

    beatmap: Optional[:class:`BeatmapCompact`]

    beatmapset: Optional[:class:`BeatmapsetCompact`]

    count: :class:`int`
    """

    __slots__ = ("beatmap_id", "beatmap", "beatmapset", "count")

    def __init__(self, data):
        self.beatmap_id: int = data["beatmap_id"]
        self.beatmap: Optional[BeatmapCompact] = get_optional(data, "beatmap", BeatmapCompact)
        self.beatmapset: Optional[BeatmapsetCompact] = get_optional(data, "beatmapset", BeatmapsetCompact)
        self.count: int = data["count"]

    def __repr__(self):
        return prettify(self, "beatmap_id", "count")


class BeatmapsetRequirement:
    """
    Gives information on requirements for a beatmap

    **Attributes**

    current: :class:`int`

    required: :class:`int`
    """

    __slots__ = ("current", "required")

    def __init__(self, data):
        self.current: int = data["current"]
        self.required: int = data["required"]

    def __repr__(self):
        return prettify(self, "current", "required")


class BeatmapsetAvailability:
    """
    Gives information on the availability of a beatmap for download.

    **Attributes**

    download_disabled: :class:`bool`

    more_information: Optional[:class:`str`]
    """

    __slots__ = ("download_disabled", "more_information")

    def __init__(self, data):
        self.download_disabled: bool = data["download_disabled"]
        self.more_information: Optional[str] = data.get("more_information")

    def __repr__(self):
        return prettify(self, "download_disabled", "more_information")


class BaseNominations:
    """
    Base attributes for :class:`LegacyNominations` and :class:`Nominations`

    **Attributes**

    disqualification: Optional[:class:`BeatmapsetEvent`]

    nominated: Optional[:class:`bool`]

    nomination_reset: Optional[:class:`BeatmapsetEvent`]

    ranking_eta: Optional[:class:`str`]

    ranking_queue_position: Optional[:class:`int`]

    required_hype: :class:`int`
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
        self.required_hype: int = data["required_hype"]

    def __repr__(self):
        return prettify(self, "nominated")


class LegacyNominations(BaseNominations):
    """
    Shows info about nominations on a beatmapset, extending :class:`BaseNominations`

    **Attributes**

    is_legacy: :class:`bool`
        True

    current: :class:`int`

    required: :class:`int`
    """

    __slots__ = ("current", "required")
    is_legacy = True

    def __init__(self, data):
        super().__init__(data)
        self.current: int = data["current"]
        self.required: int = data["required"]

    def __repr__(self):
        return prettify("current", "required")


class Nominations(BaseNominations):
    """
    Shows info about nominations on a beatmapset, extending :class:`BaseNominations`

    **Attributes**

    is_legacy: :class:`bool`
        False

    current: Union[:class:`int`, Dict[:class:`GameModeStr`, :class:`int`]]

    required: :class:`int`
    """

    __slots__ = ("current", "required")
    is_legacy = False

    def __init__(self, data):
        super().__init__(data)
        self.current: Dict[GameModeStr, int] = dict(
            zip(map(GameModeStr, (current := data["current"]).keys()), current.values())
        )
        self.required: Dict[GameModeStr, int] = dict(
            zip(
                map(GameModeStr, (required := data["required"]).keys()),
                required.values(),
            )
        )

    def __repr__(self):
        return prettify(self, "current", "required")


class CurrentNomination:
    """
    Info about a nomination

    **Attributes**

    beatmapset_id: :class:`int`

    rulesets: Optional[List[:class:`GameModeStr`]]

    reset: :class:`bool`

    user_id: :class:`int`
    """

    def __init__(self, data):
        self.beatmapset_id: int = data["beatmapset_id"]
        self.rulesets: Optional[List[GameModeStr]] = get_optional_list(data, "rulesets", GameModeStr)
        self.reset: bool = data["reset"]
        self.user_id: int = data["user_id"]

    def __repr__(self):
        return prettify(self, "beatmapset_id", "user_id")


_NOMINATIONS_TYPE = Union[LegacyNominations, Nominations]


def get_beatmapset_nominations(data) -> _NOMINATIONS_TYPE:
    if data.get("legacy_mode", False):
        return LegacyNominations(data)
    return Nominations(data)
