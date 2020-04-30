from datetime import datetime
from datetime import timedelta
import asyncio
import discord

import modules.talking as talking
import modules.utility as utility

from classes.DictSavable import DictSavable
from modules import basics


class OngoingReactionMenu(DictSavable):
    def __init__(self,bot,**kwargs):#validfor,adddict,removedict,messagecount,context,userids):
        # Setup
        defaults = {
            "validfor":datetime.utcnow()+timedelta(minutes=10),
            "adddict":{},
            "removedict":{},
            "messagecount": 1,
            "messages": [],
            "foreignmessages":[],
            "userids": [],
            "context": None,
            "id": None,
            "differentchannel": None,
            "disableinputs": False,
            "ended": False # Used to make sure this only finishes once
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        self.bot = bot
        # Other stuff
        self.endtime = datetime.utcnow() + kwargs["validfor"]
        asyncio.ensure_future(self.start())
    
    async def start(self):
        await self.createmessages(self.messagecount)
        asyncio.ensure_future(self.timer())
    
    async def createmessages(self,messagecount):
        for x in range(messagecount):
            new = await self.getlayout(x)
            channel = self.differentchannel if self.differentchannel != None else self.context.message.channel
            if type(new) is str:
                self.messages.append( await talking.say( self.context, new ,nowebhook=True,channel=channel) )
            else:
                self.messages.append( await talking.say( self.context, embed=new ,nowebhook=True,channel=channel) )
        self.add_reaction_menu()
    
    async def timer(self):
        while self.endtime > datetime.utcnow():
            wait = self.endtime - datetime.utcnow()
            await asyncio.sleep(wait.seconds + (24*60*60*wait.days))
        await self.end()

    # To be overwritten when a child needs an ending method.
    async def preend(self):
        pass

    async def end(self):
        if self.ended:
            return
        self.ended = True
        await self.preend()
        
        self.remove_reaction_menu()
        for x in range(len(self.messages)):
            asyncio.ensure_future( self.updatemessage(x,final=True) )
        l = []
        ul = []
        for uid in self.userids:
            ul.append(utility.get_member_or_user(self.bot, self.context.message.guild, uid))
        if ul != []:
            ul.append(utility.get_member_or_user(self.bot, self.context.message.guild, self.bot.me.id))
        
        for k in utility.nodups(list(self.adddict.keys()) + list(self.removedict.keys())):
            l.append([utility.get_emoji(self.bot, str(k))] + ul)
        
        for m in self.messages:
            await utility.safelyclear(self.bot,m,l)
        
    async def inputtest(self, payload, ar):
        if self.disableinputs:
            return
        if ar == "a":
            d = self.adddict
        if ar == "r":
            d = self.removedict
        if (payload.user_id in self.userids or self.userids == []) and payload.user_id != self.bot.me.id:
            emoji = payload.emoji
            if -1 in d.keys(): # -1 means any emoji will do
                asyncio.ensure_future(d[-1](payload))
            if emoji.is_custom_emoji() and emoji.id in d.keys():
                await d[emoji.id](payload)
            elif emoji.is_unicode_emoji() and emoji.name in d.keys():
                await d[emoji.name](payload)
                
    async def removeinputreaction(self, payload):
        for m in self.messages + self.foreignmessages:
            if m.id == payload.message_id:
                asyncio.ensure_future( m.remove_reaction(payload.emoji, self.bot.get_user(payload.user_id)) )
    
    async def getlayout(self,index,*,final=False):
        return "­"
        
    async def updatemessage(self,index,*,final=False):
        new = await self.getlayout(index, final=final)
        if type(new) is str:
            await talking.edit(self.context, self.messages[index], new)
        else:
            await talking.edit(self.context, self.messages[index], embed=new)
        print("ok guys")
        self.save()
        
    # Manage reaction menus
    def add_reaction_menu(self):
        id = 0
        bot = self.bot
        for x in bot.reactionmenus_idrm.keys():
            if x>id:
                id = x
        id += 1
        self.id = id
        for m in self.messages + self.foreignmessages:
            if m.id not in bot.reactionmenus_msgid.keys():
                 bot.reactionmenus_msgid[m.id] = []
            bot.reactionmenus_msgid[m.id].append(id)
        bot.reactionmenus_idrm[id] = self
        
    def remove_reaction_menu(self):
        bot = self.bot
        for k,i in list(bot.reactionmenus_msgid.items()):
            if self.id in i:
                bot.reactionmenus_msgid[k].remove(self.id)
            if bot.reactionmenus_msgid[k] == []:
                del bot.reactionmenus_msgid[k]
        del self.bot.reactionmenus_idrm[self.id]
        
    @staticmethod
    def get_by_id(bot,id):
        if id in bot.reactionmenus_idrm.keys():
            return bot.reactionmenus_idrm[id]
        return None
        
    @staticmethod
    def get_ids_by_mid(bot,mid):
        if mid in bot.reactionmenus_msgid.keys():
            return bot.reactionmenus_msgid[mid]
        return None

    def mintimeleft(self,time):
        setto = datetime.utcnow() + time
        if self.endtime < setto:
            self.endtime = setto

    def save(self):
        if type(self).__name__ == "EightLineFromSonic06":
            basics.thisisthethingthatactuallysaves(f"reactionmenus/{self.id}", basics.dictsavehelper(self, debug=True))