import asyncio
import discord

import modules.utility as utility
from classes.AchievementBrowser import AchievementBrowser

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from modules import aesthetic, ccc

btn_num = ["<:bn_1:327896448232325130>","<:bn_2:327896448505217037>","<:bn_3:327896452363976704>","<:bn_4:327896452464508929>","<:bn_5:327896454733627403>","<:bn_6:327896456369274880>","<:bn_7:327896458067968002>","<:bn_8:327896459070537728>","<:bn_9:327896459292704769>","<:bn_10:327896459477385226>","<:bn_11:327896459586306048>","<:bn_12:327896459880169472>","<:bn_13:327896459745951745>","<:bn_14:327896460064587776>","<:bn_15:327896461473873920>","<:bn_16:327896461339787265>"]

class Petition(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "emoji":"<a:rolling:393641477068029953>",
            "q":"­",
            "lit":False
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        self.pageindex = 0

        self.words = "**" + self.q + "**"
        self.names = ""
        self.idlist = []  # For achievements
        self.idlistnoremove = []  # For achievements
        self.header = "\nPetition started by " + self.context.message.author.mention + ".\n\n"
        self.signtut = f"Hit {self.emoji} to sign.\n"
        self.footer = "Total signatures: "
        self.poweredup = False
        
    async def start(self):
        await OngoingReactionMenu.start(self)
        # Arrows
        asyncio.ensure_future(self.messages[0].add_reaction( self.emoji ))
        self.adddict[self.emoji.id] = self.sign
        self.removedict[self.emoji.id] = self.unsign

        await self.updatemessage(0)

    async def preend(self):
        await AchievementBrowser.ach_check(self.bot, self.context.message.author, self.context.message.channel,
                                           "petitionend", {"idlist":self.idlist, "lit":self.lit})
        await OngoingReactionMenu.end(self)

    async def getlayout(self,index,*,final=False):
        return self.words+\
               (" 🔥" if self.lit else "")+\
               self.header+\
               aesthetic.indentlist(self.names)+\
               "\n\n"+\
               ("" if final else self.signtut)+\
               self.footer+\
               str(self.names.count("\n")) +\
               ["","\nThis petition has timed out. You'll need to create another one."][final]

    async def sign(self, payload):
        if (str(payload.user_id) not in self.names or self.poweredup) and payload.user_id != 309960863526289408:
            self.names += f"<@{payload.user_id}>\n"
            firsttime = payload.user_id not in self.idlistnoremove
            if payload.user_id not in self.idlist:
                self.idlist.append(payload.user_id)
            if payload.user_id not in self.idlistnoremove:
                self.idlistnoremove.append(payload.user_id)
            await self.updatemessage(0)
            await AchievementBrowser.ach_check(self.bot, self.context.message.author, self.context.message.channel,
                                               "petition", [self.idlist])
            if payload.user_id not in self.idlistnoremove:
                await AchievementBrowser.ach_check(self.bot, self.context.guild.get_member(payload.user_id),
                                                   self.context.message.channel, "petitionsig", [self.idlist,self.idlistnoremove,firsttime])


    async def unsign(self,payload):
        if str(payload.user_id) in self.names and not self.poweredup:
            self.names = "".join(self.names.split(f"<@{payload.user_id}>\n"))
            while payload.user_id in self.idlist:
                self.idlist.remove(payload.user_id)
            await self.updatemessage(0)