import asyncio
from datetime import datetime
from datetime import timedelta

import discord

import modules.utility as utility
import modules.basics as basics
from classes.AchievementBrowser import AchievementBrowser

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.SingleButton import SingleButton
from modules import ot, talking, aesthetic, ccc

btn_num = ["<:bn_1:327896448232325130>","<:bn_2:327896448505217037>","<:bn_3:327896452363976704>","<:bn_4:327896452464508929>","<:bn_5:327896454733627403>","<:bn_6:327896456369274880>","<:bn_7:327896458067968002>","<:bn_8:327896459070537728>","<:bn_9:327896459292704769>","<:bn_10:327896459477385226>","<:bn_11:327896459586306048>","<:bn_12:327896459880169472>","<:bn_13:327896459745951745>","<:bn_14:327896460064587776>","<:bn_15:327896461473873920>","<:bn_16:327896461339787265>"]

class ObamaSilver(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "collectors": set()
        }
        self.obamasilver = utility.get_emoji(bot, ":obamasilverpile:349449386692050944")
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        
    async def start(self):
        await OngoingReactionMenu.start(self)

        bot=self.bot
        context=self.context
        m=context.message

        self.adddict[self.obamasilver.id] = self.collect
        asyncio.ensure_future(self.foreignmessages[0].add_reaction(self.obamasilver))

    async def preend(self):
        if self.collectors:
            bot = self.bot
            context = self.context
            m = context.message

            asyncio.ensure_future(utility.safelyclear(self.bot, self.foreignmessages[0], [[self.obamasilver]]))

            fullcollectors = set()
            for u in self.collectors:
                fullcollectors.add(self.context.message.guild.get_member(u))

            names = ""
            for u in fullcollectors:
                names += f"{ccc.shownames(self.bot, u)}\n"
                ot.otedit(bot, u, 0.2, True, channel=m.channel, type="silver", extras=
                {
                    "collectors": fullcollectors,
                    "allthesame": all(qwerty.display_name == next(iter(fullcollectors)).display_name for qwerty in fullcollectors)
                })
            s = f"<:obamasilver:349436656236888066> The following users have collected from the pile of Obama Silver and got 0.2 Obama Tokens:\n{names}"
            await talking.say(self.context, aesthetic.indentlist(s))

    async def collect(self,payload):
        context = self.context
        m = context.message
        u = m.guild.get_member(payload.user_id)
        if u.bot:
            return

        if not self.collectors:
            self.endtime = datetime.utcnow() + timedelta(seconds=10)
            asyncio.ensure_future(self.timer())

        self.collectors.add(u.id)