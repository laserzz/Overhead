import discord
from discord.ext import commands
from main import apdcoll
from uiutils import modalcreate, applyui, appdataui

class ModApps(commands.Cog, name="Mod Apps"):
    def __init__(self, bot):
        self.bot = bot

    mappcmd = discord.SlashCommandGroup(name='modapps', description='Command for modapps')

    @mappcmd.command(name="logsetup", description="Set up channels to send apps to")
    @commands.has_permissions(administrator=True)
    async def modappsetup(self, ctx, modrole:discord.Role):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }
        category = await ctx.guild.create_category(name="modapps", overwrites=overwrites)
        logchannel = await ctx.guild.create_text_channel(name="modapps", category=category, overwrites=overwrites)
        await apdcoll.update_one(
            {"_id": ctx.guild.id},
            {
                "$set": {
                    "channelid": logchannel.id,
                    "categoryid": category.id,
                    "modroleid": modrole.id
                }
            }
        )
        await ctx.respond("Setup Done!", ephemeral=True)

    @mappcmd.command(name="modalcreate", description="creates a mod app modal")
    @commands.has_permissions(administrator=True)
    async def create(self, ctx):
        modal = modalcreate.MyModal(title="Modal Results")
        await ctx.send_modal(modal)

    @mappcmd.command(name="appsetup", description="sets up apps")
    @commands.has_permissions(administrator=True)
    async def appsetup(self, ctx, channel:discord.TextChannel):
        await channel.send("Staff Application Here!", view=applyui.ApplyView())
        await ctx.respond("ModApps set up!", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(applyui.ApplyView())
        self.bot.add_view(appdataui.AppDataView())

def setup(bot):
    bot.add_cog(ModApps(bot))