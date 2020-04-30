import asyncio
import discord

import modules.utility as utility

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu

btn_num = ["<:bn_1:327896448232325130>","<:bn_2:327896448505217037>","<:bn_3:327896452363976704>","<:bn_4:327896452464508929>","<:bn_5:327896454733627403>","<:bn_6:327896456369274880>","<:bn_7:327896458067968002>","<:bn_8:327896459070537728>","<:bn_9:327896459292704769>","<:bn_10:327896459477385226>","<:bn_11:327896459586306048>","<:bn_12:327896459880169472>","<:bn_13:327896459745951745>","<:bn_14:327896460064587776>","<:bn_15:327896461473873920>","<:bn_16:327896461339787265>"]

class PageMessage(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "pages":["­"],
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        self.pageindex = 0
        
    async def start(self):
        await OngoingReactionMenu.start(self)
        # Arrows
        emoji = utility.get_emoji(self.bot, "<:bn_ba:328062456905728002>")
        asyncio.ensure_future(self.messages[0].add_reaction( emoji ))
        self.adddict[emoji.id] = self.backpage
        
        emoji = utility.get_emoji(self.bot, "<:bn_fo:328724374465282049>")
        asyncio.ensure_future(self.messages[0].add_reaction( emoji ))
        self.adddict[emoji.id] = self.fowardpage
        # Numbers
        for x in range(len(self.pages))[:16]:
            emoji = utility.get_emoji(self.bot, btn_num[x])
            asyncio.ensure_future(self.messages[0].add_reaction( emoji ))
            self.adddict[emoji.id] = self.jumptopage
        await self.updatemessage(0)
        
    async def getlayout(self,index,*,final=False):
        #embed = discord.Embed(description=self.pages[self.pageindex])
        #return embed
        return self.pages[self.pageindex] + ["","\nThis menu has timed out. You'll need to create another one."][final]
        
    async def jumptopage(self,payload):
        await self.removeinputreaction(payload)
        self.pageindex = int(payload.emoji.name.replace("bn_",""))-1
        await self.updatemessage(0)
        
    async def fowardpage(self,payload):
        await self.removeinputreaction(payload)
        self.pageindex = (self.pageindex + 1) % len(self.pages)
        await self.updatemessage(0)
        
    async def backpage(self,payload):
        await self.removeinputreaction(payload)
        self.pageindex = (self.pageindex - 1) % len(self.pages)
        await self.updatemessage(0)