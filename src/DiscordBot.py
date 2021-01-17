import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

# database management

# command sets
from commands.EventCommands import EventCommands
from commands.CurrencyCommands import CurrencyCommands
from commands.RPGCommands import RPGCommands


load_dotenv()


class DiscordBot(commands.Bot):
    def __init__(self):
        # grabbing the token from the environment variables
        self._TOKEN = os.getenv('TOKEN')
        # adding all the intents
        intents = discord.Intents.all()

        commands.Bot.__init__(self, command_prefix='a71 ', intents=intents)

    # Logs in and connects the bot to discord
    def dsbotstart(self):
        self._load_commands()

        while True:
            self.run(self._TOKEN)
            print("bot crashed")

    def _load_commands(self):
        # self._bot.remove_command('help')
        self.add_cog(CurrencyCommands())
        self.add_cog(EventCommands())
        self.add_cog(RPGCommands())

        @self.event
        async def on_ready():
            print('Il bot è connesso su discord')
