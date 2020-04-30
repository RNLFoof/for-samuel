import discord
from discord.ext import commands
from discord.ext.commands import Cog

import modules.talking as talking
import modules.basics as basics

class Personalization(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def reply(self, context):
        """Toggles pings on most commands."""
        m = context.message
        u = m.author
        bot = self.bot
        
        if u.id in bot.disablereplyping:
            bot.disablereplyping.remove(u.id)
            await talking.reply(context, "You've enabled pings on most commands.")
        else:
            bot.disablereplyping.append(u.id)
            await talking.reply(context, "You've disabled pings on most commands.")
        basics.save(bot,"disablereplyping")
        print(bot.disablereplyping)
        
def setup(bot):
    bot.add_cog(Personalization(bot))