import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        channel = self.bot.get_channel(994731835261210634)
        embed = discord.Embed(title="Error", description=f"```{error}```", color=discord.Color.embed_background(theme="dark"))
        embed2 = discord.Embed(title="Error", description=f"The developers are aware of this error. Please wait a few hours before using this command again.", color=discord.Color.embed_background(theme="dark"))
        await ctx.respond(embed=embed2)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
