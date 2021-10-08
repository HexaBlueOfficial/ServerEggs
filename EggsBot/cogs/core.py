import discord
import discord_slash as interactions
import json
import random
import platform
import aiohttp
from discord_slash import cog_ext
from discord.ext import commands, tasks

class Core(commands.Cog):
    """Core Slash Commands for the Server Eggs Bot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.presence.start()
        with open("./ServerEggs/EggsBot/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)

    @tasks.loop(seconds=400.0)
    async def presence(self):
        presences = {"playing": ["with Eggs", "with you", "around"], "watching": ["Eggs", "more Eggs", "a lot of Eggs", "way too many Eggs", "https://eggs.hexa.blue/", "https://hexa.blue/", "https://discord.gg/DsARcGwwdM"]}
        playorwatch = random.randint(1, 2)
        if playorwatch == 1:
            presencetouse = random.randint(0, 2)
            await self.bot.change_presence(activity=discord.Game(name=presences["playing"][presencetouse]))
        else:
            presencetouse = random.randint(0, 3)
            await self.bot.change_presence(activity=discord.Activity(name=presences["watching"][presencetouse], type=discord.ActivityType.watching))

    @presence.before_loop
    async def before_presence(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await guild.me.edit(nick="Eggs")

    @cog_ext.cog_subcommand(base="info", name="bot", description="Core - Gets information about the Bot.")
    async def infobot(self, ctx: interactions.SlashContext):
        e = discord.Embed(title="About Server Eggs", color=int(self.embed["color"], 16), description="**Server Eggs** is a Discord **Bot** that... we don't know how to describe either.")
        e.set_author(name=self.embed["author"] + "Core", icon_url=self.embed["icon"])
        e.set_thumbnail(url=self.embed["icon"])
        e.add_field(name="Developers", value="<@450678229192278036> (Flamey#0075)")
        e.add_field(name="Stats", value=f"**Servers:** {len(self.bot.guilds)}\n**Users:** {len(self.bot.users)}")
        e.add_field(name="Versions", value=f"**Server Eggs:** v{self.bot.version}\n**Python:** v{platform.python_version()}\n**discord-py-interactions:** v{interactions.__version__}", inline=False)
        e.add_field(name="Credits", value="**Hosting:** [Library of Code](https://loc.sh/discord)", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        components = [
            interactions.utils.manage_components.create_actionrow(
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "Invite", None, None, "https://discord.com/api/oauth2/authorize?client_id=886686500845138041&permissions=274945361920&scope=bot%20applications.commands"),
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "Website", None, None, "https://eggs.hexa.blue/"),
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "Docs", None, None, "https://eggs.hexa.blue/docs"),
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "Support", None, None, "https://discord.gg/DsARcGwwdM")
            )
        ]
        await ctx.send(embed=e, components=components)

    @cog_ext.cog_subcommand(base="info", name="api", description="Core - Gets information about the SEggs API.")
    async def infoapi(self, ctx: interactions.SlashContext):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://eggsapi.xyz/api") as response:
                response = await response.json()
                version = response["version"]
                eggs = response["stats"]["eggs"]
                posts = response["stats"]["blogposts"]

        e = discord.Embed(title="About the EggsAPI", color=int(self.embed["color"], 16), description="The **Eggs API** gives you **e g g s**, and it is powered by this Bot.")
        e.set_author(name=self.embed["author"] + "Core", icon_url=self.embed["icon"])
        e.set_thumbnail(url=self.embed["icon"])
        e.add_field(name="Developers", value="<@450678229192278036> (Flamey#0075)")
        e.add_field(name="Stats", value=f"**Eggs Uploaded:** {eggs}\n**Blog Posts:** {posts}")
        e.add_field(name="Versions", value=f"**EggsAPI:** v{version}\n**Node.js:** v14\n**Next.js:** v11.1.2", inline=False)
        e.add_field(name="Credits", value="**Hosting:** [Vercel](https://vercel.com)", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        await ctx.send(embed=e)

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))