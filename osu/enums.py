from enum import IntFlag, IntEnum, Enum, EnumMeta
from typing import Sequence, Union

from .constants import incompatible_mods


__all__ = (
    "Mod",
    "Mods",
    "RankStatus",
    "GameModeStr",
    "GameModeInt",
    "WikiSearchMode",
    "UserBeatmapType",
    "RankingType",
    "CommentSort",
    "MultiplayerScoresSort",
    "BeatmapsetEventType",
    "BeatmapsetEventSort",
    "MatchSort",
    "MatchEventType",
    "RoomSort",
    "RoomType",
    "RoomCategory",
    "RoomFilterMode",
    "RoomStatus",
    "RealTimeQueueMode",
    "PlaylistQueueMode",
    "BeatmapsetGenre",
    "BeatmapsetLanguage",
    "BeatmapsetSearchGeneral",
    "BeatmapsetSearchStatus",
    "BeatmapsetSearchExtra",
    "BeatmapsetSearchPlayed",
    "BeatmapsetSearchSort",
    "ScoreRank",
    "ObjectType",
    "UserScoreType",
    "ForumTopicType",
    "ChatChannelType",
    "NotificationType",
    "NotificationCategory",
    "UserAccountHistoryType",
    "MessageType",
    "KudosuAction",
    "ScoringType",
    "TeamType",
    "UserRelationType",
    "ChatMessageType",
)


class PartialEnum:
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PartialEnum({repr(self.value)})"


class FallbackEnum(EnumMeta):
    def __new__(cls, name, bases, attrs):
        enum = EnumMeta.__new__(cls, name, bases, attrs)

        old__new__ = getattr(enum, "enum__new__", Enum.__new__)

        def fallback__new__(cls, value, *args, **kwargs):
            try:
                return old__new__(cls, value, *args, **kwargs)
            except ValueError:
                return PartialEnum(value)

        enum.__new__ = fallback__new__

        return enum


class Mod(Enum, metaclass=FallbackEnum):
    """
    Enum of all mods, score submittable or not.

    **Mods**

    Easy = 'EZ'

    NoFail = 'NF'

    HalfTime = 'HT'

    Daycore = 'DC'

    HardRock = 'HR'

    SuddenDeath = 'SD'

    Perfect = 'PF'

    DoubleTime = 'DT'

    Nightcore = 'NC'

    Hidden = 'HD'

    Flashlight = 'FL'

    Blinds = 'BL'

    StrictTracking = 'ST'

    Target = 'TP'

    DifficultyAdjust = 'DA'

    Classic = 'CL'

    Random = 'RD'

    Mirror = 'MR'

    Alternate = 'AL'

    SingleTap = 'SG'

    Autoplay = 'AT'

    Cinema = 'CN'

    Relax = 'RX'

    Autopilot = 'AP'

    SpunOut = 'SO'

    Transform = 'TR'

    Wiggle = 'WG'

    SpinIn = 'SI'

    Grow = 'GR'

    Deflate = 'DF'

    WindUp = 'WU'

    WindDown = 'WD'

    Traceable = 'TC'

    BarrelRoll = 'BR'

    ApproachDifferent = 'AD'

    Muted = 'MU'

    NoScope = 'NS'

    Magnetised = 'MG'

    Repel = 'RP'

    AdaptiveSpeed = 'AS'

    FreezeFrame = 'FR'

    TouchDevice = 'TD'

    Swap = 'SW'

    FloatingFruits = 'FF'

    FadeIn = 'FI'

    FourKeys = '4K'

    FiveKeys = '5K'

    SixKeys = '6K'

    SevenKeys = '7K'

    EightKeys = '8K'

    NineKeys = '9K'

    TenKeys = '10K'

    OneKey = '1K'

    TwoKeys = '2K'

    ThreeKeys = '3K'

    DualStages = 'DS'

    Invert = 'IN'

    ConstantSpeed = 'CS'

    HoldOff = 'HO'

    AccuracyChallenge = 'AC'
    """

    Easy = "EZ"
    NoFail = "NF"
    HalfTime = "HT"
    Daycore = "DC"
    HardRock = "HR"
    SuddenDeath = "SD"
    Perfect = "PF"
    DoubleTime = "DT"
    Nightcore = "NC"
    Hidden = "HD"
    Flashlight = "FL"
    Blinds = "BL"
    StrictTracking = "ST"
    Target = "TP"
    DifficultyAdjust = "DA"
    Classic = "CL"
    Random = "RD"
    Mirror = "MR"
    Alternate = "AL"
    SingleTap = "SG"
    Autoplay = "AT"
    Cinema = "CN"
    Relax = "RX"
    Autopilot = "AP"
    SpunOut = "SO"
    Transform = "TR"
    Wiggle = "WG"
    SpinIn = "SI"
    Grow = "GR"
    Deflate = "DF"
    WindUp = "WU"
    WindDown = "WD"
    Traceable = "TC"
    BarrelRoll = "BR"
    ApproachDifferent = "AD"
    Muted = "MU"
    NoScope = "NS"
    Magnetised = "MG"
    Repel = "RP"
    AdaptiveSpeed = "AS"
    FreezeFrame = "FR"
    TouchDevice = "TD"
    Swap = "SW"
    FloatingFruits = "FF"
    FadeIn = "FI"
    FourKeys = "4K"
    FiveKeys = "5K"
    SixKeys = "6K"
    SevenKeys = "7K"
    EightKeys = "8K"
    NineKeys = "9K"
    TenKeys = "10K"
    OneKey = "1K"
    TwoKeys = "2K"
    ThreeKeys = "3K"
    DualStages = "DS"
    Invert = "IN"
    ConstantSpeed = "CS"
    HoldOff = "HO"
    AccuracyChallenge = "AC"
    Bloom = "BM"
    NoRelease = "NR"
    Depth = "DP"
    Cover = "CO"


