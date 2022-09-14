import discord
from discord.ui import View, Modal, InputText
from main import apdcoll, apucoll, coll
from uiutils import appdataui

class ApplyView(View): #class for applying
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Apply", custom_id="apply-button", style=discord.ButtonStyle.green)
    async def btn_callback(self, button, interaction: discord.Interaction):
        data = await coll.find_one({"_id": interaction.guild_id})
        data2 = await apucoll.find_one({"_id": interaction.guild_id})
        try:
            usercheck = data2[interaction.user.name]
            if usercheck == interaction.user.id:
                return await interaction.response.send_message("You already have an open application.", ephemeral=True)
        except KeyError:
            pass
        modal = Modal(title="Mod App")
        data.pop("_id")
        for key in data:
            val = data[key]
            if key == "Field 1":
                modal.add_item(InputText(label=val))
                continue
            modal.add_item(InputText(label=val, style=discord.InputTextStyle.long))

        async def modal_callback(interaction: discord.Interaction):
            try:
                descstr = ""
                data = await apdcoll.find_one({"_id": interaction.guild_id})
                fielddata = await coll.find_one({"_id": interaction.guild_id})
                i = 0
                for fields in fielddata:
                    val = fielddata[fields]
                    if fields == "_id":
                        continue
                    descstr += f"**{val}**\n{modal.children[i].value}\n\n"
                    i += 1

                channel = interaction.guild.get_channel(data['channelid'])
                await apucoll.update_one({"_id": interaction.guild_id}, {"$set": {interaction.user.name: interaction.user.id}}, upsert=True)
                embed = discord.Embed(title="App Results", description=descstr)
                embed.set_footer(text=interaction.user.id)
                await channel.send(embed=embed, view=appdataui.AppDataView())
                await interaction.response.send_message("App sent!", ephemeral=True)
            except KeyError:
                await interaction.response.send_message("The mod apps have not completed setup!")
            except discord.HTTPException:
                await interaction.response.send_message("An error occurred while submitting the app, likely due to a field being too long.")

        modal.callback = modal_callback
        await interaction.response.send_modal(modal)