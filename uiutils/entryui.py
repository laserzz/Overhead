import discord
from discord.ui import View
from main import apdcoll
from uiutils import ticketui

class EntryView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Acknowledge", style=discord.ButtonStyle.green, custom_id="ack-btn")
    async def ack_btn(self, button, interaction:discord.Interaction):
        user = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))
        await interaction.message.delete(delay=1.0)
        await user.send("Your entry has been acknowledged. Thank you for writing, and we will address your issue ASAP.")

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="etickets-btn")
    async def etic_btn(self, button, interaction:discord.Interaction):
        for chn in interaction.guild.channels:
            if str(interaction.user.id) in chn.name:
                return await interaction.response.send_message("You already have an open ticket!", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        data = await apdcoll.find_one({"_id": interaction.guild_id})

        category = interaction.guild.get_channel(data["ticketCat"])
        channel = await interaction.guild.create_text_channel(name=f"{interaction.message.embeds[0].footer.text}", category=category)
        perms = channel.overwrites_for(interaction.guild.get_member(int(interaction.message.embeds[0].footer.text)))
        perms.view_channel=True
        await channel.set_permissions(interaction.user, overwrite=perms)
        embed = discord.Embed(title=f"ticket {interaction.user}", description="Describe your issue here.")
        await channel.send(embed=embed, view=ticketui.TicketView())
        await interaction.message.delete(delay=0.5)