class Mods(IntFlag):
    """
    IntFlag enum for all score submittable mods. Info gathered from
    https://github.com/ppy/osu-web/blob/973315aded8a5762fc00a9f245337802c27bd213/app/Libraries/Mods.php
    and https://github.com/ppy/osu-web/blob/973315aded8a5762fc00a9f245337802c27bd213/database/mods.json

    **List of mods, their acronyms, and their bitwise representation**

    NoFail (NF) = 1 << 0

    Easy (EZ) = 1 << 1

    TouchDevice (TD) = 1 << 2  # Replaces unused NoVideo mod

    Hidden (HD) = 1 << 3

    HardRock (HR) = 1 << 4

    SuddenDeath (SD) = 1 << 5

    DoubleTime (DT) = 1 << 6

    Relax (RX) = 1 << 7

    HalfTime (HT) = 1 << 8

    Nightcore (NC) = (1 << 9)

    Flashlight (FL) = 1 << 10

    SpunOut (SO) = 1 << 12

    AutoPilot (AP) = 1 << 13

    Perfect (PF) = 1 << 14

    FadeIn (FI) = 1 << 20

    Mirror (MR) = 1 << 30

    Key4 (4K) = 1 << 15

    Key5 (5K) = 1 << 16

    Key6 (6K) = 1 << 17

    Key7 (7K) = 1 << 18

    Key8 (8K) = 1 << 19

    Key9 (9K) = 1 << 24
    """

    NoFail = 1 << 0
    Easy = 1 << 1
    TouchDevice = 1 << 2
    Hidden = 1 << 3
    HardRock = 1 << 4
    SuddenDeath = 1 << 5
    DoubleTime = 1 << 6
    Relax = 1 << 7
    HalfTime = 1 << 8
    Nightcore = 1 << 9
    Flashlight = 1 << 10
    SpunOut = 1 << 12
    AutoPilot = 1 << 13
    Perfect = 1 << 14
    FadeIn = 1 << 20
    Mirror = 1 << 30

    FourKeys = 1 << 15
    FiveKeys = 1 << 16
    SixKeys = 1 << 17
    SevenKeys = 1 << 18
    EightKeys = 1 << 19
    NineKeys = 1 << 24

    @classmethod
    def get_from_abbreviation(cls, abbreviation: str) -> "Mods":
        """
        Get mod from its abbreviation. Abbreviations are taken from https://osu.ppy.sh/wiki/en/Game_modifier/Summary

        **Parameters**

        abbreviation: str
            Abbreviation of the mod (must be capitalized)

        **Returns**

        :class:`Mods`
        """
        return cls[Mod(abbreviation.upper()).name]

    @staticmethod
    def get_from_list(mods: Sequence["Mods"]) -> Union["Mods", None]:
        """
        Get a :class:`Mods` object from a list of :class:`Mods`.

        **Parameters**

        mods: Sequence[:class:`Mods`]
            Sequence of mods of type Mods

        **Returns**

        Union[:class:`Mods`, :class:`NoneType`]
        """
        if len(mods) == 0:
            return
        a = mods[0]
        for i in range(1, len(mods)):
            a |= mods[i]
        return a

    @staticmethod
    def parse_any_list(mods: Sequence[Union[str, int, "Mods"]]) -> "Mods":
        """
        Take a list and return a parsed list. Parsing the list involves
        converting any object recognizable as a mod to a :class:`Mods` object.
        This includes mod names/abbreviations as strings and also their bitset values.

        **Parameters**

        mods: Sequence[Union[:class:`Mods`, str, int]]
            Sequence of :class:`Mods`, str, and/or int objects
            to be parsed and returned as a :class:`Mods` object.

        **Returns**

        Union[:class:`Mods`, :class:`NoneType`]
        """
        ret = []
        for mod in mods:
            if isinstance(mod, Mods):
                ret.append(mod)
            elif isinstance(mod, str):
                if mod in Mods.__members__:
                    ret.append(Mods[mod])
                else:
                    try:
                        ret.append(Mods.get_from_abbreviation(mod.upper()))
                    except ValueError:
                        raise ValueError(
                            "Mods represented as strings must be either the full name or "
                            "abbreviation. '{mod}' does not fall under either of those."
                        )
            elif isinstance(mod, int):
                ret.append(Mods(mod))
            else:
                raise TypeError("Mods can only be parsed to Mods objects if they're of type str, int, or Mods")
        return Mods.get_from_list(ret) if len(ret) > 0 else None

    def get_incompatible_mods(self):
        """
        Get a list of mods that are incompatible with this mod.

        **Returns**

        Sequence[:class:`Mods`]
        """
        if self.name is None:
            raise ValueError("Cannot get incompatible mods of a multi-mods enum object.")
        return list(map(lambda x: Mods[x], incompatible_mods[self.name]))

    def is_compatible_with(self, other: "Mods"):
        """
        Check if this mod is compatible with another mod.

        **Parameters**

        other: :class:`Mods`
            Mod to check compatibility with.

        **Returns**

        bool
        """
        if self.name is None or other.name is None:
            raise ValueError("Cannot check compatibility of a multi-mods enum object.")
        return other not in self.get_incompatible_mods()

    def is_compatible_combination(self):
        """
        Check if all the mods in this Mods object are compatible with each other.

        **Returns**

        bool
        """
        mods = list(self)

        for i in range(len(mods)):
            for j in range(i + 1, len(mods)):
                if not mods[i].is_compatible_with(mods[j]):
                    return False
        return True

    def to_readable_string(self):
        """
        Get a readable string representation of this mod (sorted by bitset ascending).
        Example: (Mods.HardRock | Mods.Hidden) -> "HDHR"

        **Returns**

        str
        """
        return "".join(map(lambda mod: Mod[mod.name].value, sorted(self, key=lambda m: m.value)))

    def __iter__(self):
        value = self.value
        for mod in reversed(Mods.__members__.values()):
            if value >= mod.value:
                value -= mod.value
                yield mod
            if value == 0:
                break


