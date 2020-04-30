import asyncio
import random

import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.Rerollable import Rerollable
from modules import talking, ccc, aesthetic


class EightLineFromSonic06(Rerollable):
    def __init__(self,bot,**kwargs):
        Rerollable.__init__(self,bot,**kwargs)
        defaults = {
            "q": self.q
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def specificroll(self):
        line = ccc.eightlinefromsonic0()
        self.rerolllist.append(aesthetic.hoveremoji(line))
        self.message = await talking.replystring(self.context,f"asked {basics.spitback(self.q)}, I respond: {line}")
