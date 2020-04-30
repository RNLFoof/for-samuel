import discord
from discord.ext import commands
from discord.ext.commands import Cog

import modules.talking as talking
import modules.basics as basics
import modules.ccc as ccc
import datetime
import re

import modules.utility as utility
import modules.aesthetic as aesthetic

from classes.PageMessage import PageMessage

class Users(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def bans(self,context):
        """Checks who's banned on the server."""
        s=""
        try:
            l = await context.message.guild.bans()
        except:
            s="Understandably, I don't have permission to ban people, so I can't see who has already been banned."
            await talking.reply(context, s)
            return

        if len(l)==0:
            s="Nobody is banned on this server."
            await talking.say(context,s)
        else:
            lol = [["User","Reason","Mention"]]
            print(l)
            for x in l:
                lol.append([basics.truename(self.bot, x.user), "No reason provided" if x.reason is None else x.reason, x.user.mention])
            s = aesthetic.chart(lol,align=["l","l","unwrap"])

            s="The following users are banned from this server:\n\n"+s
            await talking.reply(context, s, disableaes=True)
        
def setup(bot):
    bot.add_cog(Users(bot))