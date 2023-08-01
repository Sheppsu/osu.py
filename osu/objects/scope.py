class Scope:
    """
    Scope object for telling the program what scopes you are using

    **Valid scopes**

    public
        Allows reading of publicly available data on behalf of the user.
    identify (default)
        Allows reading of the public profile of the user (/me).
    friends.read
        Allows reading of the user's friend list.
    forum.write
        Allows creating and editing forum posts on a user's behalf.
    delegate
        Allows acting as the owner of a client; only available for Client Credentials Grant.
    chat.write
        Allows sending chat messages on a user's behalf.
    """

    __slots__ = ("scopes", "scopes_list")
    valid_scopes = [
        "chat.write",
        "delegate",
        "forum.write",
        "friends.read",
        "identify",
        "public",
    ]

    def __init__(self, *scopes):
        for scope in scopes:
            if scope not in self.valid_scopes and scope != "*":
                raise NameError(
                    f"{scope} is not a valid scope. The valid scopes consist of " f"{','.join(self.valid_scopes)}"
                )
        self.scopes = " ".join(scopes)
        self.scopes_list = list(scopes)

    @classmethod
    def default(cls):
        return cls("public")

    @classmethod
    def identify(cls):
        return cls("public", "identify")

    def __iter__(self):
        return iter(self.scopes_list)

    def __len__(self):
        return len(self.scopes_list)

    def __str__(self):
        return str(self.scopes_list)

    def __contains__(self, scope: str):
        return scope in self.scopes_list or "*" in self.scopes_list
