from discord.ext import commands

from DBHandler import DBHandler
from RPGFunctionality.Player import Player


class RPGCommands(commands.Cog):
    def __init__(self):
        database = DBHandler()

    @commands.command(name="inventory", aliases=["inventario"],
                  help="visualizza e interagisci con il tuo inventario")
    async def inventory_manager(self, ctx, subj, n_obj: int = None):
        pRequester = Player(ctx.author.id)

        if subj == "show" or subj == "mostra":
            if n_obj is not None:
                await ctx.send(pRequester.getItem(n_obj))
            else:
                await ctx.send(pRequester.getInv())
