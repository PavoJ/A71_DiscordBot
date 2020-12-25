from commands import permscheck

#pcommands = None

def load(bot):
    dbot = bot.getBot()
    database = bot.getDB()

    @dbot.command(name='event_currency')
    async def event_currency(ctx, what, amount: int = None, *users):
        await points_commands(ctx, "valuta_evento", what, users, amount)

    @dbot.command(name="fragments")
    async def fragment_currency(ctx, what, amount: int = None, *users):
        await points_commands(ctx, "frammenti", what, users, amount)

    async def points_commands(ctx, currency, what, users, amount: int):
        if what == "show":
            await points_show(ctx, users, currency)

        elif (what == "add" or what == "remove") and (amount is not None) and len(users) > 0:
            if what == "remove":
                amount = -amount

            await points_mod(ctx, currency, users, amount)

        else:  # wrong usage
            # await ctx.send("Utilizzo del comando improprio.")
            await ctx.send(f"{users}, {amount}")

    # shows the points a user currently has
    async def points_show(ctx, user, currency):
        errorHappened = False

        if len(user) > 1:
            await ctx.send("l'utente da visualizzare può essere solo uno")
        elif len(user) == 0:
            user = ctx.author.id
            member = ctx.guild.get_member(user)
        else:
            try:
                user = int(user[0][3:-1])
                member = ctx.guild.get_member(user)
            except ValueError:
                errorHappened = True

        if member is None or errorHappened:
            await ctx.send("L'utente non è in questo server o non esiste")

        entry = database.getEntry("userdata", userID=user)
        if entry is None:
            entry = database.addEntry("userdata", ["userID"], [user])

        await ctx.send(f"{member.mention} ha {getattr(entry, currency)} {currency}")

    # adds or removes a type of currency from a specified user
    @permscheck.has_perms
    async def points_mod(ctx, currency, users, amount):
        for user in users:
            user = int(user[3:-1])

            entry = database.getEntry("userdata", userID=user)
            member = ctx.guild.get_member(user)

            if entry is None and member is not None:
               entry = database.addEntry("userdata", ["userID", currency], [user, amount])
            else:
               database.changeEntry(
                   "userdata",
                   "userID", entry.userID,
                   currency, int(getattr(entry, currency)) + amount)

        await ctx.send("comando eseguito con successo")