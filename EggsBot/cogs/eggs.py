
import discord
import discord_slash as interactions
import json
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

    @cog_ext.cog_subcommand(base="egg", name="random", description="Eggs - Gets a random Egg from the SEggs API.")
    async def eggrandom(self, ctx: interactions.SlashContext):
        await ctx.send("**Coming soon!**")

    @cog_ext.cog_subcommand(base="egg", name="create", description="Eggs - Create an Egg on this server!", options=[
        interactions.utils.manage_commands.create_option("name", "The name of the Egg.", 3, True),
        interactions.utils.manage_commands.create_option("description", "A description for the Egg.", 3, True),
        interactions.utils.manage_commands.create_option("picture", "A link to the Egg picture (ex: https://this.is-for.me/i/z1kb.jpg).", 3, True)
    ])
    @commands.has_permissions(manage_guild=True)
    async def eggcreate(self, ctx: interactions.SlashContext, name: str, description: str, picture: str):
        async def eggcoro(ectx: interactions.SlashContext):
            for key, value in self.slash.commands.items():
                if key == name:
                    desc: str = value.description
                    description = desc.lstrip("Eggs - ")
                    break

            e = discord.Embed(title=f"The \"{name}\" Egg", color=int(self.embed["color"], 16), description=f"**Uploaded by `{str(ctx.author)} ({ctx.author.id})`.**\n\"{description}\"")
            e.set_author(name=self.embed["author"] + "Eggs", icon_url=self.embed["icon"])
            e.set_image(url=picture)
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
            await ectx.send(embed=e)
        
        self.slash.add_slash_command(eggcoro, name.lower(), f"Eggs - {description}", [ctx.guild.id])
        await self.slash.sync_all_commands()

        await ctx.send("Egg created successfully!", hidden=True)

    @cog_ext.cog_subcommand(base="egg", name="delete", description="Eggs - Delete an Egg from this server.", options=[
        interactions.utils.manage_commands.create_option("name", "The name of the Egg.", 3, True)
    ])
    @commands.has_permissions(manage_guild=True)
    async def eggdelete(self, ctx: interactions.SlashContext, name: str):
        for key, value in self.slash.commands.items():
            if key == name:
                cmdid: str = value["id"]
                await interactions.utils.manage_commands.remove_slash_command(self.bot.user.id, self.token["eggs"], ctx.guild.id, cmdid)
                await self.slash.sync_all_commands()
                break

        await ctx.send("Egg deleted successfully.", hidden=True)

def setup(bot: commands.Bot):
    bot.add_cog(Eggs(bot))
