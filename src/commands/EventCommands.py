from discord.ext import commands

from DBHandler import DBHandler
from commands.wrappers import permscheck


class EventCommands(commands.Cog):
    def __init__(self):
        self.database = DBHandler()
        self.reactionSetup = None

    @commands.command(name="event", aliases=["evento"],
                  help="comandi amministrativi per la gestione degli eventi", category="amministrazione")
    async def event_manager(self, ctx, subj, what=None):
        if subj == "reset":
            await self.event_reset(ctx)
        elif subj == "reaction" and what == "add" or subj == "reazione" and what == "aggiungi":
            await self.reaction_set(ctx, ctx.message.author.id)
        elif subj == "reaction" and what == "remove" or subj == "reazione" and what == "rimuovi":
            pass

    # resetting an event (converting each user's event currency to shards)

    @permscheck.has_perms
    async def event_reset(self, ctx):
        for member in self.database.getTable("userdata"):
            if member.valuta_evento != 0:
                self.database.changeEntry("userdata", "userID", member.userID,
                                     "frammenti", member.frammenti + member.valuta_evento)
                self.database.changeEntry("userdata", "userID", member.userID,
                                     "valuta_evento", 0)

        await ctx.send("L'evento è stato resettato")

    async def reaction_set(self, ctx, userid):
        self.reactionSetup = {
            "ctx": ctx,
            "userid": userid
        }
        await ctx.send("reagisci al messaggio")

    # adding or removing reaction events, used as a way to obtain currency

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, p):
        # if an admin is adding a message to the reactable messages
        if self.reactionSetup is not None and self.reactionSetup["userid"] == p.user_id:
            self.database.addEntry(
                "reaction_messages",
                ["messageID", "createdBy", "channelID", "emojiID"],
                [p.message_id, p.user_id, p.channel_id, p.emoji.id]
            )

            msgctx = self.reactionSetup["ctx"]
            self.reactionSetup = None
            await msgctx.send("reazione aggiunta")

        # se un utente ha reagito su un messaggio presente nel database appostito
        elif self.database.getEntry("reaction_messages", messageID=p.message_id, emojiID=p.emoji.id) is not None:
            # controllo se ha già reagito prima d'ora
            if self.database.getEntry("member_reactions", messageID=p.message_id) is None:
                self.database.addEntry(
                    "member_reactions",
                    ["messageID", "userID", "reactionID"],
                    [p.message_id, p.user_id, p.emoji.id]
                )
                player_entry = self.database.getEntry("userdata", userID=p.user_id)
                if player_entry is None:
                    player_entry = self.database.addEntry("userdata", ["userID"], [p.user_id])

                self.database.changeEntry(
                    "userdata",
                    "userID", p.user_id,
                    "valuta_evento", player_entry.valuta_evento+1)
