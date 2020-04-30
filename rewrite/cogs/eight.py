import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Cog

import modules.talking as talking
import modules.basics as basics
import modules.ccc as ccc
import random
from PIL import Image
from PIL import ImageDraw

from classes.EightBall import EightBall
from classes.EightBannedUser import EightBannedUser
from classes.EightLineFromSonic06 import EightLineFromSonic06
from classes.EightUser import EightUser


class Eight(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="8")
    async def eight(self, context):
        """Just tells you 8."""
        await context.send("8")
        
    # @commands.command(name='8no', aliases=["no"])
    # async def eightno(self, context):
    #     """Randomly answers no."""
    #     q=basics.contentq(context.message.content, split=False)
    #     await talking.reply(context,'asked {}, I respond: {}'.format(basics.spitback(q), ccc.eightno()))
    #
    # @commands.command(name='8yes', aliases=["yes"])
    # async def eightyes(self, context):
    #     """Randomly answers yes."""
    #     q=basics.contentq(context.message.content, split=False)
    #     await talking.reply(context,'asked {}, I respond: {}'.format(basics.spitback(q),ccc.eightyes()))
        
    @commands.command(name='8hippo', pass_context=True, aliases=["hippo"])
    async def eighthippo(self, context):
        """Answers with a random hippo from our vast catalog."""
        q=basics.contentq(context.message.content, split=False)
        await talking.reply(context,'asked {}, I respond: {}'.format(basics.spitback(q),ccc.eighthippo(self.bot)))
        
    @commands.command(pass_context=True, name='8channel')
    async def eightchannel(self, context):
        """Answers with a random channel."""
        q=basics.contentq(context.message.content, split=False)
        await talking.reply(context,'asked {}, I respond: {}'.format(basics.spitback(q),ccc.eightchannel(context.message.guild)))
        
    @commands.command(name='8chat', pass_context=True, aliases=["chat"])
    async def eightchat(self, context):
        """Answers with a random TT speedchat phrase."""
        q=basics.contentq(context.message.content, split=False)
        await talking.reply(context,'asked {}, I respond: {}'.format(basics.spitback(q),ccc.eightchat()))
    
    @commands.command(name='8color', pass_context=True, aliases=["8colour","8col","col"])
    async def eightcolor(self, context):
        """Answers with a random color."""
        q=basics.contentq(context.message.content, split=False)
        m=context.message
        color = ccc.eightcolor()
        image = Image.new('RGBA', (100,100), (0,0,0,0))
        draw = ImageDraw.Draw(image, mode="RGBA")
        draw.ellipse((0,0,99,99),fill="#000")
        border = 8
        draw.ellipse((border,border,99-border,99-border),fill=color)
        image = image.resize((25,25),Image.ANTIALIAS)
        await talking.reply(context,'asked {}, I respond: {}!'.format(basics.spitback(q),ccc.eightcolor()), PIL=image)
        
    @commands.command(name='8compact', pass_context=True, aliases=["8comp"])
    async def eightcompact(self, context):
        """Reacts with a yes or no."""
        await context.message.add_reaction(random.choice([":bn_yes:331164192864206848",":bn_no:331164190284972034"]))
        
    @commands.command(name='8xavier',pass_context=True,  aliases=["8xra"])
    async def eightxavier(self, context):
        """Answers with a random XRA ks mateline."""
        q = basics.contentq(context.message.content, split=False)
        await talking.reply(context,'asked {}, I respond: {}'.format(basics.spitback(q),ccc.eightxavier()), specificwebhook=("Xavier","https://cdn.discordapp.com/attachments/320713790771691530/536735846439845888/1502427950625.png"))

    @commands.command(name='8animal', aliases=["animal","8animals","animals","8ani","ani","8animorphs","animorphs"])
    async def eightanimal(self, context):
        """Answers with a random animal.

        Credit to https://a-z-animals.com/animals/, because I freaking stole their list(and took out some of the more obscure or redundant animals)"""
        q=basics.contentq(context.message.content, split=False)
        await talking.reply(context,'asked {}, I respond: {}!'.format(basics.spitback(q),ccc.eightanimal()))

    @commands.command(name='8fetlifeadvertisement', pass_context=True, aliases=["fetlifeadvertisement","8fetlife","fetlife","8ad","ad","8fla","fla"])
    async def eightfetlifeadvertisement(self, context):
        """Answers with a random fetlife ad."""
        q = basics.contentq(context.message.content, split=False)
        await talking.reply(context, 'asked {}, I respond: {}'.format(basics.spitback(q), ccc.allads()))

    @commands.command(name="8ball", aliases=["ball","8yes","8yeah","8ya","8yeh","8ye","8yup","8y","8no","8nah","8nope","8n","yes","yeah","ya","yeh","ye","yup","y","no","nah","nope","n"])
    async def eightball(self, context):
        """Randomly answers yes or no.

        Modifiers:
        yes|yeah|ya|yeh|ye|yup|y|no|nah|nope|n|NUMBER(\||/|;|:)NUMBER : Forces all yeses, all nos, or a yes:no ratio.
        
        Rigged Aliases:
        8yes, 8yeah, 8ya, 8yeh, 8ye, 8yup, 8y, yes, yeah, ya, yeh, ye, yup, y : Forces all yeses.
        8no, 8nah, 8nope, 8n, no, nah, nope, n : Forces all nos."""
        bot = self.bot
        EightBall(bot, validfor=datetime.timedelta(minutes=5), messagecount=1, q=basics.contentq(context.message.content,split=False),
                 context=context)
        

    @commands.command(name='8linefromsonic06', aliases=["8linefromsonic2006","8linefromsonic","8line","8sonic","linefromsonic06","linefromsonic2006","linefromsonic","line","sonic","06","806"])
    async def eightlinefromsonic06(self, context):
        """Answers with a random line from Sonic 06.

        Credit to SONIC FANS ON SONIC WIKI"""
        bot = self.bot
        EightLineFromSonic06(bot, validfor=datetime.timedelta(minutes=5), messagecount=1,
                  q=basics.contentq(context.message.content, split=False),
                  context=context)

    @commands.command(name='8user', aliases=["8cp","cp","coolpeople","8coolpeople","user"])
    async def eightuser(self, context):
        """Answers with a random medium+ priority member."""
        bot = self.bot
        EightUser(bot, validfor=datetime.timedelta(minutes=5), messagecount=1,
                  q=basics.contentq(context.message.content, split=False),
                  context=context)

    @commands.command(pass_context=True, name='8banneduser', aliases=["8banned","8ban","8bans"])
    async def eightbanneduser(self,context):
        """Answers a question with a random banned user from the server."""
        bot=self.bot
        m=context.message

        try:
            l = await context.message.guild.bans()
        except:
            await talking.reply(context,"I'm missing permissions to check who is banned on this server.")
            return
        if not l:
            await talking.reply(context,"Nobody is banned on this server.")
            return

        EightBannedUser(bot, validfor=datetime.timedelta(minutes=5), messagecount=1,
                  q=basics.contentq(context.message.content, split=False), l=l,
                  context=context)

def setup(bot):
    bot.add_cog(Eight(bot))