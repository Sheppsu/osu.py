from .enums import Mods, Enum, BeatmapsetSearchSort, BeatmapsetSearchGeneral, BeatmapsetSearchPlayed, \
    BeatmapsetSearchStatus, BeatmapsetSearchExtra, ScoreRank, GameModeInt, Mod
from typing import Sequence, Union


def check_scope(func):
    def check(self, other):
        if not isinstance(other, self.__class__) and type(other) != str:
            raise TypeError(f"Cannot compare type Scope with type {type(other).__name__}")
        if isinstance(other, self.__class__):
            other = other.scope
        if other not in self.valid_scopes:
            raise NameError(f"{other} is not a valid scope.")
        return func(self, other)
    return check


def create_autoclass_for_sphinx():
    with open('objects.py', 'r') as f:
        info = f.readline()
        while info:
            if info.startswith('class'):
                name = info.split()[1]
                if '(' in name:
                    name = name.split('(')[0]
                else:
                    name = name[:-1]
                content = f"{name}\n{'^' * len(name)}\n.. autoclass:: osu.{name}\n   :members:\n\n"
                with open('text.txt', 'a') as f2:
                    f2.write(content)
                    f2.close()
            info = f.readline()
        f.close()


def parse_mods_arg(mods):
    if mods is None:
        return
    if isinstance(mods, Mods):
        return mods.value
    if isinstance(mods, Sequence):
        if len(mods) == 0:
            return
        return Mods.parse_any_list(mods).value
    raise TypeError(f"mods argument must be of type Mods or Sequence, not {type(mods)}")


def prettify(cls: object, *fields: str) -> str:
    d = {s: getattr(cls, s) for s in fields}
    return cls.__class__.__qualname__ + '(' + ', '.join([f"{k}={d[k]!r}" for k in d]) + ')'


def parse_enum_args(*args):
    args = [arg.value if isinstance(arg, Enum) else arg for arg in args]
    return args if len(args) != 1 else args[0]


def create_multipart_formdata(data: dict):
    return {k: (None, v, "text/plain", {"charset": "utf-8"}) for k, v in data.items()}


class Util:
    @staticmethod
    def int(value):
        if value is None:
            return
        return int(value)

    @staticmethod
    def float(value):
        if value is None:
            return
        return float(value)


