from commands import permscheck


def load(bot):
    dbot = bot.getBot()
    database = bot.getDB()

    #todo migliorare il codice della traduzione
    @dbot.command(name='event_currency', aliases=['valuta_evento'])
    async def event_currency(ctx, what, amount = None, *users):
        await points_commands(ctx, "valuta_evento", what, users, amount)

    @dbot.command(name='shards', aliases=['frammenti'])
    async def fragment_currency(ctx, what, amount = None, *users):
        await points_commands(ctx, "frammenti", what, users, amount)

    async def points_commands(ctx, currency, what, users, amount):
        if what == "show" or what == "mostra":
            await points_show(ctx, amount, currency)
        else:
            amount = int(amount)

            if ((what == "add" or what == "aggiungi") or (what == "remove" or what == "rimuovi")) and \
                    (amount is not None) and len(users) > 0:
                if what == "remove" or what == "rimuovi":
                    amount = -amount

                await points_mod(ctx, currency, users, amount)

            else:  # wrong usage
                # await ctx.send("Utilizzo del comando improprio.")
                await ctx.send(f"{users}, {amount}")

    # shows the points a user currently has
    async def points_show(ctx, user, currency):
        errorHappened = False

        member = None

        if user is None:
            user = ctx.author.id
            member = ctx.guild.get_member(user)
        else:
            try:
                user = int(user[3:-1])
                member = ctx.guild.get_member(user)
            except ValueError:
                errorHappened = True

        if member is None or errorHappened:
            await ctx.send("L'utente non è in questo server o non esiste")
            return

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