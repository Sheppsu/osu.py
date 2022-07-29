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
