from osu import Client


client = Client()
listing = client.get_changelog_listing()
for stream in listing["streams"]:
    print(f"Stream {stream.display_name} ({stream.id}) - {stream.user_count} users. Latest build: {stream.latest_build.display_version}")
    build = client.get_changelog_build(stream.name, stream.latest_build.version)
    for changelog in build.changelog_entries:
        print(f"{changelog.title}: {changelog.message}")
