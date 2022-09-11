from discord.ext import commands
import discord
from main import coll, apdcoll, vcoll, apucoll, vdcoll, vmcoll, vucoll

class joinleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        user = self.bot.user
        embed2 = discord.Embed(title="Guild Join", description=f"Joined {guild.name}\n**Member Count:** {guild.member_count}", color=0x00ff00)
        embed2.set_thumbnail(url=guild.icon.url)
        embed2.set_footer(text=f"ID: {guild.id}")
        ch = self.bot.get_channel(1018377407473922099)
        await ch.send(embed=embed2)

        embed = discord.Embed(title="Thanks For Inviting Me!", description="Type /help for more information.")
        embed.set_thumbnail(url=user.avatar.url)
        for channel in guild.channels:
            try:
                await channel.send(embed=embed)
                return
            except:
                continue

    @commands.Cog.listener()
    async def on_guild_remove(self, guild:discord.Guild):
        ls = [apdcoll, vcoll, apucoll, vdcoll, vmcoll, vucoll, coll]
        gid = {"_id": guild.id}
        for colls in ls:
            await colls.delete_one(gid)

        em = discord.Embed(title="Guild Leave", description=f"Left {guild.name}", color=0xff0000)
        em.set_thumbnail(url=guild.icon.url)
        em.set_footer(text=f"ID: {guild.id}")
        ch = self.bot.get_channel(1018377407473922099)
        await ch.send(embed=em)

def setup(bot):
    bot.add_cog(joinleave(bot))