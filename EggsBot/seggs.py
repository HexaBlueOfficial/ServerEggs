import discord
import discord_slash as interactions
import json
import typing
from discord.ext import commands

with open("./token.json") as tokenfile:
    token = json.load(tokenfile)
with open("./ServerEggs/EggsBot/assets/embed.json") as embedfile:
    embed = json.load(embedfile)

bot = commands.Bot(command_prefix=commands.when_mentioned, help_command=None, intents=discord.Intents.all())
slash = interactions.SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

bot.version = "2.0.0a"

@bot.event
async def on_ready():
    channel = bot.get_channel(832677639944667186)
    await channel.send(f"**Server Eggs** is ready and running on **discord-py-interactions v{interactions.__version__}!**")

@bot.event
async def on_slash_command_error(ctx: typing.Union[interactions.SlashContext, interactions.MenuContext], ex):
    e = discord.Embed(title="An Error Occurred", color=int(embed["color"], 16), description=f"{ex}")
    e.set_author(name=embed["author"] + "Main", icon_url=embed["icon"])
    e.set_footer(text=embed["footer"], icon_url=embed["icon"])
    await ctx.send(embed=e, hidden=True)

    raise ex

extensions = ["cogs.core", "cogs.developer", "cogs.eggs", "cogs.utility"]
for extension in extensions:
    bot.load_extension(extension)

bot.run(token["eggsbeta"])