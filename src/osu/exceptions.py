class ScopeException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class ClientException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error