class RankStatus(IntEnum, metaclass=FallbackEnum):
    """
    IntEnum enum for rank status of a beatmap.

    **Statuses**

    GRAVEYARD = -2

    WIP = -1

    PENDING = 0

    RANKED = 1

    APPROVED = 2

    QUALIFIED = 3

    LOVED = 4
    """

    GRAVEYARD = -2
    WIP = -1
    PENDING = 0
    RANKED = 1
    APPROVED = 2
    QUALIFIED = 3
    LOVED = 4


class GameModeStr(Enum, metaclass=FallbackEnum):
    """
    Enum for GameModes using their string names.

    **GameModes**

    STANDARD = 'osu'

    TAIKO = 'taiko'

    CATCH = 'fruits'

    MANIA = 'mania'
    """

    STANDARD = "osu"
    TAIKO = "taiko"
    CATCH = "fruits"
    MANIA = "mania"

    def get_int_equivalent(self: "GameModeStr") -> "GameModeInt":
        return GameModeInt[self.name]


class GameModeInt(IntEnum, metaclass=FallbackEnum):
    """
    Enums for GameModes using their int values.

    **GameModes**

    STANDARD = 0

    TAIKO = 1

    CATCH = 2

    MANIA = 3
    """

    STANDARD = 0
    TAIKO = 1
    CATCH = 2
    MANIA = 3

    def get_str_equivalent(self: "GameModeInt") -> GameModeStr:
        return GameModeStr[self.name]


class WikiSearchMode(Enum, metaclass=FallbackEnum):
    """
    Enum for wiki search modes. Relevant to :func:`osu.Client.search`.

    ALL = "all"

    USER = "user"

    WIKI = "wiki_page"
    """

    ALL = "all"
    USER = "user"
    WIKI = "wiki_page"


class UserBeatmapType(Enum, metaclass=FallbackEnum):
    """
    User beatmap types. Relavent to :func:`osu.Client.get_user_beatmaps`.

    **User beatmap types**

    favourite, graveyard, loved, most_played, pending, ranked

    FAVOURITE = 'favourite'

    GRAVEYARD = 'graveyard'

    GUEST = 'guest'

    LOVED = 'loved'

    MOST_PLAYED = 'most_played'

    NOMINATED = 'nominated'

    PENDING = 'pending'

    RANKED = 'ranked'
    """

    FAVOURITE = "favourite"
    GRAVEYARD = "graveyard"
    GUEST = "guest"
    LOVED = "loved"
    MOST_PLAYED = "most_played"
    NOMINATED = "nominated"
    PENDING = "pending"
    RANKED = "ranked"


class RankingType(Enum, metaclass=FallbackEnum):
    """
    Ranking types to sort by for :func:`osu.Client.get_ranking`.

    **Ranking types**

    SPOTLIGHT = 'charts'

    COUNTRY = 'country'

    PERFORMANCE = 'performance'

    SCORE = 'score'

    TEAM = 'team'
    """

    SPOTLIGHT = "charts"
    COUNTRY = "country"
    PERFORMANCE = "performance"
    SCORE = "score"
    TEAM = "team"


class CommentSort(Enum, metaclass=FallbackEnum):
    """
    Type to sort comments by. Relevant to :func:`osu.Client.get_comments`.

    **Comment sorts**

    NEW = 'new'

    OLD = 'old'

    TOP = 'top'
    """

    NEW = "new"
    OLD = "old"
    TOP = "top"


class MultiplayerScoresSort(Enum, metaclass=FallbackEnum):
    """
    Sort option for multiplayer scores index. Relevant to :func:`osu.Client.get_scores`.

    **Multiplayer scores sorts**

    ASC = 'score_asc'

    DESC = 'score_desc'
    """

    ASC = "score_asc"
    DESC = "score_desc"


