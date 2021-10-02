import discord
import discord_slash as interactions
import json
import dinteractions_Paginator as paginator
from discord_slash import cog_ext
from discord.ext import commands

class Promo(commands.Cog):
    """Commands that promote Server Eggs' partners."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./ServerEggs/EggsBot/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)

    @cog_ext.cog_slash(name="featured", description="Promo - Featured Servers that use Server Eggs.")
    async def featured(self, ctx: interactions.SlashContext):
        e1 = discord.Embed(title="Featured Servers", description="Featured Servers that use Server Eggs.")
        e2 = discord.Embed(title="Phoenix Community", description="Do you like gaming, especially GTA and Minecraft? Do you like having fun and making friends? If yes, Phoenix Community is for you!\nTalk about your favourite game, and do a little trolling in the #memes-n-shitposting channel.\nThe server has a custom \"Phoenix\" Bot written in Python (like Server Eggs!), which lets you add roles to yourself, jokingly \"kill\" other members, \"scan\" fake barcodes made of `I`s and `l`s, and more!")

        embeds = [e1, e2]

        for embed in embeds:
            embed.color = int(self.embed["color"], 16)
            embed.set_author(name=self.embed["author"] + "Promo", icon_url=self.embed["icon"])
            embed.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        await paginator.Paginator(self.bot, ctx, embeds)

    @cog_ext.cog_slash(name="hexacode", description="Promo - Need more Bot power? Check out HexaCode's full portfolio!")
    async def hexacode(self, ctx: interactions.SlashContext):
        e1 = discord.Embed(title="HexaCode", description="Check out HexaCode's Bots!")

        e2 = discord.Embed(title="mkbot", description="Can't code, but want a custom Bot anyway? With mkbot, you can create your own Bot for free (with a Premium version that gives additional features)!")
        e2.add_field(name="Invite", value="Coming soon!", inline=False)
        e2.add_field(name="Website", value="Coming soon!", inline=False)

        e3 = discord.Embed(title="XYZ", description="Need a powerful moderation Bot, that can do everything you've ever wished for? XYZ is what you need!")
        e3.add_field(name="Invite", value="Coming soon... er or later.", inline=False)
        e3.add_field(name="Website", value="Coming soon!", inline=False)

        e4 = discord.Embed(title="ChatRelay", description="Do you know [Hiven](https://hiven.io)? If you want to help your Discord friends move there, just set up the Bot and the Hiven chat will be relayed to Discord (and vice-versa)!")
        e4.add_field(name="Invite", value="Coming a week after mkbot!", inline=False)
        e4.add_field(name="Website", value="Coming soon!", inline=False)

        embeds = [e1, e2, e3, e4]

        for embed in embeds:
            embed.color = int(self.embed["color"], 16)
            embed.set_author(name=self.embed["author"] + "Promo", icon_url=self.embed["icon"])
            embed.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        await paginator.Paginator(self.bot, ctx, embeds)

def setup(bot: commands.Bot):
    bot.add_cog(Promo(bot))