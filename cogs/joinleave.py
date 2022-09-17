from discord.ext import commands
import discord
from main import coll, apdcoll, vcoll, apucoll, vdcoll, vmcoll, vucoll, ecoll
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()
joinhook = os.getenv('JOIN')
leavehook = os.getenv('LEAVE')

async def toWebhook(webhookURL, em):
    async with aiohttp.ClientSession() as cs:
        webhook = discord.Webhook.from_url(webhookURL, session=cs)
        await webhook.send(embed=em)

class JoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):

        embed2 = discord.Embed(title="Guild Join", color=0x00ff00)
        embed2.add_field(name="Guild Name", value=guild.name, inline=False)
        embed2.add_field(name="ID", value=str(guild.id), inline=False)
        embed2.add_field(name="Owner", value=f"{guild.owner} `{guild.owner_id}`", inline=False)
        embed2.add_field(name="Members", value=f"```{guild.member_count}```", inline=False)
        embed2.set_thumbnail(url=guild.icon.url)
        embed2.set_footer(text=f"Guild #{len(self.bot.guilds)}")
        
        await toWebhook(joinhook, embed2)

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

        em = discord.Embed(title="Guild Leave", color=0xff0000)
        em.add_field(name="Guild Name", value=guild.name, inline=False)
        em.add_field(name="ID", value=str(guild.id), inline=False)
        em.add_field(name="Owner", value=f"{guild.owner} `{guild.owner_id}`", inline=False)
        em.add_field(name="Members", value=f"```{guild.member_count}```", inline=False)
        em.set_thumbnail(url=guild.icon.url)
        em.set_footer(text=f"Guild #{len(self.bot.guilds) + 1}")
        await toWebhook(
            leavehook,
            em
        )

def setup(bot):
    bot.add_cog(JoinLeave(bot))