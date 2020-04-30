import asyncio
import discord

import modules.utility as utility

from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from modules import basics

class InputMenu(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        self.guildid = kwargs["context"].message.guild.id
        self.channelid = kwargs["context"].message.channel.id
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        self.btn_write = utility.get_emoji(bot,"<:bn_xat:331164192793165824>")

    async def createmessages(self, messagecount):
        self.add_input_menu_start()
        await OngoingReactionMenu.createmessages(self, messagecount)
        self.add_input_menu_end()

    def add_input_menu_start(self):
        id = 0
        bot = self.bot
        bot.inputmenus_serverids.setdefault(self.guildid, set())
        while id in bot.inputmenus_serverids[self.guildid]:
            id+=1
        bot.inputmenus_serverids[self.guildid].add(id)

        bot.inputmenus_channelids.setdefault(self.channelid, [])
        bot.inputmenus_channelids[self.channelid].append(id)

        self.id = id

    def add_input_menu_end(self):
        bot = self.bot
        for m in self.messages:
            bot.inputmenus_msgid.setdefault(m.id, [])
            bot.inputmenus_msgid[m.id].append(self.id)

        bot.inputmenus_idim[self.id] = self

    def remove_reaction_menu(self):
        OngoingReactionMenu.remove_reaction_menu(self)
        self.remove_input_menu()

    def remove_input_menu(self):
        bot = self.bot
        for k,i in list(bot.inputmenus_msgid.items()):
            if self.id in i:
                bot.inputmenus_msgid[k].remove(self.id)
            if bot.inputmenus_msgid[k] == []:
                del bot.inputmenus_msgid[k]
        del self.bot.inputmenus_idim[self.id]

        bot.inputmenus_channelids[self.channelid].remove(self.id)
        if len(bot.inputmenus_channelids[self.channelid]) == 0:
            del bot.inputmenus_msgid[self.channelid]

        bot.inputmenus_serverids[self.guildid].remove(self.id)
        if len(bot.inputmenus_serverids[self.guildid]) == 0:
            del bot.inputmenus_serverids[self.guildid]

    async def inputmessage(self, m):
        await self.input(m, m.content)

    async def input(self,m,s):
        pass
