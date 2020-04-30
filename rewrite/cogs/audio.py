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

class Audio(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True,aliases=["audie","xat"])
    async def audies(self, context):
        """Uploads a chosen audie.
        
        Modifiers:
        all|list : Display all audies."""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content,split=True)
        audies = ccc.allaudies()
        # print(len(audies))

        if len(q)==0:
            await talking.reply(context,f"Please specify an audie! Use `s!audie [list]` for a list.")
            return
        q, all = basics.subcommands(context, q[0],["all|list"])
        q = re.sub(r"[^A-Za-z0-9]","",q)

        if all!=None:
            pages = []
            n = 0
            #for a in range(8):
            page = []
            for b in range(19*8):
                page.append([])
                for c in range(4):
                    page[-1].append(audies[n])
                    n += 1
            for n,x in enumerate(aesthetic.chart(page,header=False,linelimit=19)):
                pages.append(f"__**Audie List**__ (Page {n+1}/8)\n{x}")
            rm = PageMessage(bot, validfor=datetime.timedelta(minutes=5), messagecount=1, userids = [m.author.id], pages=pages, context=context)
            #utility.add_reaction_menu(bot,rm)
            #bot.ongoingreactionmenus.append(new)
            #new.test()
            #basics.save(bot,"ongoingreactionmenus")
        elif q.lower() not in audies:
            await talking.reply(context,f"There's no audie called {basics.spitback(q)}.")
        else:
            with open(f"audio/audies/{q}.mp3", "rb") as f:
                await talking.say(context,f"#{q.title()}",file=f)

    @commands.command(pass_context=True,name="8audies",aliases=["8audie","8xat"])
    async def eightaudies(self, context):
        """Answers with a random XRA audie."""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content , split=False)
        audie = ccc.eightaudie()
        with open(f"audio/audies/{audie}.mp3", "rb") as f:
            await talking.reply(context,'asked {}, I respond: #{}!'.format(basics.spitback(q),audie.title()),file=f)

def setup(bot):
    bot.add_cog(Audio(bot))