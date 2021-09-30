import discord
import discord_slash as interactions
import json
import asyncpg
import aiohttp
from discord_slash import cog_ext
from discord.ext import commands

class Developer(commands.Cog):
    "Developer-only stuff."

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./token.json") as tokenfile:
            self.token = json.load(tokenfile)
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)

    async def pgexecute(self, sql: str, stuff: str=None):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["eggs"])
        if stuff is None:
            await db.execute(f'''{sql}''')
        else:
            await db.execute(f'''{sql}''', stuff)

    async def pgselect(self, query: str):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["eggs"])
        return await db.fetchrow(f'''{query}''')

    @cog_ext.cog_subcommand(base="db", subcommand_group="table", name="create", description="Developer - Creates a table in the SEggsAPI DB.", base_default_permission=False, base_permissions={
        832594030264975420: [
            interactions.utils.manage_commands.create_permission(450678229192278036, interactions.model.SlashCommandPermissionType.USER, True)
        ],
        838718002412912661: [
            interactions.utils.manage_commands.create_permission(450678229192278036, interactions.model.SlashCommandPermissionType.USER, True)
        ]
    })
    async def dbtablecreate(self, ctx: interactions.SlashContext, name: str, stuff: str):
        await self.pgexecute(f"CREATE TABLE {name} ({stuff})")
        await ctx.send("Done.", hidden=True)

    @cog_ext.cog_subcommand(base="post", name="create", description="Developer - Makes a Blog post.", base_default_permission=False, base_permissions={
        832594030264975420: [
            interactions.utils.manage_commands.create_permission(450678229192278036, interactions.model.SlashCommandPermissionType.USER, True)
        ],
        838718002412912661: [
            interactions.utils.manage_commands.create_permission(450678229192278036, interactions.model.SlashCommandPermissionType.USER, True)
        ]
    })
    async def postcreate(self, ctx: interactions.SlashContext, pid: str, title: str, jsx: str):
        async with aiohttp.ClientSession(headers={"auth": self.token["eggs"]}) as session:
            await session.post("https://seggs.tk/api/posts", json={
                "id": pid,
                "title": title,
                "jsx": jsx
            })
        
        await ctx.send("Done.", hidden=True)

    @cog_ext.cog_subcommand(base="post", name="delete", description="Developer - Removes a Blog post.", base_default_permission=False, base_permissions={
        832594030264975420: [
            interactions.utils.manage_commands.create_permission(450678229192278036, interactions.model.SlashCommandPermissionType.USER, True)
        ],
        838718002412912661: [
            interactions.utils.manage_commands.create_permission(450678229192278036, interactions.model.SlashCommandPermissionType.USER, True)
        ]
    })
    async def postdelete(self, ctx: interactions.SlashContext, pid: str):
        async with aiohttp.ClientSession(headers={"auth": self.token["eggs"]}) as session:
            await session.delete(f"https://seggs.tk/api/posts/{pid}")
 
        await ctx.send("Done.", hidden=True)

def setup(bot: commands.Bot):
    bot.add_cog(Developer(bot))