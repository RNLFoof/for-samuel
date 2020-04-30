import asyncio
from datetime import timedelta

import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu

btn_num = ["<:bn_1:327896448232325130>","<:bn_2:327896448505217037>","<:bn_3:327896452363976704>","<:bn_4:327896452464508929>","<:bn_5:327896454733627403>","<:bn_6:327896456369274880>","<:bn_7:327896458067968002>","<:bn_8:327896459070537728>","<:bn_9:327896459292704769>","<:bn_10:327896459477385226>","<:bn_11:327896459586306048>","<:bn_12:327896459880169472>","<:bn_13:327896459745951745>","<:bn_14:327896460064587776>","<:bn_15:327896461473873920>","<:bn_16:327896461339787265>"]

class Rerollable(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "rerolls": 0,
            "message": "",
            "rerolllist": [],
            "q": ""
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        
    async def start(self):
        await OngoingReactionMenu.start(self)
        emoji = utility.get_emoji(self.bot, "<:bn_re:362741439211503616>")
        asyncio.ensure_future(self.messages[0].add_reaction( emoji ))
        self.adddict[emoji.id] = self.reroll
        await self.specificroll()
        await self.updatemessage(0)
        
    async def getlayout(self,index,*,final=False):
        s = self.message + "\n"
        if self.rerolls != 0:
            s += f"\nRerolls: {self.rerolls}"
        if len(self.rerolllist) > 1:
            s += f"\nPrevious rolls: {', '.join(self.rerolllist[:-1])}"
        s += "\nHit <:bn_re:362741439211503616> to reroll."
        return s

    async def reroll(self,payload):
        self.rerolls += 1
        self.rerolllist = self.rerolllist[-10:]
        await self.specificroll()
        await self.updatemessage(0)
        await self.removeinputreaction(payload)
        self.mintimeleft(timedelta(minutes=10))

    async def specificroll(self):
        pass