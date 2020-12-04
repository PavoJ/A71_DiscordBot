import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

class DiscordBot:
    def __init__(self):
        pass

    #Logs in and connects the bot to discord
    def connect(self):
        self._TOKEN = os.getenv('TOKEN')
        self._bot = commands.Bot(command_prefix='a71 ')

        #changing the language to italian
        #self._bot.ClientUser.edit_settings(locale='it')

        self._load_commands()
        self._bot.run(self._TOKEN)


    def _load_commands(self):
        self._bot.remove_command('help')

        @self._bot.event
        async def on_ready():
            print('Il bot è connesso su discord')

        @self._bot.command(name='esisti?')
        async def crisi_esistenziale(ctx):
            await ctx.send("sì, ed è tutta colpa tua")
