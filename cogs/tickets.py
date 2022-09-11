import discord
from discord.ext import commands
from main import apdcoll
from uiutils import ticketui, ticketsetup

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ticketsetup.TicketSetupView())
        self.bot.add_view(ticketui.TicketView())

    ticketcmd = discord.SlashCommandGroup(name="tickets", description="ticket commands")

    @ticketcmd.command(name="ticketsetup", description="sets up ticket channel")
    @commands.has_permissions(administrator=True)
    async def ticketsetup(self, ctx):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }
        cho = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=True)
        }
        category = await ctx.guild.create_category(name="tickets", overwrites=overwrites)
        logchannel = await ctx.guild.create_text_channel(name="ticket logs", category=category)
        channel = await ctx.guild.create_text_channel(name="tickets", category=category, overwrites=cho)
        await apdcoll.update_one(
            {"_id": ctx.guild.id},
            {
                "$set": {
                    "ticketChannel": channel.id,
                    "ticketLogs": logchannel.id,
                    "ticketCat": category.id,
                    "makeDelete": False
                }
            },
            upsert=True
            )
        embed = discord.Embed(title="Open a Ticket!", description="Open a ticket using the button below.")
        await channel.send(embed=embed, view=ticketsetup.TicketSetupView())
        await ctx.respond("setup complete!", ephemeral=True)

    @ticketcmd.command(name="addrole", description="Adds a role to ticket handlers.")
    @commands.has_permissions(administrator=True)
    async def add_ticket_role(self, ctx, role:discord.Role):
        data = await apdcoll.find_one({"_id": ctx.guild.id})

        channel = ctx.guild.get_channel(data["ticketCat"])
        perms = ctx.channel.overwrites_for(role)
        perms.view_channel=True
        await channel.set_permissions(role, overwrite=perms)
        await ctx.respond(f"{role.mention} added to Ticket Channels!", ephemeral=True)

    @ticketcmd.command(name="removerole", description="Removes a role from ticket handlers.")
    async def remove_ticket_role(self, ctx, role:discord.Role):
        data = await apdcoll.find_one({"_id": ctx.guild.id})

        channel = ctx.guild.get_channel(data["ticketCat"])
        perms = ctx.channel.overwrites_for(role)
        perms.view_channel=False
        await channel.set_permissions(role, overwrite=perms)
        await ctx.respond(f"{role.mention} removed from ticket channels.", ephemeral=True)

    @ticketcmd.command(name="openticket", description="opens a ticket with a certain user.")
    @commands.has_permissions(administrator=True)
    async def open_ticket(self, ctx, member:discord.Member):
        data = await apdcoll.find({"_id": ctx.guild.id})
        async for ids in data:
            try:
                category = ctx.guild.get_channel(ids["ticketCat"])
            except:
                return await ctx.respond("The ticket module has not been set up!", ephemeral=True)
        channel = await ctx.guild.create_text_channel(name=f"ticket {member}", category=category)
        perms = channel.overwrites_for(member)
        perms.view_channel=True
        await channel.set_permissions(member, overwrite=perms)
        embed = discord.Embed(title=f"ticket {member}", description="Staff has opened a ticket with you.")
        await channel.send(embed=embed, view=ticketui.TicketView())
        await ctx.respond("Ticket Open!", ephemeral=True)

    @ticketcmd.command(name="createclose", description="Toggles whether ticket creator can close it. False by default.")
    async def createclose(self, ctx, setting:bool):
        await apdcoll.update_one(
            {"_id": ctx.guild.id},
            {"$set": {"makeDelete": setting}}
        )
        await ctx.respond(f"Setting set to {setting}.")

def setup(bot):
    bot.add_cog(Tickets(bot))