import discord
from discord.ext import commands
from main import ecoll
from uiutils.entryui import EntryView

class Entry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ecmd = discord.SlashCommandGroup(name="entry", description="entry commands")

    @ecmd.command(name="entrysetup", description="sets up entry end channel. One will be created if none is specified.")
    @commands.has_permissions(administrator=True)
    @discord.option(name="channel", type=discord.TextChannel, required=False, default=None)
    async def entrysetup(self, ctx, channel):
        ov = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }

        if not channel:
            ch = await ctx.guild.create_text_channel(name="entry logs", overwrites=ov)
            chob = ctx.guild.get_channel(ch.id)
            await ecoll.update_one({"_id": ctx.guild.id}, {"$set": {"channel": chob.id}}, upsert=True)

        elif channel:
            await ecoll.update_one({"_id": ctx.guild.id}, {"$set": {"channel": channel.id}}, upsert=True)

        await ctx.respond("setup done.")

    @ecmd.command(name="create", description="creates a new entry.")
    async def create_entry(self, ctx, message):
        em = discord.Embed(title=f"Entry From {ctx.author}", description=message)
        em.set_footer(text=f"{ctx.author.id}")
        doc = await ecoll.find_one({"_id": ctx.guild.id})
        ch = ctx.guild.get_channel(doc["channel"])
        await ch.send(embed=em, view=EntryView())
        await ctx.respond("entry created successfully.", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(EntryView())

def setup(bot):
    bot.add_cog(Entry(bot))