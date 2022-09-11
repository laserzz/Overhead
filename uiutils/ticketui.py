import discord
from main import apdcoll
from discord.ui import Modal, InputText, View
import asyncio

class TicketView(View): #class for managing opened tickets
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Close Ticket", row=0, style=discord.ButtonStyle.red, custom_id="close_ticket")

    async def close_btn_callback(self, button, interaction: discord.Interaction):
        data = await apdcoll.find_one({"_id": interaction.guild_id})
        channel = interaction.guild.get_channel(data["ticketLogs"])
        category = interaction.guild.get_channel(data["ticketCat"])
        mset = data["makeDelete"]
        if mset is True and str(interaction.user.id) in interaction.channel.name:
            await interaction.response.send_message("This channel will be deleted shortly.", ephemeral=True)
            embed = discord.Embed(title=f"Log Summary for {interaction.user}'s ticket.", description="see below")
            await channel.send(embed=embed)
            await interaction.channel.delete()
            return
        else:
            pass

        for role in interaction.user.roles:
            perms = category.overwrites_for(role)
            if perms.view_channel is True or interaction.user is interaction.guild.owner:
                await interaction.response.send_message("This channel will be deleted shortly.", ephemeral=True)
                embed = discord.Embed(title=f"Log Summary for {interaction.user}'s ticket.", description="see below")
                await channel.send(embed=embed)
                await interaction.channel.delete()
                return
        else:
            return await interaction.response.send_message("only staff can close tickets", ephemeral=True)

    @discord.ui.button(label="Close With Reason", row=0, style=discord.ButtonStyle.red, custom_id="close_reason")

    async def close_reason(self, button, interaction: discord.Interaction):

        data = await apdcoll.find_one({"_id": interaction.guild_id})
        channel = interaction.guild.get_channel(data["ticketLogs"])
        category = interaction.guild.get_channel(data["ticketCat"])
        for role in interaction.user.roles:
            perms = category.overwrites_for(role)
            if perms.view_channel or interaction.user is interaction.guild.owner:

                modal = Modal(title="Close Reason")
                modal.add_item(InputText(label="Reason", style=discord.InputTextStyle.short))

                async def modal_callback(interaction: discord.Interaction):
                    embed = discord.Embed(title=f"Log Summary for {interaction.user}'s ticket.", description="see below")
                    embed.add_field(name="Reason", value=modal.children[0].value)
                    await interaction.response.send_message("reason submitted!", ephemeral=True)
                    await channel.send(embed=embed)

                modal.callback = modal_callback
                await interaction.response.send_modal(modal)
                await modal.wait()
                await asyncio.sleep(1)
                await interaction.channel.delete()
                return
        else:
            return await interaction.response.send_message("only staff can close tickets", ephemeral=True)