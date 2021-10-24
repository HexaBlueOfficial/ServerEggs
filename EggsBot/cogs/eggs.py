
import discord
import discord_slash as interactions
import json
import aiohttp
from discord_slash import cog_ext
from discord.ext import commands

class Eggs(commands.Cog):
    """egg"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.slash: interactions.SlashCommand = self.bot.slash
        with open("./token.json") as tokenfile:
            self.token = json.load(tokenfile)
        with open("./ServerEggs/EggsBot/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)

    async def template(self, ectx: interactions.SlashContext, name: str, author: discord.User, guild: discord.Guild, botver: str, picture: str, desc: str=None):
        if desc is None:
            for key, value in self.slash.commands.items():
                if key == name:
                    desc: str = value.description
                    description = desc.lstrip("Eggs - ")

                    e = discord.Embed(title=f"The \"{name}\" Egg", color=int(self.embed["color"], 16), description=f"**Uploaded by `{str(author)} ({author.id})` from `{guild.name}` on SEggs v{botver}.**\n\"{description}\"")
                    e.set_author(name=self.embed["author"] + "Eggs", icon_url=self.embed["icon"])
                    e.set_image(url=picture)
                    e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                    await ectx.send(embed=e)
                    break

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://eggsapi.xyz/api/eggs") as response:
                eggs: list = await response.json()

        for egg in eggs:
            async def eggcoro(ectx: interactions.SlashContext):
                await self.template(
                    ectx,
                    egg["name"],
                    await self.bot.fetch_user(int(egg["ddata"]["author"])),
                    self.bot.get_guild(int(egg["ddata"]["guild"])),
                    egg["ddata"]["botver"],
                    egg["pic"],
                    egg["desc"]
                )

            description = egg["desc"]
            self.slash.add_slash_command(eggcoro, egg["name"], f"Eggs - {description}", [int(egg["guild"])])

        await self.slash.sync_all_commands()
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://eggsapi.xyz/api/eggs") as response:
                eggs: list = await response.json()
        
                for egg in eggs:
                    if int(egg["ddata"]["guild"]) == guild.id:
                        name = egg["name"]
                        await session.delete(f"https://eggsapi.xyz/api/eggs/{name}")

    @cog_ext.cog_subcommand(base="egg", name="random", description="Eggs - Gets a random Egg from the SEggs API.")
    async def eggrandom(self, ctx: interactions.SlashContext):
        await ctx.defer(hidden=True)

        async with aiohttp.ClientSession() as session:
            async with session.get("https://eggsapi.xyz/api/eggs/random") as response:
                egg = await response.json()
                name = egg["name"]
                author = await self.bot.fetch_user(int(egg["ddata"]["author"]))
                guild = self.bot.get_guild(int(egg["ddata"]["guild"]))
                botver = egg["ddata"]["botver"]
                desc = egg["desc"]
                pic = egg["pic"]

        await self.template(ctx, name, author, guild, botver, pic, desc)

    @cog_ext.cog_subcommand(base="egg", name="create", description="Eggs - Create an Egg on this server!", options=[
        interactions.utils.manage_commands.create_option("name", "The name of the Egg.", 3, True),
        interactions.utils.manage_commands.create_option("description", "A description for the Egg.", 3, True),
        interactions.utils.manage_commands.create_option("picture", "A link to the Egg picture (ex: https://this.is-for.me/i/z1kb.jpg).", 3, True)
    ])
    @commands.has_permissions(manage_guild=True)
    async def eggcreate(self, ctx: interactions.SlashContext, name: str, description: str, picture: str):
        await ctx.defer(hidden=True)

        async with aiohttp.ClientSession(headers={"auth": self.token["eggs"]}) as session:
            await session.post("https://eggsapi.xyz/api/eggs", json={
                "name": name,
                "ddata": {
                    "author": str(ctx.author.id),
                    "guild": str(ctx.guild.id),
                    "botver": self.bot.version
                },
                "desc": description,
                "pic": picture
            })

        async def eggcoro(ectx: interactions.SlashContext):
            await self.template(ectx, name, ctx.author, ctx.guild, self.bot.version, picture)

        self.slash.add_slash_command(eggcoro, name.lower(), f"Eggs - {description}", [ctx.guild.id])
        await self.slash.sync_all_commands()

        await ctx.send("Egg created successfully!", hidden=True)

    @cog_ext.cog_subcommand(base="egg", name="delete", description="Eggs - Delete an Egg from this server.", options=[
        interactions.utils.manage_commands.create_option("name", "The name of the Egg.", 3, True)
    ])
    @commands.has_permissions(manage_guild=True)
    async def eggdelete(self, ctx: interactions.SlashContext, name: str):
        await ctx.defer(hidden=True)

        cmds = await interactions.utils.manage_commands.get_all_commands(self.bot.user.id, self.token["eggs"], ctx.guild.id)
        
        for cmd in cmds:
            if cmd["name"] == name:
                cmdid: str = cmd["id"]
                await interactions.utils.manage_commands.remove_slash_command(self.bot.user.id, self.token["eggs"], ctx.guild.id, cmdid)
                await self.slash.sync_all_commands(delete_from_unused_guilds=True)
                break

        async with aiohttp.ClientSession(headers={"auth": self.token["eggs"]}) as session:
            await session.delete(f"https://eggsapi.xyz/api/eggs/{name}")

        await ctx.send("Egg deleted successfully.", hidden=True)

    # Hardboiled- sorry, I meant hardcoded Eggs.

    @cog_ext.cog_slash(name="seggs", description="Eggs - The original Egg.")
    async def seggs(self, ctx: interactions.SlashContext):
        await self.template(
            ctx,
            "seggs",
            await self.bot.fetch_user(450678229192278036),
            self.bot.get_guild(832594030264975420),
            "2.0.0",
            "https://eggs.hexa.blue/images/seggs.png"
        )

    @cog_ext.cog_slash(name="hardboiled", description="Eggs - Classic hardboiled Eggs.")
    async def hardboiled(self, ctx: interactions.SlashContext):
        await self.template(
            ctx,
            "hardboiled",
            await self.bot.fetch_user(450678229192278036),
            self.bot.get_guild(832594030264975420),
            "2.0.0",
            "https://nomnompaleo.com/wp-content/uploads/2011/07/Perfect-Hard-Boiled-Eggs.jpg"
        )

    @cog_ext.cog_slash(name="softboiled", description="Eggs - Classic softboiled Eggs.")
    async def softboiled(self, ctx: interactions.SlashContext):
        await self.template(
            ctx,
            "softboiled",
            await self.bot.fetch_user(450678229192278036),
            self.bot.get_guild(832594030264975420),
            "2.0.0",
            "https://www.yeprecipes.com/data/thumbnails/15/soft-boiled-egg2.jpg"
        )

    @cog_ext.cog_slash(name="scrambled", description="Eggs - Classic scrambled Eggs.")
    async def scrambled(self, ctx: interactions.SlashContext):
        await self.template(
            ctx,
            "scrambled",
            await self.bot.fetch_user(450678229192278036),
            self.bot.get_guild(832594030264975420),
            "2.0.0",
            "https://southernbite.com/wp-content/uploads/2021/05/Perfect-Scrambled-Eggs-3.jpg"
        )

    @cog_ext.cog_slash(name="fried", description="Eggs - Classic fried Eggs.")
    async def fried(self, ctx: interactions.SlashContext):
        await self.template(
            ctx,
            "fried",
            await self.bot.fetch_user(450678229192278036),
            self.bot.get_guild(832594030264975420),
            "2.0.0",
            "https://www.rainbowcounselling.org.uk/wp-content/uploads/2020/04/fried-eggs-feature.jpg"
        )

def setup(bot: commands.Bot):
    bot.add_cog(Eggs(bot))