__all__ = ("ScopeException", "RequestException")


class ScopeException(Exception):
    """Raised when there was an exception involving scopes"""


class RequestException(Exception):
    """Raised when there was an exception involving requests to the api"""
