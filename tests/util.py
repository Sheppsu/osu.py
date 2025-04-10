from osu import AsynchronousClient


def as_async(client) -> AsynchronousClient:
    return AsynchronousClient(client.auth.as_async())