class BeatmapsetEventType(Enum, metaclass=FallbackEnum):
    """
    Enum for beatmapset event types. Relevant to :func:`osu.Client.get_beatmapset_events`.

    **Beatmapset event types**

    NOMINATE = 'nominate'

    LOVE = 'love'

    REMOVE_FROM_LOVED = 'unlove'

    QUALIFY = 'qualify'

    DISQUALIFY = 'disqualify'

    APPROVE = 'approve'

    RANK = 'rank'

    KUDOSU_ALLOW = 'kudosu_allow'

    KUDOSU_DENY = 'kudosu_deny'

    KUDOSU_GAIN = 'kudosu_gain'

    KUDOSU_LOST = 'kudosu_lost'

    KUDOSU_RECALCULATE = 'kudosu_recalculate'

    ISSUE_RESOLVE = 'issue_resolve'

    ISSUE_REOPEN = 'issue_reopen'

    DISCUSSION_LOCK = 'discussion_lock'

    DISCUSSION_UNLOCK = 'discussion_unlock'

    DISCUSSION_DELETE = 'discussion_delete'

    DISCUSSION_RESTORE = 'discussion_restore'

    DISCUSSION_POST_DELETE = 'discussion_post_delete'

    DISCUSSION_POST_RESTORE = 'discussion_post_restore'

    NOMINATION_RESET = 'nomination_reset'

    NOMINATION_RESET_RECEIVED = 'nomination_reset_received'

    GENRE_EDIT = 'genre_edit'

    LANGUAGE_EDIT = 'language_edit'

    NSFW_TOGGLE = 'nsfw_toggle'

    OFFSET_EDIT = 'offset_edit'

    BEATMAP_OWNER_CHANGE = 'beatmap_owner_change'
    """

    NOMINATE = "nominate"
    LOVE = "love"
    REMOVE_FROM_LOVED = "remove_from_loved"
    QUALIFY = "qualify"
    DISQUALIFY = "disqualify"
    APPROVE = "approve"
    RANK = "rank"

    KUDOSU_ALLOW = "kudosu_allow"
    KUDOSU_DENY = "kudosu_deny"
    KUDOSU_GAIN = "kudosu_gain"
    KUDOSU_LOST = "kudosu_lost"
    KUDOSU_RECALCULATE = "kudosu_recalculate"

    ISSUE_RESOLVE = "issue_resolve"
    ISSUE_REOPEN = "issue_reopen"

    DISCUSSION_LOCK = "discussion_lock"
    DISCUSSION_UNLOCK = "discussion_unlock"

    DISCUSSION_DELETE = "discussion_delete"
    DISCUSSION_RESTORE = "discussion_restore"

    DISCUSSION_POST_DELETE = "discussion_post_delete"
    DISCUSSION_POST_RESTORE = "discussion_post_restore"

    NOMINATION_RESET = "nomination_reset"
    NOMINATION_RESET_RECEIVED = "nomination_reset_received"

    GENRE_EDIT = "genre_edit"
    LANGUAGE_EDIT = "language_edit"
    NSFW_TOGGLE = "nsfw_toggle"
    OFFSET_EDIT = "offset_edit"

    BEATMAP_OWNER_CHANGE = "beatmap_owner_change"


class BeatmapsetEventSort(Enum, metaclass=FallbackEnum):
    """
    Sort option for beatmapset events. Relevant to :func:`osu.Client.get_beatmapset_events`.

    **Beatmapset event sorts**

    ASC = 'id_asc'

    DESC = 'id_desc'
    """

    ASC = "id_asc"
    DESC = "id_desc"


class MatchSort(Enum, metaclass=FallbackEnum):
    """
    Sort options for matches. Relevant to :func:`osu.Client.get_matches`.

    **Match sort options**

    ASCENDING = "id_asc"

    DESCENDING = "id_desc"
    """

    ASCENDING = "id_asc"
    DESCENDING = "id_desc"
    # purely for backwards compatibility
    OLDEST = "id_asc"
    NEWEST = "id_desc"


class MatchEventType(Enum, metaclass=FallbackEnum):
    """
    Enum for match event types.

    **Match event types**

    PLAYER_LEFT = 'player-left'

    PLAYER_JOINED = 'player-joined'

    PLAYER_KICKED = 'player-kicked'

    MATCH_CREATED = 'match-created'

    MATCH_DISBANDED = 'match-disbanded'

    HOST_CHANGED = 'host-changed'

    OTHER = 'other'
    """

    PLAYER_LEFT = "player-left"
    PLAYER_JOINED = "player-joined"
    PLAYER_KICKED = "player-kicked"
    MATCH_CREATED = "match-created"
    MATCH_DISBANDED = "match-disbanded"
    HOST_CHANGED = "host-changed"
    OTHER = "other"


class RoomSort(Enum, metaclass=FallbackEnum):
    """
    Sort options for rooms. Relevant to :func:`osu.Client.get_rooms`.

    **Room sort options**

    ENDED = 'ended'

    CREATED = 'created'
    """

    ENDED = "ended"
    CREATED = "created"


class RoomCategory(Enum, metaclass=FallbackEnum):
    """
    Enum for room categories.

    **Room categories**

    NORMAL = 'normal'

    SPOTLIGHT = 'spotlight'

    FEATURED_ARTIST = 'featured_artist'

    DAILY_CHALLENGE = 'daily_challenge'
    """

    NORMAL = "normal"
    SPOTLIGHT = "spotlight"
    FEATURED_ARTIST = "featured_artist"
    DAILY_CHALLENGE = "daily_challenge"


