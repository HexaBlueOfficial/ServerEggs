import discord
import discord_slash as interactions
import json
import random
import platform
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
        presences = {"playing": ["with Eggs", "with you", "around"], "watching": ["Eggs", "more Eggs", "a lot of Eggs", "way too many Eggs"]}
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
    
    @cog_ext.cog_slash(name="info", description="Core - Gets information about the Bot.")
    async def info(self, ctx: interactions.SlashContext):
        e = discord.Embed(title="About Server Eggs", color=int(self.embed["color"], 16), description="**Server Eggs** is a Discord **Bot** that... we don't know how to describe either.")
        e.set_author(name=self.embed["author"] + "Core", icon_url=self.embed["icon"])
        e.set_thumbnail(url=self.embed["icon"])
        e.add_field(name="Developers", value="**<@450678229192278036> (Flamey):** All Slash Commands.", inline=False)
        e.add_field(name="Versions", value=f"**Server Eggs:** v1.0.0\n**Python:** v{platform.python_version()}\n**discord-py-interactions:** v{interactions.__version__}", inline=False)
        e.add_field(name="Credits", value="**Hosting:** [Library of Code](https://loc.sh/discord)", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        components = [
            interactions.utils.manage_components.create_actionrow(
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "Invite", None, None, "https://discord.com/api/oauth2/authorize?client_id=886686500845138041&permissions=274945361920&scope=bot%20applications.commands"),
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "Support", None, None, "https://discord.gg/DsARcGwwdM")
            )
        ]
        await ctx.send(embed=e, components=components)

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))