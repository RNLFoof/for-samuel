import asyncio
import random

import discord

import modules.utility as utility
import modules.ccc as ccc
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from modules import talking, ot


class SingleButton(OngoingReactionMenu):
    def __init__(self, bot, **kwargs):
        OngoingReactionMenu.__init__(self, bot, **kwargs)

        async def default(self, payload):
            pass

        defaults = {
            "anyscript": default,
            "singlescript": default,
            "doublescript": default,
            "timeoutscript": default,
            "startscript": default,
            "emoji": utility.get_emoji(bot, "628461134999191568"),
            "currentreactors": set(),
            "messagecount": 0,
        }
        self.userids = [self.context.message.author.id]
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def start(self):
        await OngoingReactionMenu.start(self)
        self.adddict[self.emoji.id] = self.added
        self.removedict[self.emoji.id] = self.removed
        await self.foreignmessages[0].add_reaction(self.emoji)

    async def end(self):
        await self.timeout()
        await OngoingReactionMenu.end(self)

    async def added(self, payload):
        self.currentreactors.add(payload.user_id)
        await self.any(payload)
        await asyncio.sleep(0.75)
        if payload.user_id in self.currentreactors:
            await self.single(payload)
        else:
            await self.double(payload)

    async def removed(self, payload):
        try:
            self.currentreactors.remove(payload.user_id)
        except:
            pass

    async def any(self, payload):
        pass

    async def single(self, payload):
        pass

    async def double(self, payload):
        pass

    async def timeout(self):
        pass