class RoomType(Enum, metaclass=FallbackEnum):
    """
    Enum for room types.

    **Room types**

    PLAYLISTS = "playlists"

    HEAD_TO_HEAD = "head_to_head"

    TEAM_VERSUS = "team_versus"
    """

    PLAYLISTS = "playlists"
    HEAD_TO_HEAD = "head_to_head"
    TEAM_VERSUS = "team_versus"


class RoomFilterMode(Enum, metaclass=FallbackEnum):
    """
    Enum for different filtering modes of rooms.

    **Room filter mode types**

    ENDED = 'ended'

    PARTICIPATED = 'participated'

    OWNED = 'owned'

    ACTIVE = 'active'
    """

    ENDED = "ended"
    PARTICIPATED = "participated"
    OWNED = "owned"
    ACTIVE = "active"


class RealTimeQueueMode(Enum, metaclass=FallbackEnum):
    """
    Enum for realtime queue modes.

    **Realtime queue modes**

    HOST_ONLY = 'host_only'

    ALL_PLAYERS = 'all_players'

    ALL_PLAYERS_ROUND_ROBIN = 'all_players_round_robin'
    """

    HOST_ONLY = "host_only"
    ALL_PLAYERS = "all_players"
    ALL_PLAYERS_ROUND_ROBIN = "all_players_round_robin"


class PlaylistQueueMode(Enum, metaclass=FallbackEnum):
    """
    Enum for playlist queue modes.

    **Playlist queue modes**

    HOST_ONLY = 'host_only'
    """

    HOST_ONLY = "host_only"


class BeatmapsetSearchSort(Enum, metaclass=FallbackEnum):
    """
    Sort options for beatmapset searches. Relevant to :func:`osu.Client.search_beatmapsets`.

    **Beatmapset search sort options**

    ARTIST = 'artist'

    CREATOR = 'creator'

    DIFFICULTY = 'difficulty'

    FAVOURITES = 'favourites'

    NOMINATIONS = 'nominations'

    PLAYS = 'plays'

    RANKED = 'ranked'

    RATING = 'rating'

    RELEVANCE = 'relevance'

    TITLE = 'title'

    UPDATED = 'updated'
    """

    ARTIST = "artist"
    CREATOR = "creator"
    DIFFICULTY = "difficulty"
    FAVOURITES = "favourites"
    NOMINATIONS = "nominations"
    PLAYS = "plays"
    RANKED = "ranked"
    RATING = "rating"
    RELEVANCE = "relevance"
    TITLE = "title"
    UPDATED = "updated"


class BeatmapsetSearchStatus(Enum, metaclass=FallbackEnum):
    """
    Status options for beatmapset filtering. Relevant to :func:`osu.Client.search_beatmapsets`.

    **Beatmapset search status options**

    ANY = 'any'

    HAS_LEADERBOARD = 'leaderboard'

    RANKED = 'ranked'

    QUALIFIED = 'qualified'

    LOVED = 'loved'

    FAVOURITES = 'favourites'

    PENDING = 'pending'

    WIP = 'wip'

    GRAVEYARD = 'graveyard'

    MY_MAPS = 'mine'
    """

    ANY = "any"
    HAS_LEADERBOARD = "leaderboard"
    RANKED = "ranked"
    QUALIFIED = "qualified"
    LOVED = "loved"
    FAVOURITES = "favourites"
    PENDING = "pending"
    WIP = "wip"
    GRAVEYARD = "graveyard"
    MY_MAPS = "mine"


class BeatmapsetSearchExtra(Enum, metaclass=FallbackEnum):
    """
    Extra options for beatmapset filtering. Relevant to :func:`osu.Client.search_beatmapsets`.

    **Beatmapset search extra options**

    VIDEO = 'video'

    STORYBOARD = 'storyboard'
    """

    VIDEO = "video"
    STORYBOARD = "storyboard"


class BeatmapsetSearchGeneral(Enum, metaclass=FallbackEnum):
    """
    General options for beatmapset filtering. Relevant to :func:`osu.Client.search_beatmapsets`.

    **Beatmapset search general options**

    RECOMMENDED = 'recommended'

    CONVERTS = 'converts'

    FOLLOWS = 'follows'

    SPOTLIGHTS = 'spotlights'

    FEATURED_ARTISTS = 'featured_artists'
    """

    RECOMMENDED = "recommended"
    CONVERTS = "converts"
    FOLLOWS = "follows"
    SPOTLIGHTS = "spotlights"
    FEATURED_ARTISTS = "featured_artists"


class BeatmapsetSearchPlayed(Enum, metaclass=FallbackEnum):
    """
    Played options for beatmapset filtering. Relevant to :func:`osu.Client.search_beatmapsets`.

    **Beatmapset search played options**

    ANY = 'any'

    PLAYED = 'played'

    UNPLAYED = 'unplayed'
    """

    ANY = "any"
    PLAYED = "played"
    UNPLAYED = "unplayed"


