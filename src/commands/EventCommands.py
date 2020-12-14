from commands import permscheck


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
                    ["messageID", "createdBy", "channelID", "emojiName"],
                    [p.message_id, p.user_id, p.channel_id, p.emoji.name]
                )
                
                msgctx = bot.reactionSetup["ctx"]
                bot.reactionSetup = None
                await msgctx.send("reazione aggiunta")
        #elif database.getEntry("member_reactions", p.)

    async def reaction_set(ctx, userid):
        bot.reactionSetup = {
            "ctx": ctx,
            "userid": userid
        }
        await ctx.send("reagisci al messaggio")

    def reaction_mod():
        pass
