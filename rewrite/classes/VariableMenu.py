import asyncio
import re

import discord

import modules.utility as utility

from classes.DictSavable import DictSavable
from classes.InputMenu import InputMenu
from modules import basics, aesthetic

arrow_r = "<:_:541089103551266827>"


class VariableMenu(InputMenu):
    def __init__(self,bot,**kwargs):
        InputMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "map": {},
            "position": []
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

    async def start(self):
        await InputMenu.start(self)
        for r in self.foreignmessages[0].reactions:
            async for u in r.users():
                await self.addreaction(r, u.id)
        await self.updatemessage(0)

    async def getlayout(self,index,*,final=False):
        s = ""
        page = self.getpage()
        if page["type"] == "page":
            lol = [["Name"]]
            for n,x in enumerate(page["pages"]):
                lol.append([x])
            s = aesthetic.chart(lol)

        embed = discord.Embed(type="rich", description=f"ID: {self.id}\n{s}"[:2048])
        return embed

    async def input(self, m, s):
        print(1)
        d = self.reactions
        words = re.findall(r"[^ ]+",s)
        print(words)
        for w in words[:-1]:
            print(d.keys())
            for k in d.keys():
                print(k)
                if k==w or f":{w}:" in k:
                    found = k
                    break
            else:
                return
            d = d[found]["subreactions"]
        print(2)
        newemoji = utility.get_emoji(self.bot, words[-1])
        if newemoji is None:
            aesthetic.hoveremoji(words[-1])
        newemoji = str(newemoji)
        d.setdefault(newemoji,{})
        d[newemoji].setdefault("users",[])
        d[newemoji].setdefault("subreactions",{})
        d[newemoji]["users"].append(m.author.id)
        print()
        await self.updatemessage(0)

    def getpage(self):
        ret = self.map
        for x in self.position:
            ret = ret["pages"][x]
        return ret

    def createpage(self,name,*,desc=None,cost=0):
        return {
            "type": "page",
            "name": name,
            "desc": desc,
            "cost": cost
        }