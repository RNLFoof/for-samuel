import asyncio
import re

import discord

import modules.utility as utility

from classes.DictSavable import DictSavable
from classes.InputMenu import InputMenu
from modules import basics, aesthetic

arrow_r = "<:_:541089103551266827>"

class Help(InputMenu):
    def __init__(self,bot,**kwargs):
        InputMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "show": ""
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def getlayout(self,index,*,final=False):
        return await basics.help(self.context, self.show, False)

    async def start(self):
        await InputMenu.start(self)
        for x in range(1,17):
            await self.messages[0].add_reaction(self.bot.buttons[str(x)])
            self.adddict[self.bot.buttons[str(x)].id] = self.numberbutton

    async def input(self, m, s):
        self.show = s
        await self.updatemessage(0)

    async def reactionadded(self,payload):
        if payload.message_id == self.foreignmessages[0].id:
            await self.addreaction(payload.emoji, payload.user_id)
            await self.updatemessage(0)

    async def numberbutton(self,payload):
        print("heh")