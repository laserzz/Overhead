import discord
from discord.ext import commands
from main import vdcoll
from uiutils import modalcreate, verifydata

class FormVerify(commands.Cog, name="Form Verify"):
    def __init__(self, bot):
        self.bot = bot

    manv = discord.SlashCommandGroup(name="manualverify", description="manualverify commands")

    @manv.command(name="logsetup", description="Set up channels to send apps to")
    @commands.has_permissions(administrator=True)
    async def verifyappsetup(self, ctx, verifyrole:discord.Role):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }
        category = await ctx.guild.create_category(name="verifyapps", overwrites=overwrites)
        logchannel = await ctx.guild.create_text_channel(name="verify apps", category=category, overwrites=overwrites)
        await vdcoll.update_one(
            {"_id": ctx.guild.id},
            {
                "$set": {
                    "channelid": logchannel.id,
                    "categoryid": category.id,
                    "verifyroleid": verifyrole.id
                }
            },
            upsert=True
        )
        await ctx.respond("Setup Done!", ephemeral=True)

    @manv.command(description="creates a verify modal")
    async def createmodal(self, ctx):
        modal = modalcreate.VerifyModal(title="Modal Results")
        await ctx.send_modal(modal)

    @manv.command(description="sets up verify modal")
    async def setupverify(self, ctx, channel:discord.TextChannel):
        await channel.send("Button Here", view=verifydata.VDataSetup())
        await ctx.respond("ModApps set up!", ephemeral=True)

def setup(bot):
    bot.add_cog(FormVerify(bot))