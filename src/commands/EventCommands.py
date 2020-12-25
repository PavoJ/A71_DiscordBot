from commands import permscheck
from commands import CurrencyCommands


def load(bot):
    dbot = bot.getBot()
    database = bot.getDB()

    @dbot.command(name="event")
    async def event_manager(ctx, subj, what=None):
        if subj == "reset":
            await event_reset(ctx)
        elif subj == "reaction" and what == "add":
            await reaction_set(ctx, ctx.message.author.id)
        elif subj == "reaction" and what == "remove":
            pass

    # resetting an event

    @permscheck.has_perms
    async def event_reset(ctx):
        for member in database.getTable("userdata"):
            if member.valuta_evento != 0:
                database.changeEntry("userdata", "userID", member.userID,
                                     "frammenti", member.frammenti + member.valuta_evento)
                database.changeEntry("userdata", "userID", member.userID,
                                     "valuta_evento", 0)

        await ctx.send("L'evento è stato resettato")

    # adding or removing reaction events

    @dbot.event
    async def on_raw_reaction_add(p):
        if bot.reactionSetup is not None and bot.reactionSetup["userid"] == p.user_id:
            database.addEntry(
                "reaction_messages",
                ["messageID", "createdBy", "channelID", "emojiID"],
                [p.message_id, p.user_id, p.channel_id, p.emoji.id]
            )

            msgctx = bot.reactionSetup["ctx"]
            bot.reactionSetup = None
            await msgctx.send("reazione aggiunta")

        # se un utente ha reagito su un messaggio presente nel database appostito
        elif database.getEntry("reaction_messages", messageID=p.message_id, emojiID=p.emoji.id) is not None:
            # controllo se ha già reagito prima d'ora
            if database.getEntry("member_reactions", messageID=p.message_id) is None:
                database.addEntry(
                    "member_reactions",
                    ["messageID", "userID", "reactionID"],
                    [p.message_id, p.user_id, p.emoji.id]
                )
                player_entry = database.getEntry("userdata", userID=p.user_id)
                if player_entry is None:
                    player_entry = database.addEntry("userdata", ["userID"], [p.user_id])

                database.changeEntry(
                    "userdata",
                    "userID", p.user_id,
                    "valuta_evento", player_entry.valuta_evento+1)

    async def reaction_set(ctx, userid):
        bot.reactionSetup = {
            "ctx": ctx,
            "userid": userid
        }
        await ctx.send("reagisci al messaggio")

    def reaction_mod():
        pass
