import discord
from discord.ext import commands

from RPGFunctionality.Player import Player


class RPGCommands(commands.Cog):
    def __init__(self):
        self.invList = list()

    @commands.command(name="inventory", aliases=["inventario"],
                  help="visualizza e interagisci con il tuo inventario")
    async def inventory_manager(self, ctx, subj, n_obj: int = None):
        pRequester = Player(ctx.author.id)

        if subj == "show" or subj == "mostra":
            if n_obj is not None:
                await ctx.send(pRequester.getItem(n_obj))
            else:
                message = await ctx.send(pRequester.getInvPage(0))

                if len(pRequester.inventory) != 0:
                    await message.add_reaction('⬅')
                    await message.add_reaction('➡')

                    invreq = {"requester": {"user": ctx.author, "player": pRequester}, "message": message, "invPage": 0}

                    # to prevent memory leaks
                    if len(self.invList) > 100:
                        self.invList = list()
                    self.invList.append(invreq)

    # for scrolling through inventory pages
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        eligible = False
        request = None

        for r in self.invList:
            if reaction.message.id == r["message"].id and user.id == r["requester"]["user"].id:
                request = r
                pRequester = request["requester"]["player"]

                if reaction.emoji == '⬅':
                    try:
                        await reaction.remove(user)
                    except discord.DiscordException as e:
                        print(f"error: {e}")

                    if request["invPage"] > 0:
                        request["invPage"] = request["invPage"]-1
                        eligible = True

                elif reaction.emoji == '➡':
                    try:
                        await reaction.remove(user)
                    except discord.DiscordException as e:
                        print(f"error: {e}")

                    if len(pRequester.inventory)//pRequester.pagelen+1 > request["invPage"]+1:
                        request["invPage"] = request["invPage"]+1
                        eligible = True
            if eligible:
                break

        if eligible:
            page = request["requester"]["player"].getInvPage(request["invPage"])
            print(page)
            await request["message"].edit(content=page)

        return
