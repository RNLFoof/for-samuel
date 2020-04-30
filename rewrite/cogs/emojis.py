import discord
from PIL import Image
from discord.ext import commands
import random
import asyncio
import datetime

from discord.ext.commands import Cog

from classes.ReactionChart import ReactionChart
from classes.ReactionReactions import ReactionReactions

import modules.talking as talking
import modules.basics as basics
import modules.ccc as ccc
import modules.utility as utility


class Emojis(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='8moji', pass_context=True, aliases=["moji","8emoji","8cancer","cancer"])
    async def eightmoji(self, context):
        """Picks one of our god-awful custom emojis."""
        q=basics.contentq(context.message.content, split=False)
        await talking.reply(context,'asked {}, I respond: {}'.format(basics.spitback(q),ccc.eightcustomemoji(self.bot)))

    @commands.command(pass_context=True, aliases=["reactchart","rc"])
    async def reactionchart(self, context):
        """Displays who reacted with what to a message."""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)

        mfrom = await utility.referencemessage(context)
        if mfrom == None:
            return

        ReactionChart(bot, validfor=datetime.timedelta(minutes=5), foreignmessages=[mfrom], context=context)
        #await talking.reply(context,s.format(basics.spitback(q),ccc.eightcustomemoji(self.bot)), nowebhook=True)

    @commands.command(pass_context=True, aliases=["he", "hm", "emoji", "huge", "big"])
    async def hugemoji(self, context):
        """Shows full size emojis.

        Lists emoji URLs based on what you give it, separated by spaces."""
        q = basics.contentq(context.message.content)
        emoji = []
        for y in q:
            emojifound = utility.get_emoji_url(self.bot, y)
            if emojifound != None:
                emoji.append(emojifound)
        if emoji == []:
            await talking.reply(context,"I wasn't able to match any emojis in your message.")
        else:
            await talking.reply(context, "\n" + "\n".join(emoji))

    @commands.command(pass_context=True, aliases=["eb"])
    async def emojibutton(self, context):
        """Generates replacement CSS for use in BD.

        Generates CSS that you can use to replace the default random emojis that you click on to open the emoji menu.
        List up to 55 image references."""
        q = basics.contentq(context.message.content)
        imgs = []
        base = 44

        # Valid length?
        if len(q) == 0:
            await talking.reply(context,"You need to make at least one image reference.")
            return
        if len(q) > 55:
            await talking.reply(context,f"You can't make more than 55 image references. You've made **{len(q)}**, currently.")
            return

        # Get images
        for y in q:
            imgfound = await utility.referenceimage(context,s=y)
            if imgfound != None:
                imgfound.thumbnail((base, base))
                imgfound.convert("RGBA")
                imgs.append(imgfound)
            else:
                return

        # Actual generation
        img = Image.new('RGBA', (base * 11, base * 5), (255,255,255,0))
        n = 0
        print(imgs)
        for y in range(5):
            for x in range(11):
                xdif = base - imgs[n].width
                ydif = base - imgs[n].height
                img.paste(imgs[n], (
                    int((x*base) + xdif),
                    int((y * base) + ydif),
                    int(x*base + xdif) + imgs[n].width,
                    int(y*base + ydif) + imgs[n].height ) )
                n += 1
                n %= len(imgs)

        print(img)
        urlmsg = await talking.reply(context,PIL=img)
        await talking.say(context, f"""```css
.sprite-2iCowe {{
    background-image: url({urlmsg.attachments[0].url});
}}```""")

    @commands.command(pass_context=True, aliases=["reactionreaction","reactreact","rr"])
    async def reactionreactions(self, context):
        """Allows you to react to reactions. Sorta.

        Use a message reference to pick a message, then """
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)

        mfrom = await utility.referencemessage(context)
        if mfrom == None:
            return

        ReactionReactions(bot, validfor=datetime.timedelta(minutes=10), foreignmessages=[mfrom], context=context)

def setup(bot):
    bot.add_cog(Emojis(bot))