import discord
import random
from discord.ext import commands
from discord.ext.commands import Cog

import modules.ccc as ccc
import modules.talking as talking
import modules.basics as basics

class Time(Cog):
    def __init__(self,bot):
        self.bot = bot

    # @commands.command(pass_context=True, aliases=["event","events"])
    # async def calendar(self, context):
        # """Toggles pings on most commands."""
        # m = context.message
        # u = m.author
        # bot = self.bot
        
        # if u.id in bot.disablereplyping:
            # bot.disablereplyping.remove(u.id)
            # await talking.reply(context, "You've enabled pings on most commands.")
        # else:
            # bot.disablereplyping.append(u.id)
            # await talking.reply(context, "You've disabled pings on most commands.")
        # basics.save(bot,"disablereplyping")
        # print(bot.disablereplyping)
        
    @commands.command(name='8time', pass_context=True, aliases=["time"])
    async def eighttime(self, context):
        """Ansers with a random amount of time.
        
        Based on Micman's old ~rtime."""
        q=basics.contentq(context.message.content, split=False)
        numb = random.randint(1, 100)
        await talking.reply(context,
            'asked {}, I respond: {} {}!'.format(basics.spitback(q),numb,ccc.eighttime(numb!=1)))
        
def setup(bot):
    bot.add_cog(Time(bot))