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
    "AT": "Autoplay",
    "SO": "SpunOut",
    "AP": "Relax2",
    "PF": "Perfect",
    "FI": "FadeIn",
    "RD": "Random",
    "CM": "LastMod",
    "TP": "TargetPractice",
    "CP": "Coop",
    "SV2": "ScoreV2",
    "MR": "Mirror",
    "KM": "keyMod",  # Actually not sure about this one
    **{f"{k}K": f"Key{k}" for k in range(1, 10)}
}
