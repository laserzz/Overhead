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

    @adcmd.command(description="get info on a server by its ID.")
    @commands.is_owner()
    async def getinfo(self, ctx, guild_id:str):
        gu = self.bot.get_guild(int(guild_id))
        em = discord.Embed(
            name=f"Info For {gu.name}",
            description="See info below."
        )

        em.add_field(name="Member Count", value=gu.member_count)
        em.add_field(name="Verification", value=gu.verification_level)
        em.set_thumbnail(url=gu.icon.url)

        em.set_footer(text=guild_id)

def setup(bot):
    bot.add_cog(Admin(bot))