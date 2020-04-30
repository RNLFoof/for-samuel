import asyncio
import random

import discord

import modules.utility as utility
import modules.ccc as ccc
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.SingleButton import SingleButton
from modules import talking, ot


class OnTheFlySingleButton(SingleButton):
    def __init__(self, bot, **kwargs):
        OngoingReactionMenu.__init__(self, bot, **kwargs)

        async def default(self, payload):
            pass

        async def defaultnopayload(self):
            pass

        defaults = {
            "anyscript": default,
            "singlescript": default,
            "doublescript": default,
            "timeoutscript": default,
            "startscript": defaultnopayload
        }
        self.userids = [self.context.message.author.id]
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def start(self):
        await SingleButton.start(self)
        await self.startscript(self)

    async def any(self, payload):
        await self.anyscript(self, payload)

    async def single(self, payload):
        await self.singlescript(self, payload)

    async def double(self, payload):
        await self.doublescript(self, payload)

    async def timeout(self):
        await self.timeoutscript(self)