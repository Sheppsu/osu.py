from osu import AsynchronousClient
import os
import websockets
import asyncio
from dotenv import load_dotenv

load_dotenv()


#  Simple Twitch Bot class
class Bot:
    username = "sheppsubot"
    oauth = os.getenv("TWITCH_OAUTH")
    uri = "ws://irc-ws.chat.twitch.tv:80"

    def __init__(self):
        self.ws = None
        self.running = False
        self.loop = asyncio.get_event_loop()

        self.commands = {
            'top': self.top_play
        }

        client_id = int(os.getenv('osu_client_id'))
        client_secret = os.getenv('osu_client_secret')
        redirect_url = "http://127.0.0.1:8080"
        self.client = AsynchronousClient.from_client_credentials(client_id, client_secret, redirect_url)

    # Fundamental

    async def start(self):
        async with websockets.connect(self.uri) as ws:
            self.ws = ws
            self.running = True

            try:
                await self.connect()
                future1 = asyncio.run_coroutine_threadsafe(self.poll(), self.loop)
                await asyncio.sleep(5)
                await self.run()

                while self.running:
                    await asyncio.sleep(1)

                    if future1.done():
                        print(future1.result())

            except KeyboardInterrupt:
                self.running = False
            except websockets.exceptions.ConnectionClosedError:
                await asyncio.sleep(2)
                await self.start()

    async def run(self):
        await self.join(self.username)

    async def connect(self):
        await self.ws.send(f"PASS {self.oauth}")
        print(f"< PASS {self.oauth}", )
        await self.ws.send(f"NICK {self.username}")
        print(f"< NICK {self.username}")

    async def poll(self):
        while self.running:
            data = await self.ws.recv()
            print(f"> {data}")

            if data.startswith("PING"):
                await self.ws.send("PONG :tmi.twitch.tv")
                continue

            data = data.split()
            source = data[0]
            command = data[1]
            channel = data[2][1:]
            content = " ".join(data[3:])[1:]

            if command == "PRIVMSG":
                user = source.split("!")[0][1:]
                await self.on_message(user, channel, content)

    async def join(self, channel):
        await self.ws.send(f"JOIN #{channel}")
        print(f"< JOIN #{channel}")

    async def part(self, channel):
        await self.ws.send(f"PART #{channel}\r\n")
        print(f"< PART #{channel}\r\n")

    async def send_message(self, channel, message):
        await self.ws.send(f"PRIVMSG #{channel} :/me {message}")
        print(f"< PRIVMSG #{channel} :{message}")

    # Events

    async def on_message(self, user, channel, message):
        if message.startswith("!"):
            command = message.split()[0].lower().replace("!", "")
            args = message.split()[1:]
            if command in self.commands:
                await self.commands[command](user, channel, args)

    # Commands

    async def top_play(self, user, channel, args):
        user_id = 14895608
        mode = 'osu'
        score = (await self.client.get_user_scores(user_id, 'best', mode=mode, limit=1))[0]
        await self.send_message(channel, f"@{user} {score.pp}pp - https://osu.ppy.sh/b/{score.beatmap.id}")


bot = Bot()
bot.loop.run_until_complete(bot.start())