class BeatmapsetLanguage(IntEnum, metaclass=FallbackEnum):
    """
    Language of a beatmapset

    **Languages**

    UNSPECIFIED = 1

    ENGLISH = 2

    JAPANESE = 3

    CHINESE = 4

    INSTRUMENTAL = 5

    KOREAN = 6

    FRENCH = 7

    GERMAN = 8

    SWEDISH = 9

    SPANISH = 10

    ITALIAN = 11

    RUSSIAN = 12

    POLISH = 13

    OTHER = 14
    """

    UNSPECIFIED = 1
    ENGLISH = 2
    JAPANESE = 3
    CHINESE = 4
    INSTRUMENTAL = 5
    KOREAN = 6
    FRENCH = 7
    GERMAN = 8
    SWEDISH = 9
    SPANISH = 10
    ITALIAN = 11
    RUSSIAN = 12
    POLISH = 13
    OTHER = 14


class BeatmapsetGenre(IntEnum, metaclass=FallbackEnum):
    """
    Genre of a beatmapsets

    **Genres**

    UNSPECIFIED = 1

    VIDEO_GAME = 2

    ANIME = 3

    ROCK = 4

    POP = 5

    OTHER = 6

    NOVELTY = 7

    HIP_HOP = 9

    ELECTRONIC = 10

    METAL = 11

    CLASSICAL = 12

    FOLK = 13

    JAZZ = 14
    """

    UNSPECIFIED = 1
    VIDEO_GAME = 2
    ANIME = 3
    ROCK = 4
    POP = 5
    OTHER = 6
    NOVELTY = 7
    HIP_HOP = 9
    ELECTRONIC = 10
    METAL = 11
    CLASSICAL = 12
    FOLK = 13
    JAZZ = 14


class ScoreRank(Enum, metaclass=FallbackEnum):
    """
    Enum for score ranks.

    **Score ranks**

    SILVER_SS = 'XH'

    SS = 'X'

    SILVER_S = 'SH'

    S = 'S'

    A = 'A'

    B = 'B'

    C = 'C'

    D = 'D'

    F = 'F'
    """

    SILVER_SS = "XH"
    SS = "X"
    SILVER_S = "SH"
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class ObjectType(Enum, metaclass=FallbackEnum):
    """
    Enum for different object types. Score types are most relevant.

    **Object types**

    BeatmapDiscussion = "beatmapset_discussion"

    BeatmapDiscussionPost = "beatmapset_discussion_post"

    Beatmapset = "beatmapset"

    Build = "build"

    Channel = "channel"

    Comment = "comment"

    ForumPost = "forum_post"

    ForumTopic = "forum_topic"

    LegacyMatchScore = "legacy_match_score"

    NewsPost = "news_post"

    ScoreBestFruits = "score_best_fruits"

    ScoreBestMania = "score_best_mania"

    ScoreBestOsu = "score_best_osu"

    ScoreBestTaiko = "score_best_taiko"

    ScoreFruits = "score_fruits"

    ScoreMania = "score_mania"

    ScoreOsu = "score_osu"

    ScoreTaiko = "score_taiko"

    SoloScore = "solo_score"

    User = "user"
    """

    @staticmethod
    def enum__new__(cls, value):
        if value == "beatmap_discussion":
            return super().__new__(cls, "beatmapset_discussion")

        return super().__new__(cls, value)

    BeatmapDiscussion = "beatmapset_discussion"
    BeatmapDiscussionPost = "beatmapset_discussion_post"
    Beatmapset = "beatmapset"
    Build = "build"
    Channel = "channel"
    Comment = "comment"
    ForumPost = "forum_post"
    ForumTopic = "forum_topic"
    LegacyMatchScore = "legacy_match_score"
    NewsPost = "news_post"
    ScoreBestFruits = "score_best_fruits"
    ScoreBestMania = "score_best_mania"
    ScoreBestOsu = "score_best_osu"
    ScoreBestTaiko = "score_best_taiko"
    ScoreFruits = "score_fruits"
    ScoreMania = "score_mania"
    ScoreOsu = "score_osu"
    ScoreTaiko = "score_taiko"
    SoloScore = "solo_score"
    User = "user"


class UserScoreType(Enum, metaclass=FallbackEnum):
    """
    Enum for the get_user_scores endpoint that specifies score type.

    **User score types**

    BEST = "best"

    FIRSTS = "firsts"

    RECENT = "recent"

    PINNED = "pinned"
    """

    BEST = "best"
    FIRSTS = "firsts"
    RECENT = "recent"
    PINNED = "pinned"


class ForumTopicType(Enum, metaclass=FallbackEnum):
    """
    Enum for :class:`ForumTopic` type attribute.

    **Forum topic types**

    NORMAL = "normal"

    STICKY = "sticky"

    ANNOUNCEMENT = "announcement"
    """

    NORMAL = "normal"
    STICKY = "sticky"
    ANNOUNCEMENT = "announcement"


class ChatChannelType(Enum, metaclass=FallbackEnum):
    """
    Enum for type of :class:`ChatChannel`

    **Chat channel types**

    PUBLIC = "PUBLIC"

    PRIVATE = "PRIVATE"

    MULTIPLAYER = "MULTIPLAYER"

    SPECTATOR = "SPECTATOR"

    TEMPORARY = "TEMPORARY"

    PM = "PM"

    GROUP = "GROUP"

    ANNOUNCE = "ANNOUNCE"
    """

    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    MULTIPLAYER = "MULTIPLAYER"
    SPECTATOR = "SPECTATOR"
    TEMPORARY = "TEMPORARY"
    PM = "PM"
    GROUP = "GROUP"
    ANNOUNCE = "ANNOUNCE"


