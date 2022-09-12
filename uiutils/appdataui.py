import discord
from discord.ui import View
from main import apdcoll, apucoll
from uiutils import ticketui

class AppDataView(View): #class for viewing application data
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept-btn")
    async def acc_callback(self, button, interaction: discord.Interaction):
        userid = int(interaction.message.embeds[0].footer.text)
        userobj = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))
        username = userobj.name
        data2 = apdcoll.find({"_id": interaction.guild_id})
        role = interaction.guild.get_role(data2["modroleid"])
        await userobj.add_roles(role)

        await userobj.send("Your Application has been accepted!")
        await apucoll.update_one({"_id": interaction.guild_id}, {"$unset": {username: userid}})
        await interaction.message.delete(delay=2)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, custom_id="deny-btn")

    async def deny_callback(self, button, interaction: discord.Interaction):
        userid = int(interaction.message.embeds[0].footer.text)
        userobj = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))
        username = userobj.name
        data = await apucoll.find_one({"_id": interaction.guild_id})
        user = interaction.guild.get_member(data[username])

        await user.send("Your Application has been denied. For more information, you may open a ticket if Overhead's ticket system is set up in the server.")
        await apucoll.update_one({"_id": interaction.guild_id}, {"$unset": {username: userid}})
        await interaction.message.delete(delay=2)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.blurple, custom_id="ticketapp-btn")
    async def tic_callback(self, button, interaction: discord.Interaction):
        userid = int(interaction.message.embeds[0].footer.text)
        userobj = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))
        username = userobj.name
        data = await apucoll.find_one({"_id": interaction.guild_id})
        user = interaction.guild.get_member(data[interaction.user.name])

        await user.send("Staff has opened a ticket for further discussion of your application.")

        username, tag = user.name, user.discriminator
        for chn in interaction.guild.channels:
            if username and tag in chn.name:
                return await interaction.response.send_message("This user already has an open ticket.", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        data = await apdcoll.find({"_id": interaction.guild_id})
        async for ids in data:
            category = interaction.guild.get_channel(ids["ticketCat"])
            
        await apucoll.update_one({"_id": interaction.guild_id}, {"$unset": {username: userid}})
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True),
            user: discord.PermissionOverwrite(view_channel=True)
        }
        channel = await interaction.guild.create_text_channel(name=f"ticket {interaction.user}", category=category, overwrites=overwrites)
        embed = discord.Embed(title=f"ticket {interaction.user}", description="Staff has opened a ticket for further discussion of your application.")
        await channel.send(embed=embed, view=ticketui.TicketView())