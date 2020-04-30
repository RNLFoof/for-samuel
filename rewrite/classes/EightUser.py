import asyncio
import random

import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.Rerollable import Rerollable
from modules import talking, ccc, aesthetic


class EightUser(Rerollable):
    def __init__(self,bot,**kwargs):
        Rerollable.__init__(self,bot,**kwargs)
        defaults = {
            "q": self.q
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def specificroll(self):
        u = random.choice(utility.getcoolpeople(self.bot, self.context.message.guild, priority="medium"))
        self.rerolllist.append(basics.useremoji(self.bot, u, guild=self.context.message.guild))
        self.message = await talking.replystring(self.context, f"asked {basics.spitback(self.q)}, I respond: {ccc.repuser(self.bot, u)}")
