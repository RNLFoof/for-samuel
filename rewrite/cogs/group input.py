import datetime

import discord
import random
from discord.ext import commands
from discord.ext.commands import Cog

import modules.ccc as ccc
import modules.talking as talking
import modules.basics as basics
from classes.Petition import Petition
from modules import utility


class GroupInput(Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command(pass_context=True, aliases=["petiton"])
    async def petition(self, context):
        """Start a petition with the given title.

        People can "sign" the petition by hitting a pen reaction, adding their name to a list.

        Modifiers:
        nounsign|noundo : Disables unsigning.
        EMOJI : Replaces the pen with that emoji."""
        bot=self.bot
        q = basics.contentq(context.message.content,split=False)
        q, undo, match = basics.subcommands(context,q,["nounsign|noundo",r".*?"])

        if match!=None:
            emoji = utility.get_emoji(self.bot,match.group(1))
            if emoji == None:
                await talking.reply(context,"{} isn't a valid emoji!".format(match.group(1)))
                return
        else:
            emoji = utility.get_emoji(self.bot, "<a:rolling:393641477068029953>")

        Petition(bot, validfor=datetime.timedelta(minutes=60), messagecount=1, emoji=emoji, q=q, lit=await ccc.lit(context.message,binary=True),
                    context=context)
        
def setup(bot):
    bot.add_cog(GroupInput(bot))