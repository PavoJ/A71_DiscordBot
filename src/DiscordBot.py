import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

# database management
import DBHandler

# command sets
from commands import EventCommands, CurrencyCommands

load_dotenv()


class DiscordBot:
    def __init__(self):
        self._TOKEN = None
        self._bot = None
        self._database = None

        self.reactionSetup = None

    def getBot(self):
        return self._bot

    def getDB(self):
        return self._database

    # Logs in and connects the bot to discord
    def connect(self):
        # grabbing the token from the environment variables
        self._TOKEN = os.getenv('TOKEN')
        # adding all the intents
        intents = discord.Intents.all()
        # setting up the bot
        self._bot = commands.Bot(command_prefix='a71 ', intents=intents)

        # changing the language to italian (doesn't work)
        # self._bot.ClientUser.edit_settings(locale='it')

        self._database = DBHandler.DBHandler()

        self._load_commands()
        self._bot.run(self._TOKEN)

        return

    def _load_commands(self):
        # self._bot.remove_command('help')
        CurrencyCommands.load(self)
        EventCommands.load(self)

        @self._bot.event
        async def on_ready():
            print('Il bot è connesso su discord')
