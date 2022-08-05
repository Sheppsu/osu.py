from enum import IntFlag, IntEnum, Enum
from typing import Sequence, Union
from .constants import mod_abbreviations, incompatible_mods, mod_abbreviations_reversed


class Mods(IntFlag):
    """
    IntFlag enum for all mods. Info gathered from
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
    Nightcore = (1 << 9)
    Flashlight = 1 << 10
    SpunOut = 1 << 12
    AutoPilot = 1 << 13
    Perfect = 1 << 14
    FadeIn = 1 << 20
    Mirror = 1 << 30

    Key4 = 1 << 15
    Key5 = 1 << 16
    Key6 = 1 << 17
    Key7 = 1 << 18
    Key8 = 1 << 19
    Key9 = 1 << 24

    @classmethod
    def get_from_abbreviation(cls, abbreviation: str) -> 'Mods':
        """
        Get mod from its abbreviation. Abbreviations are taken from https://osu.ppy.sh/wiki/en/Game_modifier/Summary

        **Parameters**

        abbreviation: :class:`str`
            Abbreviation of the mod (must be capitalized)

        **Returns**

        :class:`Mods`
        """
        return cls[mod_abbreviations[abbreviation.upper()]]

    @staticmethod
    def get_from_list(mods: Sequence['Mods']) -> 'Mods':
        """
        Get a :class:`Mods` object from a list of :class:`Mods`.

        **Parameters**

        mods: Sequence[:class:`Mods`]
            Sequence of mods of type Mods

        **Returns**

        :class:`Mods`
        """
        a = mods[0]
        for i in range(1, len(mods)):
            a |= mods[i]
        return a

    @staticmethod
    def parse_any_list(mods: Sequence[Union[str, int, 'Mods']]) -> 'Mods':
        """
        Take a list and return a parsed list. Parsing the list involves
        converting any object recognizable as a mod to a :class:`Mods` object.
        This includes mod names/abbreviations as strings and also their bitset values.

        **Parameters**

        mods: Sequence[Union[:class:`Mods`, :class:`str`, :class:`int`]]
            Sequence of :class:`Mods`, :class:`str`, and/or :class:`int` objects
            to be parsed and returned as a :class:`Mods` object.

        **Returns**

        :class:`Mods`
        """
        ret = []
        for mod in mods:
            if isinstance(mod, Mods):
                ret.append(mod)
            elif isinstance(mod, str):
                if mod.upper() in mod_abbreviations:
                    ret.append(Mods.get_from_abbreviation(mod.upper()))
                elif mod in Mods.__members__:
                    ret.append(Mods[mod])
                else:
                    raise ValueError("Mods represented as strings must be either the full name or abbreviation. "
                                     f"'{mod}' does not fall under either of those.")
            elif isinstance(mod, int):
                ret.append(Mods(mod))
            else:
                raise TypeError("Mods can only be parsed to Mods objects if they're of type str, int, or Mods")
        return Mods.get_from_list(ret)

    def get_incompatible_mods(self):
        """
        Get a list of mods that are incompatible with this mod.

        **Returns**

        Sequence[:class:`Mods`]
        """
        if self.name is None:
            raise ValueError("Cannot get incompatible mods of a multi-mods enum object.")
        return list(map(lambda x: Mods[x], incompatible_mods[self.name]))

    def is_compatible_with(self, other: 'Mods'):
        """
        Check if this mod is compatible with another mod.

        **Parameters**

        other: :class:`Mods`
            Mod to check compatibility with.

        **Returns**

        :class:`bool`
        """
        if self.name is None or other.name is None:
            raise ValueError("Cannot check compatibility of a multi-mods enum object.")
        return other not in self.get_incompatible_mods()

    def is_compatible_combination(self):
        """
        Check if all the mods in this Mods object are compatible with each other.

        **Returns**

        :class:`bool`
        """
        mods = list(self)

        for i in range(len(mods)):
            for j in range(i+1, len(mods)):
                if not mods[i].is_compatible_with(mods[j]):
                    return False
        return True

    def to_readable_string(self):
        """
        Get a readable string representation of this mod (sorted by bitset ascending).
        Example: (Mods.HardRock | Mods.Hidden) -> "HDHR"

        **Returns**

        :class:`str`
        """
        return "".join(map(lambda mod: mod_abbreviations_reversed[mod.name],
                           sorted(self, key=lambda m: m.value)))

    def __iter__(self):
        mods = str(self).split('|')
        mods[0] = mods[0].replace("Mods.", "")
        mods = list(map(lambda x: Mods[x], mods))
        return iter(mods)


class RankStatus(IntEnum):
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


class GameModeStr(Enum):
    """
    Enum for GameModes using their string names.

    **GameModes**

    STANDARD = 'osu'

    TAIKO = 'taiko'

    CATCH = 'fruits'

    MANIA = 'mania'
    """
    STANDARD = 'osu'
    TAIKO = 'taiko'
    CATCH = 'fruits'
    MANIA = 'mania'

    @staticmethod
    def get_int_equivalent(gamemode: Enum) -> IntEnum:
        return GameModeInt[gamemode.name]


class GameModeInt(IntEnum):
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

    @staticmethod
    def get_str_equivalent(gamemode: IntEnum) -> Enum:
        return GameModeStr[gamemode.name]


class WikiSearchMode(Enum):
    """
    Enum for wiki search modes. Relevant to :func:`osu.Client.search`.
    """
    ALL = 'all'
    USER = 'user'
    WIKI = 'wiki_page'


class UserBeatmapType(Enum):
    """
    User beatmap types. Relavent to :func:`osu.Client.get_user_beatmaps`.

    **User beatmap types**

    favourite, graveyard, loved, most_played, pending, ranked

    FAVOURITE = 'favourite'

    GRAVEYARD = 'graveyard'

    LOVED = 'loved'

    MOST_PLAYED = 'most_played'

    PENDING = 'pending'

    RANKED = 'ranked'
    """

    FAVOURITE = 'favourite'
    GRAVEYARD = 'graveyard'
    LOVED = 'loved'
    MOST_PLAYED = 'most_played'
    PENDING = 'pending'
    RANKED = 'ranked'


class RankingType(Enum):
    """
    Ranking types to sort by for :func:`osu.Client.get_ranking`.

    **Ranking types**

    SPOTLIGHT = 'charts'

    COUNTRY = 'country'

    PERFORMANCE = 'performance'

    SCORE = 'score'
    """
    SPOTLIGHT = 'charts'
    COUNTRY = 'country'
    PERFORMANCE = 'performance'
    SCORE = 'score'


class CommentSort(Enum):
    """
    Type to sort comments by. Relevant to :func:`osu.Client.get_comments`.

    **Comment sorts**

    NEW = 'new'

    OLD = 'old'

    TOP = 'top'
    """
    NEW = 'new'
    OLD = 'old'
    TOP = 'top'


class MultiplayerScoresSort(Enum):
    """
    Sort option for multiplayer scores index. Relevant to :func:`osu.Client.get_scores`.

    **Multiplayer scores sorts**

    ASC = 'score_asc'

    DESC = 'score_desc'
    """
    ASC = 'score_asc'
    DESC = 'score_desc'
