base_url = "https://osu.ppy.sh/api/v2/"
auth_url = "https://osu.ppy.sh/oauth/authorize/"
token_url = "https://osu.ppy.sh/oauth/token/"

mod_abbreviations = {
    "NF": "NoFail",
    "EZ": "Easy",
    "TD": "TouchDevice",
    "HD": "Hidden",
    "HR": "HardRock",
    "SD": "SuddenDeath",
    "DT": "DoubleTime",
    "RL": "Relax",
    "HT": "HalfTime",
    "NC": "Nightcore",
    "FL": "Flashlight",
    "SO": "SpunOut",
    "AP": "AutoPilot",
    "PF": "Perfect",
    "FI": "FadeIn",
    "MR": "Mirror",
    **{f"{k}K": f"Key{k}" for k in range(4, 10)}
}

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
    **{f"Key{k}": [f"Key{k2}" for k2 in range(4, 10) if k2 != k] for k in range(4, 10)}
}
