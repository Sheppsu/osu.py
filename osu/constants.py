import os

base_url = lambda domain: f"https://{domain}/api/v2/"
auth_url = lambda domain: f"https://{domain}/oauth/authorize/"
token_url = lambda domain: f"https://{domain}/oauth/token/"

DEFAULT_DOMAIN = os.getenv("OSUPY_DEFAULT_DOMAIN") or "osu.ppy.sh"
DEFAULT_BASE_URL = base_url(DEFAULT_DOMAIN)
DEFAULT_AUTH_URL = auth_url(DEFAULT_DOMAIN)
DEFAULT_TOKEN_URL = token_url(DEFAULT_DOMAIN)

# Info gathered from https://github.com/ppy/osu-web/blob/973315aded8a5762fc00a9f245337802c27bd213/database/mods.json
incompatible_mods = {
    "NoFail": ["SuddenDeath", "Perfect", "AutoPilot", "Relax"],
    "Easy": ["HardRock"],
    "TouchDevice": [],
    "Hidden": [],
    "HardRock": ["Easy", "Mirror"],
    "SuddenDeath": ["NoFail", "Perfect", "Relax", "AutoPilot"],
    "DoubleTime": ["HalfTime"],
    "Relax": ["NoFail", "SuddenDeath", "Perfect", "AutoPilot"],
    "HalfTime": ["DoubleTime", "Nightcore"],
    "Nightcore": ["HalfTime"],
    "Flashlight": [],
    "SpunOut": ["AutoPilot"],
    "AutoPilot": ["NoFail", "SuddenDeath", "Perfect", "Relax", "SpunOut"],
    "Perfect": ["NoFail", "SuddenDeath", "Relax"],
    "FadeIn": ["Hidden", "Flashlight"],
    "Mirror": ["HardRock"],
    **{f"Key{k}": [f"Key{k2}" for k2 in range(4, 10) if k2 != k] for k in range(4, 10)},
}
