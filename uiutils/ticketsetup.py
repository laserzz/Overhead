import discord
from uiutils import ticketui
from discord.ui import View
from main import apdcoll

class TicketSetupView(View): #class for opening tickets
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="ticket_opener")

    async def btn_callback(self, button, interaction:discord.Interaction):
        for chn in interaction.guild.channels:
            if str(interaction.user.id) in chn.name:
                return await interaction.response.send_message("You already have an open ticket!", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        data = await apdcoll.find_one({"_id": interaction.guild_id})

        category = interaction.guild.get_channel(data["ticketCat"])
        channel = await interaction.guild.create_text_channel(name=f"{interaction.user.id}", category=category)
        perms = channel.overwrites_for(interaction.user)
        perms.view_channel=True
        await channel.set_permissions(interaction.user, overwrite=perms)
        embed = discord.Embed(title=f"ticket {interaction.user}", description="Describe your issue here.")
        await channel.send(embed=embed, view=ticketui.TicketView())