import discord
import json
import discord_slash as interactions
from datetime import datetime
from discord_slash import cog_ext
from discord.ext import commands

class Utility(commands.Cog):
    """Utility Commands for Server Eggs."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./ServerEggs/EggsBot/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.launch_time = datetime.utcnow()

    @cog_ext.cog_slash(name="ping", description="Utility - Gets the Bot's Ping Latency.")
    async def ping(self, ctx: interactions.SlashContext):
        ping = round(self.bot.latency * 1000, 1)

        e = discord.Embed(title="Ping Latency", color=int(self.embed["color"], 16), description=f"My Ping Latency is {ping}ms.")
        e.set_author(name=self.embed["author"] + "Utility", icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)

    @cog_ext.cog_slash(name="uptime", description="Utility - Gets the Bot's Uptime.")
    async def uptime(self, ctx: interactions.SlashContext):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        e = discord.Embed(title="Uptime", color=int(self.embed["color"], 16), description=f"The Bot has been online for:\n{days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")
        e.set_author(name=self.embed["author"] + "Utility", icon_url=self.embed["icon"])
        e.add_field(name="Last Restart", value="The Bot was last restarted on {} UTC".format(self.bot.launch_time.strftime("%A, %d %B %Y at %H:%M")), inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)

def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))