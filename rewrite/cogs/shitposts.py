import random

import discord
from discord.ext import commands
from discord.ext.commands import Cog

import modules.talking as talking
import modules.basics as basics
import modules.aesthetic as aesthetic
import datetime

from classes.AchievementBrowser import AchievementBrowser
from classes.Sue import Sue

from classes.PageMessage import PageMessage
from modules import ccc, utility


class Shitposts(Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command(pass_context=True, aliases=["financiallydemolish","dragthroughthelegalsystem","classtrial"])
    async def sue(self, context):
        """Sue somebody.
        
        Modifiers:
        all|list|stats|records : Display stats from previous cases."""
        bot = self.bot
        m = context.message
        
        # Modifiers
        q = basics.contentq(m.content,split=False)
        q, all = basics.subcommands(context, q,["all|list|stats|records"])
        if all != None:
            lines = [["User"] + list(Sue.getstats(bot, m.author).keys())]
            pages = []
            something = False
            n = 0
            #for a in range(8):
            if m.guild.id in bot.suepoints.keys():
                for k,i in bot.suepoints[m.guild.id].items():
                    u = m.guild.get_member(k)
                    if u == None:
                        continue
                    l = []
                    for k,i in Sue.getstats(bot, u).items():
                        l.append(str(i))
                    lines.append([basics.truename(bot, u)] + l)
                    something = True
            if not something:
                await talking.reply(context,"There aren't any stats on this server.")
            else:
                align = ["l"]
                l = aesthetic.chart(lines,linelimit=20,align=["l"] + (["r"] * (len(lines[0])-1)))
                for n,x in enumerate(l):
                    pages.append(f"__**Suing Stats**__ (Page {n+1}/{len(l)})\n{x}")
                rm = PageMessage(bot, validfor=datetime.timedelta(minutes=5), messagecount=1, userids = [m.author.id], pages=pages, context=context)
            return
        
        # Make sure there's a mention
        if len(m.mentions) == 0:
            await talking.reply(context,"You need to specify who you want to sue!")
            return
        
        # Initialize stuff
        if m.guild.id not in bot.suepoints.keys():
            bot.suepoints[m.guild.id] = {}
        for uid in [m.author.id,m.mentions[0].id]:
            if uid not in bot.suepoints[m.guild.id].keys():
                bot.suepoints[m.guild.id][uid] = {}
                for a in ["suer","suee"]:
                    for b in ["win","lose"]:
                        bot.suepoints[m.guild.id][uid][a + b] = 0
        basics.save(self.bot, "suepoints")
                        
        reason = basics.mentionlesscontent(basics.contentq(m.content,split=False))
        if reason == "":
            reason = "(No reason.)"
        
        suemsg = await talking.say(context,"­",nowebhook=True)
        rm = Sue(bot, validfor=datetime.timedelta(minutes=5), messagecount=1, suer=m.author, suee=m.mentions[0], reason=reason, context=context)

    @commands.command(pass_context=True)
    async def lit(self, context):
        """Measures how lit the chat is.

        Based on how many messages there were in the last two minutes."""
        ach = await ccc.lit(context.message, ach=True)
        print(ach)
        mps = ach["mps"]

        string = "There's a bit going on, I guess."
        if mps == 0:
            string = "It's totally dead in here."
        if mps >= 1 / 18:
            string = "Better than nothing."
        if mps >= 1 / 16:
            string = "Not dead, I'll say that"
        if mps >= 1 / 14:
            string = "Well, there's activity."
        if mps >= 1 / 12:
            string = "Not lit, but nice."
        if mps >= 1 / 10:
            string = "Not really, but there's stuff happening for sure."
        if mps >= 1 / 8:
            string = "Doing pretty well, I'd say."
        if mps >= 1 / 6:
            string = "Getting there!"
        if mps >= 1 / 4:
            string = "Yeah, it's lit."
        if mps >= 1 / 2:
            string = "IT'S LIT"
        if mps >= 1:
            string = "SHIT'S ON FIRE BRO"
        if mps >= 2:
            string = "IT'S BLOWING UP"
        if mps >= 4:
            string = "SHUT THE FUCK UP"
        if mps >= 6:
            string = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        if mps >= 10:
            string = "WHY"
        if mps >= 15:
            string = "HOW DID YOU EVEN GET THIS RESPONSE YOU DIPSHITS"

        await talking.reply(context, string)

        for u in ach["users"]:
            await AchievementBrowser.ach_check(self.bot, u, context.message.channel, "lit", ach)

    @commands.command(pass_context=True,aliases=["bandwagon"])
    async def hey(self, context):
        """\*touches your shoulder* Hey.

        Says "Hey" five times using an imitation webhook of five random people on the server. Don't leave it blank and instead of "Hey" the webhooks will say whatever you provided."""
        m = context.message
        bot = self.bot

        l = list(m.guild.members)
        random.shuffle(l)

        q = basics.contentq(m.content,split=False)
        if not q:
            q = "Hey"

        for u in l[:5]:
            await talking.say(context,q,specificwebhook=(u.display_name, u.avatar_url))

    @commands.command(pass_context=True, aliases=["fake"])
    async def imitate(self, context):
        """Lets you post webhook messages.

        Provide an Image Reference for the avatar, nickname, and message body, in that order, separated by semicolons."""
        m = context.message
        q = basics.contentq(m.content, split=False)

        q = q.split(";", 2)
        if len(q) < 3:
            await talking.reply(context,
                                "I need an Image Reference for the avatar, nickname, and message body, in that order, separated by semicolons.")
        else:
            url = await utility.referenceimage(context, s=q[0], returnurl=True)
            if not url:
                return
            await talking.say(context, q[2], specificwebhook=(q[1], url))

    @commands.command(pass_context=True, aliases=["mask"], hidden=True)
    async def masks(self, context):
        """Go away"""
        m = context.message
        q = basics.contentq(m.content, split=False)
        d={
            116718249567059974: ("https://cdn.discordapp.com/attachments/315666280185069568/703767537216651274/unknown.png", "Barely Allan"),
            134826546694193153: ("https://cdn.discordapp.com/attachments/204434027774476288/703769697895841922/im-173860.png", "Hai Chang"),
            112767329347104768: ("https://cdn.discordapp.com/attachments/315666280185069568/703777924519690320/unknown.png", "Teenage Edgy Blond Granny"),
            112814914019614720: (" https://cdn.discordapp.com/attachments/141764382513168384/703780828404121651/unknown.png", "Ophiuchus")
        }
        if m.author.id in d:
            await m.delete()
            await talking.say(context, q, specificwebhook=(d[m.author.id][1], d[m.author.id][0]))

    @commands.command(pass_context=True, aliases=["echoes","reverb"])
    async def echo(self, context):
        """Does an echo effect on provided text."""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)

        if not q:
            await talking.reply(context,"I need an input to work with!")
        else:
            await talking.say(context,ccc.echo(q))

    @commands.command(pass_context=True, aliases=["pisson", "cumon", "nuton", "jizzon", "bleedon", "sweaton"])
    async def peeon(self, context):
        """Spray people.

        Shows a dickdick spraying various fluids on a mentioned user based on the alias used.

        Modifiers:
        cum|nut|jizz : Replace pee with cum.
        bleed|blood : Replace pee with blood.
        sweat : Replace pee with sweat.

        Rigged Aliases:
        cumon, nuton, jizzon : Replace pee with cum.
        bleedon : Replace pee with blood.
        sweaton : Replace pee with sweat."""

        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)

        q, cum, bleed, sweat = basics.subcommands(context, q,
                                           [r"cum|nut|jizz", r"bleed|blood", r"sweat"],
                                           riggedaliases=[
                                               {
                                                   "regex": r"cumon|nuton|jizzon",
                                                   "slot": 0,
                                                   "value": "cum"
                                               },
                                               {
                                                   "regex": r"bleedon",
                                                   "slot": 1,
                                                   "value": "bleed"
                                               },
                                               {
                                                   "regex": r"sweaton",
                                                   "slot": 2,
                                                   "value": "sweat"
                                               }
                                           ])

        if len(context.message.mentions) == 0:
            await talking.reply(context, "You need to mention someone!")
            return

        s = "<:dickdicks1:275176074940252163><:dickdicks2:275176053947891714><:dickdicks3:275176078853537792>"
        emoji = basics.useremoji(bot, m.mentions[0])
        if cum:
            s += "<:liqMilk:273903113264693248>"
            fluid = "cum"
        elif bleed:
            s += "<:liqBlood:382341153699135488>"
            fluid = "blood"
        elif sweat:
            s += "💦"
            fluid = "sweat"
        else:
            s += "<:liqPee:273882459924594689>"
            fluid = "pee"

        msg = await talking.say(context, s + emoji)
        await AchievementBrowser.ach_check(bot, m.mentions[0], m.channel, "peetarget",
                           [fluid, context.message.author])
        await msg.add_reaction(basics.useremoji(bot, m.author)[1:-1])

    @commands.command(pass_context=True, aliases=["covid","corona"])
    async def covid19(self, context):
        """Provides COVID-19 stats for a provided country or province.

        Cool API found here:
        https://github.com/ExpDev07/coronavirus-tracker-api"""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)

        confirmed, date = ccc.covid(bot, q, "confirmed", includedate=True)
        deaths = ccc.covid(bot, q, "deaths")
        recovered = ccc.covid(bot, q, "recovered")

        lol = [
            ["Confirmed", confirmed],
            ["Deaths", deaths],
            ["Recovered", recovered]
        ]

        if confirmed is None and deaths is None and recovered is None:
            await talking.reply(context, f"The API didn't return any results for {basics.spitback(q)}.")
        else:
            await talking.reply(context, f"Stats for {basics.spitback(q)} ({date}):\n{aesthetic.chart(lol, header=False)}")

def setup(bot):
    bot.add_cog(Shitposts(bot))