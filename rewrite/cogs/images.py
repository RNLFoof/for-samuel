import discord
from PIL import Image
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

class Images(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True,aliases=["gif"])
    async def gifify(self, context):
        """Converts an Image Reference to a gif.

        Because the pinheads at Discord didn't let you save non-gif reaction images. Might have some loss of quality because I stink."""
        img = await utility.referenceimage(context)
        img.thumbnail((640,480),resample=Image.NEAREST)
        img.save(f"tobedeleted/{context.message.id}.gif", transparency=255,optimize=False)
        with open(f"tobedeleted/{context.message.id}.gif","rb") as f:
            await talking.reply(context,file=f)

def setup(bot):
    bot.add_cog(Images(bot))