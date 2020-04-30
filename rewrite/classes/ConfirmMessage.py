import asyncio
import random

import discord

import modules.utility as utility
import modules.ccc as ccc
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from modules import talking, ot

btn_num = ["<:bn_1:327896448232325130>","<:bn_2:327896448505217037>","<:bn_3:327896452363976704>","<:bn_4:327896452464508929>","<:bn_5:327896454733627403>","<:bn_6:327896456369274880>","<:bn_7:327896458067968002>","<:bn_8:327896459070537728>","<:bn_9:327896459292704769>","<:bn_10:327896459477385226>","<:bn_11:327896459586306048>","<:bn_12:327896459880169472>","<:bn_13:327896459745951745>","<:bn_14:327896460064587776>","<:bn_15:327896461473873920>","<:bn_16:327896461339787265>"]

class ConfirmMessage(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)

        # Setup
        if random.randint(1,100) == 1:
            btn_yes = utility.get_emoji(bot,"<:upstinky:288858540888686602>")
            btn_no = utility.get_emoji(bot,"<:downstinky:288858539332599808>")
        else:
            btn_yes = utility.get_emoji(bot,"<:bn_yes:331164192864206848>")
            btn_no = utility.get_emoji(bot,"<:bn_no:331164190284972034>")

        async def default(self):
            pass

        async def defaultno(self):
            self.message='THEN DIE'

        defaults = {
            "message": "Hit YES to confirm. Hit NO to uh, die.",
            "yesscript": default,
            "noscipt": defaultno,
            "timeoutscript": default,
            "btn_yes": btn_yes,
            "btn_no": btn_no,
            "cost": 0
        }
        self.userids = [self.context.message.author.id]
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

        # Remove if broke
        ots = ot.otedit(self.bot, self.context.message.author, 0, False, channel=self.context.message.channel)
        if ots < self.cost:
            self.message = f"You need {ccc.pluralstr('Obama Token', self.cost)} to do this, but you only have {ots}."
            asyncio.ensure_future(self.end())
            return
        
    async def start(self):
        await OngoingReactionMenu.start(self)
        asyncio.ensure_future(self.messages[0].add_reaction( self.btn_yes ))
        self.adddict[self.btn_yes.id] = self.runscript
        asyncio.ensure_future(self.messages[0].add_reaction( self.btn_no ))
        self.adddict[self.btn_no.id] = self.runscript
        await self.updatemessage(0)

    async def runscript(self, payload):
        if payload.emoji.name == "bn_yes":
            if self.cost != 0 and ot.otedit(self.bot, self.context.message.author, 0, False, channel=self.context.message.channel)<self.cost:
                self.message = f"You no longer have the {ccc.pluralstr('Obama Token',self.cost)} required to do this."
            else:
                await self.yesscript(self)
        elif payload.emoji.name == "bn_no":
            await self.noscipt(self)
        await self.end()

    async def getlayout(self,index,*,final=False):
        return await talking.replystring(self.context, self.message.replace("YES",str(self.btn_yes)).replace("NO",str(self.btn_no)))