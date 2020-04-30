import asyncio

import modules.talking as talking
import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu

class Sue(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "suer":None,
            "suee":None,
            "reason":""
        }
        self.innocentlist = []
        self.guiltylist = []
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        
    async def start(self):
        await OngoingReactionMenu.start(self)
        
        for x in ["331164189399711767","331164189039132673"]:
            emoji = utility.get_emoji(self.bot, x)
            asyncio.ensure_future(self.messages[0].add_reaction( emoji ))
            self.adddict[emoji.id] = self.addvote
            self.removedict[emoji.id] = self.removevote
            
    async def end(self):
        asyncio.ensure_future( OngoingReactionMenu.end(self) )
        
        i = ""
        g = ""
        ip = 0 # Innocent Points
        gp = 0
        for x in self.innocentlist:
            i += f"    <@{x}>\n"
            ip += 1
        for x in self.guiltylist:
            g += f"    <@{x}>\n"
            gp += 1
        p = gp - ip # Actual guilty points
            
        if p > 0: # Guilty
            self.bot.suepoints[self.context.guild.id][self.suer.id]["suerwin"] += p
            self.bot.suepoints[self.context.guild.id][self.suee.id]["sueelose"] += p
        elif p < 0: # Innocent
            self.bot.suepoints[self.context.guild.id][self.suer.id]["suerlose"] += abs(p)
            self.bot.suepoints[self.context.guild.id][self.suee.id]["sueewin"] += abs(p)
        basics.save(self.bot, "suepoints")
            
        await talking.say(self.context, f"""The results of {self.suer.mention} attempting to sue {self.suee.mention} are in!
**Reason:** {self.reason}

Innocent:
{i}­
Guilty:
{g}­""")
        
    async def getlayout(self,index,*,final=False):
        i = ""
        g = ""
        for x in self.innocentlist:
            i += basics.useremoji(self.bot, utility.get_member_or_user(self.bot, self.messages[0].guild, x))
        for x in self.guiltylist:
            g += basics.useremoji(self.bot, utility.get_member_or_user(self.bot, self.messages[0].guild, x))
        
        return f"""{self.suer.mention} is attempting to sue {self.suee.mention}!
**Reason:** {self.reason}

Vote now on your phones!
Innocent:
    {i}­
Guilty:
    {g}­"""
        
    async def addvote(self,payload):
        if payload.user_id in [self.suer.id, self.suee.id]:
            return
        # Remove other reaction
        if payload.emoji.name == "bn_i":
            asyncio.ensure_future(self.messages[0].remove_reaction(utility.get_emoji(self.bot,"331164189039132673"),self.bot.get_user(payload.user_id)))
            a = self.innocentlist
        if payload.emoji.name == "bn_g":
            asyncio.ensure_future(self.messages[0].remove_reaction(utility.get_emoji(self.bot,"331164189399711767"),self.bot.get_user(payload.user_id)))
            a = self.guiltylist
        # Modify list
        id = payload.user_id
        while id in self.guiltylist:
            self.guiltylist.remove(id)
        while id in self.innocentlist:
            self.innocentlist.remove(id)
        a.append(id)
        
        await self.updatemessage(0)
        
    async def removevote(self,payload):
        if payload.user_id in [self.suer.id, self.suee.id]:
            return
        # Modify list
        id = payload.user_id
        if payload.emoji.name == "bn_g":
            while id in self.guiltylist:
                self.guiltylist.remove(id)
        if payload.emoji.name == "bn_i":
            while id in self.innocentlist:
                self.innocentlist.remove(id)
        
        await self.updatemessage(0)
        
    @staticmethod
    def getstats(bot, member):
        getfrom = bot.suepoints[member.guild.id][member.id]
        try:
            getfrom = bot.suepoints[member.guild.id][member.id]
        except:
            return {"Dick Inches":0, "Overall":0}
        return {
            "Dick Inches": -getfrom["sueelose"],
            "Overall": getfrom["suerwin"] + getfrom["sueewin"] - getfrom["suerlose"] - getfrom["sueelose"]
        }