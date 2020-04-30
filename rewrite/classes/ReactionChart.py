import asyncio
import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu

btn_num = ["<:bn_1:327896448232325130>","<:bn_2:327896448505217037>","<:bn_3:327896452363976704>","<:bn_4:327896452464508929>","<:bn_5:327896454733627403>","<:bn_6:327896456369274880>","<:bn_7:327896458067968002>","<:bn_8:327896459070537728>","<:bn_9:327896459292704769>","<:bn_10:327896459477385226>","<:bn_11:327896459586306048>","<:bn_12:327896459880169472>","<:bn_13:327896459745951745>","<:bn_14:327896460064587776>","<:bn_15:327896461473873920>","<:bn_16:327896461339787265>"]

class ReactionChart(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        DictSavable.__init__(self, {}, kwargs, exclude=["validfor"])
        
    async def start(self):
        await OngoingReactionMenu.start(self)
        self.adddict[-1] = self.emojichanged
        self.removedict[-1] = self.emojichanged
        await self.updatemessage(0)
        
    async def getlayout(self,index,*,final=False):
        bot = self.bot
        m = self.context.message
        s = f"[<a:hippovortex:395505717374877696>]({self.foreignmessages[0].jump_url})"
        mfrom = await self.foreignmessages[0].channel.get_message(self.foreignmessages[0].id)
        reactdict = {}
        userlist = []
        for r in mfrom.reactions:
            e = await utility.hasemoji(bot,r.emoji)
            reactdict[e] = []
            async for u in r.users():
                ae = basics.useremoji(bot, u, guild=m.guild)
                reactdict[e].append(ae)
                userlist.append(ae)
        
        userlist = utility.nodups(userlist)
        s += "".join(userlist)
        for k,i in reactdict.items():
            s += f"\n{k}"
            for u in userlist:
                s += ["▪","⭕"][u in i]
                
        return discord.Embed(type="rich", description = s + ["","\nThis chart has timed out. You'll need to create another one."][final])
        
    async def emojichanged(self,payload):
        if payload.message_id == self.foreignmessages[0].id:
            await self.updatemessage(0)