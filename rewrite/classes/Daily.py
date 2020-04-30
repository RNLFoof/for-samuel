import asyncio
from datetime import datetime
import random

import modules.talking as talking
import modules.utility as utility
import modules.basics as basics
from classes.AchievementBrowser import AchievementBrowser

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from modules.ot import otedit


class Daily(OngoingReactionMenu):
    def __init__(self, bot, **kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "differentchannel": self.bot.epicord.get_channel(488516474735034389) if self.context.message.guild.id==self.bot.epicord.id else None
        }
        self.userids = [self.context.message.author.id]
        self.personpicked = None
        self.bot.sdailylast[self.context.message.guild.id][str(self.context.message.author.id)] = str(datetime.utcnow().date())
        basics.save(self.bot, "sdailylast")
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        
    async def start(self):
        emojis = {} # People to emojis

        peoplemedium = utility.getcoolpeople(self.bot, self.context.message.guild, priority="medium")
        random.shuffle(peoplemedium)
        for x in list(peoplemedium):
            if x.bot:
                peoplemedium.remove(x)
            elif basics.useremoji(self.bot, x, default="aes",actualemoji=True) in emojis.values():
                peoplemedium.remove(x)
            else:
                emojis[x.id] = basics.useremoji(self.bot, x, default="aes",actualemoji=True)

        peoplelow = utility.getcoolpeople(self.bot, self.context.message.guild, priority="low")
        random.shuffle(peoplelow)
        for x in list(peoplelow):
            if x.bot:
                peoplelow.remove(x)
            elif basics.useremoji(self.bot, x, default="aes",actualemoji=True) in emojis.values():
                peoplelow.remove(x)
            else:
                emojis[x.id] = basics.useremoji(self.bot, x, default="aes",actualemoji=True)

        self.people = [peoplelow[0], peoplemedium[0], peoplemedium[1]]
        random.shuffle(self.people)

        await OngoingReactionMenu.start(self)

        self.edict={} # Emoji IDs to people
        for x in self.people:
            asyncio.ensure_future(self.messages[0].add_reaction(emojis[x.id]))
            self.edict[emojis[x.id].id] = x
            self.adddict[emojis[x.id].id] = self.givetoken
        print(self.adddict.keys())

    async def givetoken(self,payload):
        self.disableinputs = True
        self.personpicked = self.edict[payload.emoji.id]
        otedit(self.bot, self.personpicked, 1, True, channel=self.messages[0].channel, type="daily")
        await talking.reply(self.context, f"You've given a token to {self.personpicked.mention}.",channel=self.messages[0].channel)
        await AchievementBrowser.ach_check(self.bot, self.context.message.author, self.context.message.channel, "daily", [self.personpicked])
        print(self.personpicked)
        print(self.context.message.author)
        await AchievementBrowser.ach_check(self.bot, self.personpicked, self.context.message.channel, "dailyrecieved", [self.context.message.author])
        await self.end()

    async def getlayout(self,index,*,final=False):
        crossout = "~~" if self.personpicked != None else ""
        return f"""{self.context.message.author.mention}: {crossout}Pick {basics.truename(self.bot, self.people[0])}, {basics.truename(self.bot, self.people[1])}, or {basics.truename(self.bot, self.people[2])} to give them a token.{crossout}
""" + ("" if not final else ("This menu has timed out. Way to go.\n" if self.personpicked== None else f"{self.personpicked.mention} was chosen.\n")) + f"""Back to the trigger channel: {self.context.message.channel.mention}"""