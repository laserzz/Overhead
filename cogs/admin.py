import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    adcmd = discord.SlashCommandGroup(name="admin", description="admin commands. bot owner only.")

    @adcmd.command(description="leave server")
    @commands.is_owner()
    async def leave(self, interaction:discord.Interaction):
        modal = discord.ui.Modal(
            title="Leave server"
        )
        modal.add_item(discord.ui.InputText(label="Server ID"))

        async def callback(inter: discord.Interaction):
            gu = self.bot.get_guild(int(modal.children[0].value))
            await inter.response.send_message(f"left from {gu}", ephemeral=True)
            await gu.leave()

        modal.callback = callback
        await interaction.response.send_modal(modal)
        await modal.wait()

def setup(bot):
    bot.add_cog(Admin(bot))