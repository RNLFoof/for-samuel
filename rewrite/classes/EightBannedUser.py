import asyncio
import random

import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.Rerollable import Rerollable
from modules import talking, ccc, aesthetic


class EightBannedUser(Rerollable):
    def __init__(self,bot,**kwargs):
        Rerollable.__init__(self,bot,**kwargs)
        defaults = {
            "q": self.q,
            "l": []
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def specificroll(self):
        u = random.choice(self.l)
        name = basics.truename(self.bot, u.user)
        reason = u.reason if u.reason else "No reason given"
        self.rerolllist.append(aesthetic.hoveremoji(name))
        self.message = await talking.replystring(self.context,f"asked {basics.spitback(self.q)}, I respond: {u.user.mention} {aesthetic.hoveremoji(reason)}")
