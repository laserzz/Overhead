from discord.ext import commands
import discord
from main import coll, apdcoll, vcoll, apucoll, vdcoll, vmcoll, vucoll, ecoll
import aiohttp

async def toWebhook(webhookURL, em):
    async with aiohttp.ClientSession() as cs:
        webhook = discord.Webhook.from_url(webhookURL, session=cs)
        await webhook.send(embed=em)

class JoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):

        embed2 = discord.Embed(title="Guild Join", description=f"Joined {guild.name}\n**Member Count:** {guild.member_count}", color=0x00ff00)
        embed2.set_thumbnail(url=guild.icon.url)
        embed2.set_footer(text=f"ID: {guild.id}")
        
        await toWebhook("https://discord.com/api/webhooks/1019824834835918859/hsozuMNoNUJn9jxLbiyvT-rwOTcJO5Aooi3phEqNSpojPHiB9a1YdvcxgtaVDG8QrQBE", embed2)

        user = self.bot.user
        embed = discord.Embed(title="Thanks For Inviting Me!", description="Type /help for more information.")
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_footer(text="Overhead Join Message", icon_url=guild.icon.url)
        for channel in guild.channels:
            try:
                await channel.send(embed=embed)
                return
            except:
                continue

    @commands.Cog.listener()
    async def on_guild_remove(self, guild:discord.Guild):
        ls = [apdcoll, vcoll, apucoll, vdcoll, vmcoll, vucoll, coll, ecoll]
        gid = {"_id": guild.id}
        for colls in ls:
            try:
                await colls.delete_one(gid)
            except:
                continue

        em = discord.Embed(title="Guild Leave", description=f"Left {guild.name}", color=0xff0000)
        em.set_thumbnail(url=guild.icon.url)
        em.set_footer(text=f"ID: {guild.id}")
        await toWebhook(
            "https://discord.com/api/webhooks/1019824962745413672/vDqbRpOwYhJOFDL8oS5XQVwzTVZmz_gbrOHutg6FdamEIsaJRrpxFgChLNFuTJclYmrD",
            em
        )

def setup(bot):
    bot.add_cog(JoinLeave(bot))