import asyncio
import discord
import math

import modules.utility as utility

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.PageMessage import PageMessage
from modules import aesthetic

btn_num = ["<:bn_1:327896448232325130>","<:bn_2:327896448505217037>","<:bn_3:327896452363976704>","<:bn_4:327896452464508929>","<:bn_5:327896454733627403>","<:bn_6:327896456369274880>","<:bn_7:327896458067968002>","<:bn_8:327896459070537728>","<:bn_9:327896459292704769>","<:bn_10:327896459477385226>","<:bn_11:327896459586306048>","<:bn_12:327896459880169472>","<:bn_13:327896459745951745>","<:bn_14:327896460064587776>","<:bn_15:327896461473873920>","<:bn_16:327896461339787265>"]

class SortableChart(PageMessage):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "lol": [[]],
            "initialsort": [],
            "defaultreverse": set(),
            "addnumbers": False,
            "resetnumbers": None, # Do the numbers again when sorted by these. Use a set.
            "align": []
        }

        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

        if self.addnumbers:
            self.lol[0].insert(0,"#")
            for n,x in enumerate(self.lol[1:]):
                x.insert(0,n+1)

        self.pageindex = 0
        self.sortindex = {} # Used to turn reactions into which column to sort
        self.userids = [self.context.message.author.id]
        self.toprowtext = aesthetic.chart(self.lol, align=self.align).split("\n")[0]
        self.toprowlist = self.lol[0]
        self.lol = self.lol
        self.rowsperpage = math.ceil(math.floor(1900/len(self.toprowtext)))
        if self.addnumbers:
            self.rowsperpage-=self.rowsperpage%5

    async def start(self):
        for n in self.initialsort:
            self.sortchart(n,initial=True)
        self.genpages()

        await PageMessage.start(self)

        for n,x in enumerate(self.toprowlist):
            if x[0].lower() in self.bot.buttons:
                #Cycle up to five times
                i = 0
                while i!=5:
                    e = self.bot.buttons[chr(ord(x[0].lower())+i)]
                    if e.id not in self.adddict:
                        break
                    i+=1
                    print(chr(ord(x[0].lower())+i))
                    print(e.id)

                if e.id not in self.adddict:
                    asyncio.ensure_future(self.messages[0].add_reaction(e))
                    self.sortindex[e.id] = n
                    self.adddict[e.id] = self.payloadtosortchart

    async def payloadtosortchart(self,payload):
        self.sortchart(self.sortindex[payload.emoji.id])
        self.genpages()
        asyncio.ensure_future(self.removeinputreaction(payload))
        await self.updatemessage(0)

    def sortchart(self,n,initial=False):
        rem = list(self.lol)
        self.lol = sorted(self.lol, key=lambda x: x[n], reverse= n in self.defaultreverse)
        if rem == self.lol and not initial: # If it's initial then if two columns sort the same it'll flip
            self.lol = sorted(self.lol, key=lambda x: x[n], reverse=n not in self.defaultreverse)

        at = 1 # For equal values
        rem = None
        if self.resetnumbers is not None and n in self.resetnumbers:
            for m, x in enumerate(self.lol):
                if rem != x[n]:
                    at = m + 1
                rem = x[n]
                x[0] = at

    def genpages(self):
        s = aesthetic.chart(self.lol, header=False, align=self.align).strip().split("\n")[1:]
        self.pages = []
        genningpage = 0
        for n,x in enumerate(s):
            if n % self.rowsperpage == 0:
                genningpage += 1
                self.pages.append(self.toprowtext)
            self.pages[-1] = (self.pages[-1] + f"\n{x}").strip()

            print("AAA" + x)
            if (n+1) % self.rowsperpage == 0 or n+1 == len(s):
                self.pages[-1] += f"\n\nPage {genningpage}/{math.ceil(len(s)/self.rowsperpage)}"