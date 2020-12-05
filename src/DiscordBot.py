import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import DBHandler

load_dotenv()

class DiscordBot:
    def __init__(self):
        pass

    #Logs in and connects the bot to discord
    def connect(self):
        self._TOKEN = os.getenv('TOKEN')
        self._bot = commands.Bot(command_prefix='a71 ')

        #changing the language to italian (doesn't work)
        #self._bot.ClientUser.edit_settings(locale='it')

        self._database = DBHandler.DBHandler()

        self._load_commands()
        self._bot.run(self._TOKEN)

        return


    def _load_commands(self):
        self._bot.remove_command('help')

        @self._bot.event
        async def on_ready():
            print('Il bot è connesso su discord')

        @self._bot.command(name='esisti?')
        async def crisi_esistenziale(ctx):
            await ctx.send("sì, ed è tutta colpa tua")

        @self._bot.command(name='frammenti')
        async def points_add(ctx, what, user, amount):
            entry = self._database.getEntry("userdata", "user", f"'{user}'")
            user = ctx.guild.get_member(entry[1].replace())
            print(entry)
            print(user)
            #if entry is None:
            #    self._database.addEntry("userdata", ["user"])

            self._database.changeEntry("userdata", "id", getattr(entry, "id"), "frammenti", int(getattr(entry, "frammenti"))+int(amount))
            await ctx.send(getattr(entry, "frammenti"))
