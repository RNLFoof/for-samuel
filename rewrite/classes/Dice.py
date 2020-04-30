import asyncio
import random

import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.Rerollable import Rerollable
from modules import talking, ccc


class Dice(Rerollable):
    def __init__(self,bot,**kwargs):
        Rerollable.__init__(self,bot,**kwargs)
        # Setup
        self.q, eo = basics.subcommands(self.context,self.q,[r"equaloutcome|eo"])
        defaults = {
            "die": [6],
            "outcomes": [],
            "eo": eo
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def specificroll(self):
        self.generateoutcomes()
        popped = self.outcomes.pop(random.randint(0,len(self.outcomes)-1))
        self.message = await talking.replystring(self.context,popped)
        self.rerolllist.append("LOL")
        print(self.outcomes)

    def generateoutcomes(self):
        if len(self.outcomes) == 0:
            for x in range(1,7):
                for y in range(1,7):
                    self.outcomes.append(f"{x}/6 + {y}/6 = {x+y}")