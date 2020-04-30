import json
import pickle
import math

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
from classes.AchievementBrowser import AchievementBrowser
from classes.Help import Help

from classes.PageMessage import PageMessage
from classes.ReactionChart import ReactionChart
from classes.SortableChart import SortableChart


class Meta(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True,aliases=["in","i"])
    async def input(self, context):
        """Inputs to certain commands.

        It'll be mentioned whenever you can use it. With nothing to input to, this command doesn't do anything."""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)

        try:
            await m.delete()
        except:
            pass

        # Specific
        q, id = basics.subcommands(context, q, ["[0-9]+"])
        if id != None:
            id = int(id.group(1))

        # Default
        if id == None:
            bot.inputmenus_channelids.setdefault(m.channel.id, [])
            if len(bot.inputmenus_channelids) != 0:
                id = bot.inputmenus_channelids[m.channel.id][-1]

        # Go
        if id != None:
            m.content = q
            await bot.inputmenus_idim[int(id)].inputmessage(m)

    @commands.command(pass_context=True,aliases=["h"],hidden=True)
    async def helpnew(self, context):
        bot = self.bot
        q = basics.contentq(context.message.content,split=False)
        #await talking.say(context,embed=await basics.help(context,q,False))

        Help(bot, validfor=datetime.timedelta(minutes=10), show=q, context=context)

        if context.message.author.id == bot.rnl.id and "GO" in context.message.content:
            await basics.updateglobalhelp(context)

    @commands.command(pass_context=True,aliases=["apart","ap"])
    async def apartment(self, context):
        """Provides a link to RSRB's Low Budget Apartment."""
        await talking.reply(context,"why do strangers keep coming into my fuckin house\nhttps://discord.gg/XaYv9cr")

    @commands.command(pass_context=True, aliases=["ach", "achievement"])
    async def achievements(self, context):
        """Opens an achievement display menu.

        Mention someone to see their achievements instead.

        Modifiers:
        top|list|high|rank|ranks : Show a scoreboard. """
        bot = self.bot
        m = context.message
        q = basics.contentq(context.message.content, split=False)

        q, top, transfer = basics.subcommands(context, q, ["top|list|high|rank|ranks","transfer"])

        if top != None:
            achievements = AchievementBrowser.getachievements()
            embed = discord.Embed(title="Achievement Scoreboard", type="rich")
            cap = 0
            for x in achievements:
                if x["special"] == False:
                    cap += 1
            raredict = {}
            highdict = {}
            for s in [m.guild.id,"global"]:
                for k in self.bot.ach_tracking[s].keys():
                    u = context.message.guild.get_member(k)
                    if u != None:
                        score = 0
                        icons = ""
                        for n, x in enumerate(achievements):
                            if x["icon"] not in raredict.keys():
                                raredict[x["icon"]] = 0
                            if n in self.bot.ach_tracking[s][k].keys() and x["special"] == False:
                                if False not in self.bot.ach_tracking[s][k][n]:
                                    score += 1
                                    icons += x["icon"]
                                    raredict[x["icon"]] += 1
                        highdict.setdefault(u.id,[u,0,""])
                        highdict[u.id][1] += score
                        highdict[u.id][2] += icons
            high=list(highdict.values())

            rarelist = []
            for k in raredict.keys():
                rarelist.append([k, raredict[k]])
            rarelist = sorted(rarelist, key=lambda x: x[1])
            # await mf.say(context,str(rarelist))

            high = sorted(high, key=lambda x: x[1])[::-1]
            high = high
            # print(high)
            numbers = "<:bn_1:327896448232325130> <:bn_2:327896448505217037> <:bn_3:327896452363976704> <:bn_4:327896452464508929> <:bn_5:327896454733627403> <:bn_6:327896456369274880> <:bn_7:327896458067968002> <:bn_8:327896459070537728> <:bn_9:327896459292704769> <:bn_10:327896459477385226>".split(
                " ")

            lol = [["User", aesthetic.hoveremoji("Bar"), "Progress","%", "Rarest"]]
            for n, x in enumerate(high):
                lol.append([])
                u = x[0]
                limit = 16
                if len(basics.truename(bot,u)) > limit:
                    lol[-1].append(basics.truename(bot,u)[:limit - 1] + "…")
                else:
                    lol[-1].append(basics.truename(bot,u))

                prog = x[1] / cap
                lol[-1].append(ccc.bar(bot,1,prog,"mini"))
                lol[-1].append(f"{x[1]}/{cap}")
                lol[-1].append(f"{math.floor(prog * 100)}%")

                rares = ""
                addedrares = 0
                for y in rarelist:
                    if y[0] in x[2]:
                        rares += y[0]
                        addedrares += 1
                    if addedrares == 6:
                        break
                lol[-1].append(rares)

            s = "You don't have any achievements."
            for x in range(0, len(high)):
                if high[x][0] == context.message.author and high[x][1] != 0:
                    s = "You're ranked #{}.".format(x + 1)

            SortableChart(bot, validfor=datetime.timedelta(minutes=5), context=context, lol=lol, align=["l", "l","unwrap","l","l","unwrap"], addnumbers=True)

            return
        elif transfer !=  None and context.message.author == bot.rnl:
            tracking = pickle.load((open(
                'C:\\Users\\Zachary\\Desktop\\kkk\\Non-GML\\ButtBot\\epicord-bot-master\\saveach_tracking.txt', 'rb')))

            count = pickle.load(
                (open('C:\\Users\\Zachary\\Desktop\\kkk\\Non-GML\\ButtBot\\epicord-bot-master\\saveach_tracking_count.txt', 'rb')))

            achievements = AchievementBrowser.getachievements()

            for u in tracking.keys():
                for n,x in enumerate(tracking[u]):
                    for baseserver in [bot.epicord, bot.get_guild(403747701566734336)]:
                        server = "global" if achievements[n]["global"] else baseserver.id
                        if baseserver.get_member(int(u)) == None:
                            continue
                        bot.ach_tracking.setdefault(server,{})
                        bot.ach_tracking[server].setdefault(int(u),{})
                        bot.ach_tracking[server][int(u)].setdefault(n,[])
                        edit = bot.ach_tracking[server][int(u)][n]
                        for nn in range(len(achievements[n]["check"])):
                            if len(edit)<nn+1:
                                edit.append(False)
                            #
                            # print()
                            # print(edit)
                            # print(edit[nn])
                            # print(tracking[u])
                            # print(tracking[u][n])
                            # print(tracking[u][n][nn])
                            # print()
                            edit[nn] = tracking[u][n][nn] or edit[nn]

                            if u in count:
                                if (n,nn) in count[u]:
                                    bot.ach_tracking_count.setdefault(server,{})
                                    bot.ach_tracking_count[server].setdefault(int(u),{})
                                    bot.ach_tracking_count[server][int(u)].setdefault((n,nn),0)

                                    editc = bot.ach_tracking_count[server][int(u)]

                                    editc[(n,nn)] = ccc.highest([ count[u][(n,nn)] , editc[(n,nn)] ])


            await talking.say(context,"cool")
            basics.save(bot,"ach_tracking")
            basics.save(bot,"ach_tracking_count")
            return
        ####################################THE REAL DEAL!

        AchievementBrowser(bot, validfor=datetime.timedelta(minutes=10), context=context)

    @commands.command(hidden=True, pass_context=True)
    async def award(self, context):
        """Used to award achievements."""
        m=context.message
        s=m.content.replace(" ","")
        s=s.replace("s!award","")
        for x in m.mentions:
            s=s.replace(x.mention,"")
            s=s.replace(x.mention.replace("!",""),"")
            s=s.replace(x.mention.replace("@","@!"),"")
        print(s)
        for x in m.mentions:
            await AchievementBrowser.ach_check(self.bot,x,m.channel,"award",[s,m.author.id])

def setup(bot):
    bot.add_cog(Meta(bot))