import os
from dotenv import load_dotenv
load_dotenv()


# checks if the given user has an administrative role (admin or founder role)
def has_perms(func):
    async def wrapper(ctx, *args):
        is_authorized = False
        roles = ctx.author.roles

        for i in range(len(roles)):
            if roles[i].id == int(os.getenv("SERVERADMINROLE")) or \
                    roles[i].id == int(os.getenv("SERVERFOUNDERROLE")):
                is_authorized = True

        if is_authorized:
            await func(ctx, *args)
        else:
            await ctx.send("non hai i permessi per eseguire questo comando.")

    return wrapper
