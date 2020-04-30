import asyncio
import random

import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.Rerollable import Rerollable
from modules import talking, ccc


class Choose(Rerollable):
    def __init__(self,bot,**kwargs):
        Rerollable.__init__(self,bot,**kwargs)
        # Setup
        options=[]
        totalrate=0
        title = None
        for x in self.q.split(";"):
            rate=1
            forced=False
            x, sub = basics.subcommands(self.context,x,[r"\d+|\+|-|t"])

            if sub!=None:
                sub = sub.group(1)
                if sub == "t":
                    title = x
                    continue
                elif sub == "-":
                    rate=0
                elif sub == "+":
                    forced=True
                else:
                    rate=int(sub)

            options.append({"s":x, "chance": rate,"forced":forced})
            totalrate+=rate
        defaults = {
            "options": options,
            "totalrate": totalrate,
            "title": title
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def specificroll(self):
        l=[]
        chosen = None
        countdown=random.randint(1,self.totalrate)
        if self.title==None:
            s = "Among "
            an = "and"
        else:
            s = f"{basics.spitback(self.title)}: "
            an = "or"

        for n,x in enumerate(self.options):
            l.append(f"**{chr(65+n)})** {basics.spitback(x['s'])}")
            if countdown>0 or x['forced']:
                chosen = n
                print("penis")
            if x['forced']:
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                countdown=0
            else:
                countdown-=x['chance']
        s += ccc.andstr(l,an=an)

        if self.title == None:
            s+=f", I choose: **{chr(65+chosen)})** {basics.spitback(self.options[chosen]['s'])}!"
        else:
            s+=f"? I choose: **{chr(65+chosen)})** {basics.spitback(self.options[chosen]['s'])}!"

        self.message = await talking.replystring(self.context,s)
        self.rerolllist.append(chr(65+chosen))