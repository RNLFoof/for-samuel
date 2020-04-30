import asyncio

import modules.utility as utility

from classes.DictSavable import DictSavable
from classes.SingleButton import SingleButton
import random
from modules import talking, ot


class ObamaResidue(SingleButton):
    def __init__(self, bot, **kwargs):
        SingleButton.__init__(self, bot, **kwargs)

        defaults = {
            "otheremojis": [],
            "info": "",
            "collected": set()
        }
        self.userids = []

        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def start(self):
        m = self.context.message
        for x in (await self.context.message.channel.history(limit=20, after=m).flatten())[::-1]:
            if not x.reactions:
                m = x
                break
        self.foreignmessages.append(m)

        await SingleButton.start(self)

        for r in self.otheremojis:
            await self.foreignmessages[0].add_reaction(r)

    async def end(self):
        await utility.safelyclear(self.bot,self.foreignmessages[0], [[self.emoji]])

    async def double(self, payload):
        resinfo = self.increaseresidue(payload)
        user = self.context.message.guild.get_member(payload.user_id)
        await talking.say(self.context, resinfo + "\n\n" + self.info
        ,channel=user)

    async def single(self, payload):
        thumb = random.choice(
            ["👍","👍🏻","👍🏼","👍🏽","👍🏾","👍🏿"]
            if payload.user_id not in self.collected
            else [":pepic:487100621988560900",":pepic:487099723778621451",":pepic:487100635309670400"])
        self.increaseresidue(payload)
        await self.foreignmessages[0].add_reaction(thumb)
        await self.foreignmessages[0].remove_reaction(thumb, self.bot.me)
        await self.removeinputreaction(payload)

    def increaseresidue(self, payload):
        if payload.user_id not in self.collected:
            self.collected.add(payload.user_id)
            user = self.context.message.guild.get_member(payload.user_id)
            res = ot.residueedit(self.bot, user, 1, self.context.message.channel)
            return f"You scraped off some Obama Residue. You now have {round(res/1000, 3)} Obama Residue."
        user = self.context.message.guild.get_member(payload.user_id)
        res = ot.residueedit(self.bot, user, 0, self.context.message.channel)
        return f"You've already collected from this Obama Residue. You have {round(res/1000, 3)} Obama Residue."