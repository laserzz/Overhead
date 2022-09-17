import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    adcmd = discord.SlashCommandGroup(name="admin", description="admin commands. bot owner only.")

    @adcmd.command(description="leave server")
    @commands.is_owner()
    async def leave(self, ctx, guild_id:str):
        gu = self.bot.get_guild(int(guild_id))
        await ctx.respond(f"left {gu}", ephemeral=True)
        await gu.leave()

def setup(bot):
    bot.add_cog(Admin(bot))