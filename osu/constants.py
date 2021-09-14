base_url = "https://osu.ppy.sh/api/v2/"
auth_url = "https://osu.ppy.sh/oauth/authorize/"
token_url = "https://osu.ppy.sh/oauth/token/"

int_to_status = {
    -2: 'graveyard',
    -1: 'wip',
    0: 'pending',
    1: 'ranked',
    2: 'approved',
    3: 'qualified',
    4: 'loved',
}
