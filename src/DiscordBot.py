import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import DBHandler

load_dotenv()


class DiscordBot:
    def __init__(self):
        self._TOKEN = None
        self._bot = None
        self._database = None

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

        # funzioni usate dai comandi del bot

        # checks if the given user has an administrative role
        def has_perms(member):
            ret = False
            print(type(member.roles[0].id))
            for i in range(len(member.roles)):
                if member.roles[i].id == int(os.getenv("SERVERADMINROLE")) or \
                        member.roles[i].id == int(os.getenv("SERVERFOUNDERROLE")):
                    ret = True

            return ret


        @self._bot.event
        async def on_ready():
            print('Il bot è connesso su discord')

        # comando "a71 esisti?". Creato per scopi di testing
        # @self._bot.command(name='esisti?')
        # async def crisi_esistenziale(ctx):
        #     await ctx.send("sì, ed è tutta colpa tua")

        # @self._bot.command(name='frammenti mostra')
        # async def points_show(ctx, what, user):
        #     if what == 'mostra':
        #         entry = self._database.getEntry("userdata", "user", f"'{user}'")
        #         member = ctx.guild.get_member(user)
        #
        #         if entry is None and member is not None:
        #             entry = self._database.addEntry("userdata", ["user"], [user])
        #     if entry is None and member is None:
        #         await ctx.send("l'utente imesso non esiste")
        #     else:
        #         await ctx.send(f"{member.mention} ha {getattr(entry, 'frammenti')} frammenti")

        async def point_mod(currency, ctx, what, user, amount):
            if what == "show":

                if user is None:
                    user = ctx.author.id
                else:
                    try:
                        user = int(user[3:-1])
                    except ValueError:
                        await ctx.send("L'utente non è in questo server o non esiste")

                member = ctx.guild.get_member(user)
                if member is None:
                    await ctx.send("L'utente non è in questo server o non esiste")

                entry = self._database.getEntry("userdata", "userID", user)
                if entry is None:
                    entry = self._database.addEntry("userdata", ["userID"], [user])

                await ctx.send(f"{member.mention} ha {getattr(entry, currency)} {currency}")

            elif (what == "add" or what == "remove") and (user and amount is not None):

                amount = int(amount)
                if what == "remove":
                    amount = -amount

                if has_perms(ctx.author):
                    user = int(user[3:-1])  # User ID

                    entry = self._database.getEntry("userdata", "userID", user)
                    member = ctx.guild.get_member(user)

                    if entry is None and member is not None:
                        entry = self._database.addEntry("userdata", ["userID", currency], [user, amount])

                    else:
                        self._database.changeEntry(
                            "userdata",
                            "userID", getattr(entry, "userID"),
                            currency, int(getattr(entry, currency)) + amount)

                    await ctx.send("comando eseguito con successo")
                else:
                    await ctx.send("non hai i permessi per usare questo comando")

            else:  # wrong usage
                await ctx.send("Utilizzo del comando improprio.")

        @self._bot.command(name='event_currency')
        async def event_currency(ctx, what, user=None, amount=None):
            await point_mod("valuta_evento", ctx, what, user, amount)

        @self._bot.command(name="fragments")
        async def fragment_currency(ctx, what, user=None, amount=None):
            await point_mod("frammenti", ctx, what, user, amount)

        @self._bot.command(name="event")
        async def event_manager(ctx, what):
            if what == "reset":
                for member in self._database.getTable("userdata"):
                    if member.valuta_evento != 0:
                        self._database.changeEntry("userdata", "userID", member.userID,
                            "frammenti", member.frammenti+member.valuta_evento)
                        self._database.changeEntry("userdata", "userID", member.userID,
                            "valuta_evento", 0)

            await ctx.send("L'evento è stato resettato")
