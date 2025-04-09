from osu import AsynchronousClient


def as_async(client) -> AsynchronousClient:
    def update(auth):
        # update auth object on the sync client
        sync_refresh_callback = client.auth._refresh_callback
        updated_auth = auth.as_sync()
        # keep its refresh callback
        updated_auth.set_refresh_callback(sync_refresh_callback)
        client.auth = updated_auth
        # since the auth data was just updated
        if sync_refresh_callback is not None:
            sync_refresh_callback(client.auth)

    auth = client.auth.as_async()
    auth.set_refresh_callback(update)
    return AsynchronousClient(auth)
