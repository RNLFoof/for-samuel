import asyncio
import re

import discord

import modules.utility as utility

from classes.DictSavable import DictSavable
from classes.InputMenu import InputMenu
from modules import basics, aesthetic

arrow_r = "<:_:541089103551266827>"


class ReactionReactions(InputMenu):
    def __init__(self,bot,**kwargs):
        InputMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {

        }
        self.reactions = {}
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        self.adddict[-1] = self.reactionadded

    async def start(self):
        await InputMenu.start(self)
        for r in self.foreignmessages[0].reactions:
            async for u in r.users():
                await self.addreaction(r, u.id)
        await self.updatemessage(0)

    async def getlayout(self,index,*,final=False):
        ul = set()
        def getallusersandotherstuff(d, maxlevel, currentlevel):
            if maxlevel < currentlevel:
                maxlevel = currentlevel
            for i in d.values():
                print(i["subreactions"])
                ul.update(i["users"])
                maxlevel = getallusersandotherstuff(i["subreactions"], maxlevel, currentlevel+1)
                # for u in i["subreactions"]:
                #     getallusers(u)
            return maxlevel

        maxlevels = getallusersandotherstuff(self.reactions,0,0)
        s = f"[<a:hippovortex:395505717374877696>]({self.foreignmessages[0].jump_url}){'▪'*(maxlevels-1)}│"

        for u in ul:
            print(u)
            s += basics.useremoji(self.bot, utility.get_member_or_user(self.bot, self.bot.get_guild(self.guildid), u))

        def displayreactions(s,d,level,maxlevels):
            for k,i in d.items():
                s += f"\n{arrow_r*level}{k}{'▪'*(maxlevels-level-1)}│"
                print(i["users"])
                for u in ul:
                    s += "⭕" if u in i["users"] else "▪"
                s = displayreactions(s, i["subreactions"],level+1,maxlevels)
            return s

        s=displayreactions(s,self.reactions,0,maxlevels)
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

    async def reactionadded(self,payload):
        if payload.message_id == self.foreignmessages[0].id:
            await self.addreaction(payload.emoji, payload.user_id)
            await self.updatemessage(0)

    async def addreaction(self, reaction, user):
        reaction = str(reaction)
        self.reactions.setdefault(reaction,{})
        self.reactions[reaction].setdefault("users",[])
        self.reactions[reaction].setdefault("subreactions",{})
        self.reactions[reaction]["users"].append(user)
