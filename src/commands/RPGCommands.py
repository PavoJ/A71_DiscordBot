from discord.ext import commands

from DBHandler import DBHandler
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
                await message.add_reaction('⬅')
                await message.add_reaction('➡')

                invreq = {"requester": {"user": ctx.author, "player": pRequester}, "message": message, "invPage": 0}

                # to prevent memory leaks
                if len(self.invList) > 100:
                    self.invList = list()
                self.invList.append(invreq)

    # for scrolling through inventory pages
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, p):
        eligible = False
        request = None

        for r in self.invList:
            if p.message_id == r["message"].id and p.user_id == r["requester"]["user"].id:
                request = r
                pRequester = request["requester"]["player"]
                eligible = True

                if p.emoji.name == '⬅' and request["invPage"] > 0:
                    request["invPage"] = request["invPage"]-1
                elif p.emoji.name == '➡' and len(pRequester.inventory)/pRequester.pagelen > request["invPage"]+1:
                    request["invPage"] = request["invPage"]+1
                else:
                    eligible = False

                break

        if eligible:
            page = request["requester"]["player"].getInvPage(request["invPage"])
            await request["message"].edit(content=page)

        return
