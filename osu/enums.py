from enum import IntFlag, IntEnum
from typing import Sequence
from .constants import mod_abbreviations


class Mods(IntFlag):
    NoFail = 1 << 0
    Easy = 1 << 1
    TouchDevice = 1 << 2  # Replaces unused NoVideo mod
    Hidden = 1 << 3
    HardRock = 1 << 4
    SuddenDeath = 1 << 5
    DoubleTime = 1 << 6
    Relax = 1 << 7
    HalfTime = 1 << 8
    Nightcore = (1 << 9) + (1 << 6)  # Always used with DT
    Flashlight = 1 << 10
    Autoplay = 1 << 11  # Auto
    SpunOut = 1 << 12
    Relax2 = 1 << 13  # AutoPilot
    Perfect = 1 << 14
    Key4 = 1 << 15
    Key5 = 1 << 16
    Key6 = 1 << 17
    Key7 = 1 << 18
    Key8 = 1 << 19
    keyMod = (1 << 15) + (1 << 16) +  (1 << 17) + (1 << 18) + (1 << 19)  # k4+k5+k6+k7+k8
    FadeIn = 1 << 21
    Random = 1 << 22
    LastMod = 1 << 23  # Cinema
    TargetPractice = 1 << 24
    Key9 = 1 << 25
    Coop = 1 << 26
    Key1 = 1 << 27
    Key3 = 1 << 28
    Key2 = 1 << 29
    ScoreV2 = 1 << 30
    Mirror = 1 << 31

    @classmethod
    def get_from_abbreviation(cls, abbreviation: str):
        return cls[mod_abbreviations[abbreviation]]

    @staticmethod
    def get_from_list(mods: Sequence):
        a = mods[0]
        for i in range(1, len(mods)):
            a |= mods[i]
        return a

    @staticmethod
    def parse_and_return_any_list(mods: Sequence):
        ret = []
        for mod in mods:
            if isinstance(mod, Mods):
                ret.append(mod)
            elif isinstance(mod, str):
                try:
                    ret.append(Mods[mod])
                except KeyError:
                    ret.append(Mods.get_from_abbreviation(mod))
        return ret


class RankStatus(IntEnum):
    GRAVEYARD = -2
    WIP = -1
    PENDING = 0
    RANKED = 1
    APPROVED = 2
    QUALIFIED = 3
    LOVED = 4