class NotificationType(Enum, metaclass=FallbackEnum):
    """
    Types of notifications that can be received.

    **Notification types**

    BEATMAP_OWNER_CHANGE = 'beatmap_owner_change'

    BEATMAPSET_DISCUSSION_LOCK = 'beatmapset_discussion_lock'

    BEATMAPSET_DISCUSSION_POST_NEW = 'beatmapset_discussion_post_new'

    BEATMAPSET_DISCUSSION_QUALIFIED_PROBLEM = 'beatmapset_discussion_qualified_problem'

    BEATMAPSET_DISCUSSION_REVIEW_NEW = 'beatmapset_discussion_review_new'

    BEATMAPSET_DISCUSSION_UNLOCK = 'beatmapset_discussion_unlock'

    BEATMAPSET_DISQUALIFY = 'beatmapset_disqualify'

    BEATMAPSET_LOVE = 'beatmapset_love'

    BEATMAPSET_NOMINATE = 'beatmapset_nominate'

    BEATMAPSET_QUALIFY = 'beatmapset_qualify'

    BEATMAPSET_RANK = 'beatmapset_rank'

    BEATMAPSET_REMOVE_FROM_LOVED = 'beatmapset_remove_from_loved'

    BEATMAPSET_RESET_NOMINATIONS = 'beatmapset_reset_nominations'

    CHANNEL_ANNOUNCEMENT = 'channel_announcement'

    CHANNEL_MESSAGE = 'channel_message'

    COMMENT_NEW = 'comment_new'

    FORUM_TOPIC_REPLY = 'forum_topic_reply'

    USER_ACHIEVEMENT_UNLOCK = 'user_achievement_unlock'

    USER_BEATMAPSET_NEW = 'user_beatmapset_new'

    USER_BEATMAPSET_REVIVE = 'user_beatmapset_revive'
    """

    BEATMAP_OWNER_CHANGE = "beatmap_owner_change"
    BEATMAPSET_DISCUSSION_LOCK = "beatmapset_discussion_lock"
    BEATMAPSET_DISCUSSION_POST_NEW = "beatmapset_discussion_post_new"
    BEATMAPSET_DISCUSSION_QUALIFIED_PROBLEM = "beatmapset_discussion_qualified_problem"
    BEATMAPSET_DISCUSSION_REVIEW_NEW = "beatmapset_discussion_review_new"
    BEATMAPSET_DISCUSSION_UNLOCK = "beatmapset_discussion_unlock"
    BEATMAPSET_DISQUALIFY = "beatmapset_disqualify"
    BEATMAPSET_LOVE = "beatmapset_love"
    BEATMAPSET_NOMINATE = "beatmapset_nominate"
    BEATMAPSET_QUALIFY = "beatmapset_qualify"
    BEATMAPSET_RANK = "beatmapset_rank"
    BEATMAPSET_REMOVE_FROM_LOVED = "beatmapset_remove_from_loved"
    BEATMAPSET_RESET_NOMINATIONS = "beatmapset_reset_nominations"
    CHANNEL_ANNOUNCEMENT = "channel_announcement"
    CHANNEL_MESSAGE = "channel_message"
    COMMENT_NEW = "comment_new"
    FORUM_TOPIC_REPLY = "forum_topic_reply"
    USER_ACHIEVEMENT_UNLOCK = "user_achievement_unlock"
    USER_BEATMAPSET_NEW = "user_beatmapset_new"
    USER_BEATMAPSET_REVIVE = "user_beatmapset_revive"

    def get_category(self):
        return NotificationCategory[self.name]


