import discord
import discord_slash as interactions
import json
import asyncpg
import aiohttp
import dinteractions_Paginator as paginator
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
        with open("./ServerEggs/EggsBot/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
    
    @cog_ext.cog_slash(name="guilds", description="Developer - Gets info about all the Guilds the Bot is in.", guild_ids=[832594030264975420, 838718002412912661])
    @commands.is_owner()
    async def guilds(self, ctx: interactions.SlashContext):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://eggsapi.xyz/api/eggs") as response:
                response = await response.json()
                eggs: list = response

        embeds = []
        guilds = []

        index = 0
        for guild in self.bot.guilds:
            guilds.append(guild)
            if index == 0:
                continue
            if isinstance(index / 4, int):
                e = discord.Embed(title=f"Guilds {index / 4}", color=self.embed["color"])
                e.set_author(name=self.embed["author"] + "Developer", icon_url=self.embed["icon"])
                guildeggs = 0
                for guildx in guilds:
                    for egg in eggs:
                        if egg["guild"] == str(guildx.id):
                            guildeggs += 1
                    e.add_field(name=guildx.name, value=f"**ID:** {guildx.id}\n**Owner:** {str(guildx.owner)} (`{guildx.owner.id}`)\n**Eggs:** {guildeggs}")
                e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                embeds.append(e)
                guilds = []
        
        await paginator.Paginator(self.bot, ctx, embeds)

def setup(bot: commands.Bot):
    bot.add_cog(Developer(bot))