class BeatmapsetSearchFilter:
    """
    Util class that helps for filtering in :func:`Client.search_beatmapsets`.

    Read about each filter under its corresponding function.

    All set functions return the instance of the class to allow for chaining.
    """
    def __init__(self):
        self._filters = {
            "query": None,
            "sort": None,
            "nsfw": None,
            "played": None,
            "r": None,
            "m": None,
            "l": None,
            "g": None,
            "e": None,
            "c": None,
            "s": None,
        }

    def set_query(self, query: str) -> 'BeatmapsetSearchFilter':
        """
        Set the query to search for.

        query: :class:`str`
        """
        self._filters["query"] = query
        return self

    def set_sort(self, sort: Union[BeatmapsetSearchSort, str]) -> 'BeatmapsetSearchFilter':
        """
        Set the sort order of the search.

        sort: Union[:class:`BeatmapsetSearchSort`, :class:`str`]
        """
        self._filters["sort"] = sort.value if isinstance(sort, BeatmapsetSearchSort) else sort
        return self

    def set_nsfw(self, nsfw: bool) -> 'BeatmapsetSearchFilter':
        """
        Set whether to include NSFW in the search.

        nsfw: :class:`bool`
        """
        self._filters["nsfw"] = nsfw
        return self

    def set_played(self, played: Union[BeatmapsetSearchPlayed, str]) -> 'BeatmapsetSearchFilter':
        """
        Set whether to include played and unplayed beatmapsets in the search.

        played: Union[:class:`BeatmapsetSearchPlayed`, :class:`str`]
        """
        self._filters["played"] = played.value if isinstance(played, BeatmapsetSearchPlayed) else played
        return self

    def set_ranked(self, rank: Union[ScoreRank, str]) -> 'BeatmapsetSearchFilter':
        """
        Filter by rank achieved.

        rank: Union[:class:`ScoreRank`, :class:`str`]
        """
        self._filters["r"] = rank.value if isinstance(rank, ScoreRank) else rank
        return self

    def set_mode(self, mode: Union[GameModeInt, str]) -> 'BeatmapsetSearchFilter':
        """
        Set the game mode to filter by.

        mode: Union[:class:`GameModeStr`, :class:`str`]
        """
        self._filters["m"] = mode.value if isinstance(mode, GameModeInt) else mode
        return self

    def set_language(self, language: str) -> 'BeatmapsetSearchFilter':
        """
        Set the language to filter by.

        language: :class:`str`
        """
        self._filters["l"] = language
        return self

    def set_genre(self, genre: str) -> 'BeatmapsetSearchFilter':
        """
        Set the genre to filter by.

        genre: :class:`str`
        """
        self._filters["g"] = genre
        return self

    def set_extra(self, extras: Sequence[Union[BeatmapsetSearchExtra, str]]) -> 'BeatmapsetSearchFilter':
        """
        Set the extras to filter by.

        extras: Sequence[Union[:class:`BeatmapsetSearchExtra`, :class:`str`]]
        """
        self._filters["e"] = ".".join(list(map(
            lambda x: x.value if isinstance(x, BeatmapsetSearchExtra) else x, extras)))
        return self

    def set_generals(self, generals: Sequence[Union[BeatmapsetSearchGeneral, str]]) -> 'BeatmapsetSearchFilter':
        """
        Set the generals to filter by.

        generals: Sequence[Union[:class:`BeatmapsetSearchGeneral`, :class:`str`]]
        """
        self._filters["c"] = ".".join(list(map(
            lambda x: x.value if isinstance(x, BeatmapsetSearchGeneral) else x, generals)))
        return self

    def set_status(self, status: Union[BeatmapsetSearchStatus, str]) -> 'BeatmapsetSearchFilter':
        """
        Set the status to filter by.

        status: Union[:class:`BeatmapsetSearchStatus`, :class:`str`]
        """
        self._filters["s"] = status.value if isinstance(status, BeatmapsetSearchStatus) else status
        return self

    @property
    def filters(self):
        """
        Dictionary of all filters only including ones that have been set.
        """
        return {k: v for k, v in self._filters.items() if v is not None}


class PlaylistItemUtil:
    """
    Util class for passing playlist items to endpoints that involve creating a room
    like create_multiplayer_room and create_playlist.

    **Init Parameters**

    beatmap_id: :class:`int`

    ruleset_id: Union[:class:`GameModeInt`, :class:`int`]

    allowed_mods: Sequence[:class:`Mod`]

    required_mods: Sequence[:class:`Mod`]

    **Properties**

    json: :class:`dict`
        Dictionary format of all the attributes which the client uses
        when sending a http request
    """
    __slots__ = ("beatmap_id", "ruleset_id", "allowed_mods", "required_mods")

    def __init__(self, beatmap_id: int, ruleset_id: Union[GameModeInt, int],
                 allowed_mods: Sequence[Mod] = None, required_mods: Sequence[Mod] = None):
        self.beatmap_id = beatmap_id
        self.ruleset_id = ruleset_id
        self.allowed_mods = allowed_mods
        self.required_mods = required_mods

    @property
    def json(self) -> dict:
        def mod_map(mod):
            return {"acronym": mod.value}
        return {
            "beatmap_id": self.beatmap_id,
            "ruleset_id": parse_enum_args(self.ruleset_id),
            "allowed_mods": list(map(mod_map, self.allowed_mods)) if self.allowed_mods is not None else None,
            "required_mods": list(map(mod_map, self.required_mods)) if self.required_mods is not None else None,
        }
