import discord
from discord.ext import commands

class HelpCommand(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def help(self, ctx):
        miscls = []
        valstr = ""
        miscstr = ""
        em = discord.Embed(title="Help", description="View Commands below")
        for cn, cog in self.bot.cogs.items():
            cogcmdlist = cog.get_commands()
            if cogcmdlist == []:
                continue
            for scg in cogcmdlist:
                try:
                    for command in scg.walk_commands():
                        cmdstr = str(command)
                        cmdname = cmdstr.split(' ')[1]
                        valstr += f"`{cmdname}`\n"
                    em.add_field(name=cn, value=valstr)
                    valstr = ""

                except:
                    miscls.append(scg)
                    continue

        for miscmd in miscls:
            miscstr += f"`{miscmd}`\n"
        em.add_field(name="Misc", value=miscstr)

        await ctx.respond(embed=em)

def setup(bot):
    bot.add_cog(HelpCommand(bot))