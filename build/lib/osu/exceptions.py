class ScopeError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f"ScopeError: {self.error}"
