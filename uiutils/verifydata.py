import discord
from discord.ext import commands
from discord.ui import View, Modal, InputText
from main import vmcoll, vdcoll, vucoll
from uiutils import vdataui

class VDataSetup(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Verify", custom_id="verify-btn", style=discord.ButtonStyle.green)
    async def verify_callback(self, button, interaction: discord.Interaction):
        data = await vmcoll.find_one({"_id": interaction.guild_id})
        modal = Modal(title="Mod App")
        data.pop("_id")
        for field in data:
            val = data[field]
            if field == "Verify 1":
                modal.add_item(InputText(label=val))
                continue
            modal.add_item(InputText(label=val, style=discord.InputTextStyle.long))

        async def modal_callback(interaction: discord.Interaction):
            try:
                descstr = ""
                data = await vdcoll.find_one({"_id": interaction.guild_id})
                fielddata = await vmcoll.find_one({"_id": interaction.guild_id})
                i = 0
                for fields in fielddata:
                    if fields == "_id":
                        continue
                    descstr += f"**{fields}**\n{modal.children[i].value}\n\n"
                    i += 1
                
                channel = interaction.guild.get_channel(data['channelid'])
                await vucoll.update_one({"_id": interaction.guild_id}, {"$set": {interaction.user.name: interaction.user.id}}, upsert=True)
                embed = discord.Embed(title="App Results", description=descstr)
                embed.set_footer(text=interaction.user.id)
                await channel.send(embed=embed, view=vdataui.VDataView())
                await interaction.response.send_message("App sent!", ephemeral=True)
                
            except discord.HTTPException:
                await interaction.response.send_message("An error occurred while submitting the app, likely due to a field being too long.")

        modal.callback = modal_callback
        await interaction.response.send_modal(modal)