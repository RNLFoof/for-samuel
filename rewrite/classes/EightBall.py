import asyncio
import random

import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.Rerollable import Rerollable
from modules import talking, ccc


class EightBall(Rerollable):
    def __init__(self,bot,**kwargs):
        Rerollable.__init__(self,bot,**kwargs)
        self.q, ratio = basics.subcommands(self.context, self.q, [r"yes|yeah|ya|yeh|ye|yup|y|no|nah|nope|n|(\d)(?:\||\/|;|:)(\d)"],
           riggedaliases=[
               {
                   "regex": r"8?(yes|yeah|ya|yeh|ye|yup|y)",
                   "slot": 0,
                   "value": "y"
               },
               {
                   "regex": r"8?(no|nah|nope|n)",
                   "slot": 0,
                   "value": "n"
               }
           ])

        if ratio:
            if ratio.group(1).startswith("y"):
                y = 1
                n = 0
            elif ratio.group(1).startswith("n"):
                y = 0
                n = 1
            else:
                y = int(ratio.group(2))
                n = int(ratio.group(3))
        else:
            y = 1
            n = 1
        defaults = {
            "q": self.q,
            "yesratio": y,
            "noratio": n
        }
        kwargs["q"] = self.q
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def specificroll(self):
        if abs(hash(self.q)) % 100 == 0:
            self.rerolllist.append("🖕")
            self.message = await talking.replystring(self.context,
                                                     f"asked {basics.spitback(self.q)}, I respond: Some questions are better left unanswered. (🖕)")
        elif self.yesratio + self.noratio == 0:
            self.rerolllist.append("M")
            self.message = await talking.replystring(self.context,f"asked {basics.spitback(self.q)}, I respond: {ccc.eightmaybe()} (Maybe)")
        elif random.randint(1,self.yesratio + self.noratio) <= self.yesratio:
            self.rerolllist.append("Y")
            self.message = await talking.replystring(self.context, f"asked {basics.spitback(self.q)}, I respond: {ccc.eightyes()} (Yes)")
        else:
            self.rerolllist.append("N")
            self.message = await talking.replystring(self.context, f"asked {basics.spitback(self.q)}, I respond: {ccc.eightno()} (No)")
