import asyncio
import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu

btn_num = ["<:bn_1:327896448232325130>","<:bn_2:327896448505217037>","<:bn_3:327896452363976704>","<:bn_4:327896452464508929>","<:bn_5:327896454733627403>","<:bn_6:327896456369274880>","<:bn_7:327896458067968002>","<:bn_8:327896459070537728>","<:bn_9:327896459292704769>","<:bn_10:327896459477385226>","<:bn_11:327896459586306048>","<:bn_12:327896459880169472>","<:bn_13:327896459745951745>","<:bn_14:327896460064587776>","<:bn_15:327896461473873920>","<:bn_16:327896461339787265>"]

class FlockOfInvites(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "sl": []
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        self.step = 0
        
    async def start(self):
        await OngoingReactionMenu.start(self)
        # Arrows
        emoji = utility.get_emoji(self.bot, "<:bn_do:328724374498836500>")
        asyncio.ensure_future(self.messages[0].add_reaction( emoji ))
        self.adddict[emoji.id] = self.confirm
        # await self.updatemessage(0)
        
    async def getlayout(self,index,*,final=False):
        s = ""
        if self.step == 2:
            for g in self.sl:
                for c in sorted(g.text_channels, key= lambda x: x==g.system_channel):
                    try:
                        inv = await c.create_invite(max_age=600, reason=f"Requested by {basics.truename(self.bot, self.context.message.author)} as part of a s!flockofinvites.")
                        s += f"{g.name}: {inv.url}\n"
                        break
                    except:
                        pass
                else:
                    s += f"Unable to get invite for {g.name}.\n"

        elif self.step == 0:
            s="Hit <:bn_do:328724374498836500> if you're okay with posting invites to all the following servers:\n"
            for g in self.sl:
                s += f"{g.name}\n"
            s += ["", "This menu has timed out. You'll need to create another one."][final]
        else:
            s = "Alrighty. It might take a bit to get the invites."
        return s

    async def confirm(self,payload):
        self.step = 1
        await self.updatemessage(0)
        self.step = 2
        await self.end()
        