class NotificationCategory(Enum, metaclass=FallbackEnum):
    """
    Enum for notification categories.

    **Notification Categories**

    BEATMAP_OWNER_CHANGE = 'beatmap_owner_change'

    BEATMAPSET_DISCUSSION_LOCK = 'beatmapset_discussion'

    BEATMAPSET_DISCUSSION_POST_NEW = 'beatmapset_discussion'

    BEATMAPSET_DISCUSSION_QUALIFIED_PROBLEM = 'beatmapset_problem'

    BEATMAPSET_DISCUSSION_REVIEW_NEW = 'beatmapset_discussion'

    BEATMAPSET_DISCUSSION_UNLOCK = 'beatmapset_discussion'

    BEATMAPSET_DISQUALIFY = 'beatmapset_state'

    BEATMAPSET_LOVE = 'beatmapset_state'

    BEATMAPSET_NOMINATE = 'beatmapset_state'

    BEATMAPSET_QUALIFY = 'beatmapset_state'

    BEATMAPSET_RANK = 'beatmapset_state'

    BEATMAPSET_REMOVE_FROM_LOVED = 'beatmapset_state'

    BEATMAPSET_RESET_NOMINATIONS = 'beatmapset_state'

    CHANNEL_ANNOUNCEMENT = 'announcement'

    CHANNEL_MESSAGE = 'channel'

    COMMENT_NEW = 'comment'

    FORUM_TOPIC_REPLY = 'forum_topic_reply'

    USER_ACHIEVEMENT_UNLOCK = 'user_achievement_unlock'

    USER_BEATMAPSET_NEW = 'user_beatmapset_new'

    USER_BEATMAPSET_REVIVE = 'user_beatmapset_new'
    """

    BEATMAP_OWNER_CHANGE = "beatmap_owner_change"
    BEATMAPSET_DISCUSSION_LOCK = "beatmapset_discussion"
    BEATMAPSET_DISCUSSION_POST_NEW = "beatmapset_discussion"
    BEATMAPSET_DISCUSSION_QUALIFIED_PROBLEM = "beatmapset_problem"
    BEATMAPSET_DISCUSSION_REVIEW_NEW = "beatmapset_discussion"
    BEATMAPSET_DISCUSSION_UNLOCK = "beatmapset_discussion"
    BEATMAPSET_DISQUALIFY = "beatmapset_state"
    BEATMAPSET_LOVE = "beatmapset_state"
    BEATMAPSET_NOMINATE = "beatmapset_state"
    BEATMAPSET_QUALIFY = "beatmapset_state"
    BEATMAPSET_RANK = "beatmapset_state"
    BEATMAPSET_REMOVE_FROM_LOVED = "beatmapset_state"
    BEATMAPSET_RESET_NOMINATIONS = "beatmapset_state"
    CHANNEL_ANNOUNCEMENT = "announcement"
    CHANNEL_MESSAGE = "channel"
    COMMENT_NEW = "comment"
    FORUM_TOPIC_REPLY = "forum_topic_reply"
    USER_ACHIEVEMENT_UNLOCK = "user_achievement_unlock"
    USER_BEATMAPSET_NEW = "user_beatmapset_new"
    USER_BEATMAPSET_REVIVE = "user_beatmapset_new"


class UserAccountHistoryType(Enum, metaclass=FallbackEnum):
    """
    Type of account history object

    **User Account History Types**

    NOTE = "note"

    RESTRICTION = "restriction"

    SILENCE = "silence"

    TOURNAMENT_BAN = "tournament_ban"
    """

    NOTE = "note"
    RESTRICTION = "restriction"
    SILENCE = "silence"
    TOURNAMENT_BAN = "tournament_ban"


class MessageType(Enum, metaclass=FallbackEnum):
    """
    A type of message in beatmapset discussion

    **Message types**

    HYPE = "hype"

    MAPPER_NOTE = "mapper_note"

    PRAISE = "praise"

    PROBLEM = "problem"

    REVIEW = "review"

    SUGGESTION = "suggestion"
    """

    HYPE = "hype"
    MAPPER_NOTE = "mapper_note"
    PRAISE = "praise"
    PROBLEM = "problem"
    REVIEW = "review"
    SUGGESTION = "suggestion"


class KudosuAction(Enum, metaclass=FallbackEnum):
    """
    A type of action related to kudosu

    **Kudosu action types**

    GIVE = "give"

    VOTE_GIVE = "vote.give"

    RESET = "reset"

    VOTE_RESET = "vote.reset"

    REVOKE = "revoke"

    VOTE_REVOKE = "vote.revoke"

    RECALCULATE_RESET = "recalculate.reset"
    """

    GIVE = "give"
    VOTE_GIVE = "vote.give"
    RESET = "reset"
    VOTE_RESET = "vote.reset"
    REVOKE = "revoke"
    VOTE_REVOKE = "vote.revoke"
    RECALCULATE_RESET = "recalculate.reset"
    DENY_KUDOSU_RESET = "deny_kudosu.reset"


class ScoringType(Enum, metaclass=FallbackEnum):
    """
    Scoring type used for a legacy multiplayer match

    **Scoring types**

    SCORE = "score"

    ACCURACY = "accuracy"

    COMBO = "combo"

    SCOREV2 = "scorev2"
    """

    SCORE = "score"
    ACCURACY = "accuracy"
    COMBO = "combo"
    SCOREV2 = "scorev2"


class TeamType(Enum, metaclass=FallbackEnum):
    """
    The team type used for a legacy multiplayer match

    **Team types**

    HEAD_TO_HEAD = "head-to-head"

    TAG_COOP = "tag-coop"

    TEAM_VS = "team-vs"

    TAG_TEAM_VS = "tag-team-vs"
    """

    HEAD_TO_HEAD = "head-to-head"
    TAG_COOP = "tag-coop"
    TEAM_VS = "team-vs"
    TAG_TEAM_VS = "tag-team-vs"


class UserRelationType(Enum, metaclass=FallbackEnum):
    """
    The type of relation to a user

    **Relation types**

    FRIEND = "friend"

    BLOCK = "block"
    """

    FRIEND = "friend"
    BLOCK = "block"


class ChatMessageType(Enum, metaclass=FallbackEnum):
    """
    The type of a :class:`ChatMessage`

    **Chat message types**

    ACTION = "action"

    MARKDOWN = "markdown"

    PLAIN = "plain"
    """

    ACTION = "action"
    MARKDOWN = "markdown"
    PLAIN = "plain"


class RoomStatus(Enum, metaclass=FallbackEnum):
    """
    Possible statuses for a :class:`Room`

    **Room statuses**

    IDLE = "idle"

    PLAYING = "playing"
    """

    IDLE = "idle"
    PLAYING = "playing"
