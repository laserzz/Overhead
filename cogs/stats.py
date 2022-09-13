import discord
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def stats(self, ctx):
        em = discord.Embed(title="Bot Stats", description="Various Bot Stats", color=discord.Color.embed_background(theme="dark"))
        em.add_field(name="Server Count", value=f"{len(self.bot.guilds)}")
        em.add_field(name="Bot Owner", value=f"{self.bot.get_user(941778098674892851)}")
        em.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms")
        em.set_thumbnail(url=self.bot.user.avatar.url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.respond(embed=em)

def setup(bot):
    bot.add_cog(Stats(bot))