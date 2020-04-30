import asyncio
from datetime import datetime
from datetime import timedelta

import discord

import modules.utility as utility
import modules.basics as basics

from classes.DictSavable import DictSavable
from classes.ObamaResidue import ObamaResidue
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.SingleButton import SingleButton
from modules import ot, talking, aesthetic, ccc

btn_num = ["<:bn_1:327896448232325130>","<:bn_2:327896448505217037>","<:bn_3:327896452363976704>","<:bn_4:327896452464508929>","<:bn_5:327896454733627403>","<:bn_6:327896456369274880>","<:bn_7:327896458067968002>","<:bn_8:327896459070537728>","<:bn_9:327896459292704769>","<:bn_10:327896459477385226>","<:bn_11:327896459586306048>","<:bn_12:327896459880169472>","<:bn_13:327896459745951745>","<:bn_14:327896460064587776>","<:bn_15:327896461473873920>","<:bn_16:327896461339787265>"]

class ObamaToken(OngoingReactionMenu):
    def __init__(self,bot,**kwargs):
        OngoingReactionMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {
            "disrespectcount": {},
            "delayed": False
        }
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])
        
    async def start(self):
        await OngoingReactionMenu.start(self)

        bot=self.bot
        context=self.context
        m=context.message

        obamatoken = utility.get_emoji(bot, "a:spinningobamatoken:394587421687152640")
        self.adddict[obamatoken.id] = self.collect
        asyncio.ensure_future(self.foreignmessages[0].add_reaction(obamatoken))

    async def end(self):
        asyncio.ensure_future(utility.safelyclear(self.bot, self.foreignmessages[0], [[utility.get_emoji(self.bot, "a:spinningobamatoken:394587421687152640")]]))
        await OngoingReactionMenu.end(self)

    async def collect(self,payload):
        bot=self.bot
        context = self.context
        m = context.message
        u = m.guild.get_member(payload.user_id)
        tokeninfo = f"Spawn Message ID; {context.message.id}"
        if u.bot:
            return

        self.disrespectcount.setdefault(u.id,0)
        if payload.emoji.is_unicode_emoji() or payload.emoji.id != 394587421687152640:
            self.disrespectcount[u.id] += 1
            return
        tokeninfo += f"\nDisrespect Count; {self.disrespectcount[u.id]}"
        self.disableinputs = True
        recentspeaker = False

        timestr = '%Y/%m/%d  %I:%M:%S %p'
        uh = datetime.utcnow() - timedelta(seconds=30)
        if m.created_at <= uh and m.author.id != u.id and not m.author.bot:
                recentspeaker = True
                tokeninfo += f"\nRecent Speaker Message ID; {m.id}\nRecent Speaker Message Timestamp; {m.created_at.strftime(timestr)}"
        else:
            async for msg in m.channel.history(limit=60, oldest_first=False, before=m):
                recentspeaker = False
                if msg.created_at <= uh:
                    break
                if msg.author.id != u.id and not msg.author.bot:
                    recentspeaker = True
                    tokeninfo += f"\nRecent Speaker Message ID; {m.id}\nRecent Speaker Message Timestamp; {m.created_at.strftime(timestr)}"
                    break
        tokeninfo += f"\nCollected At; {uh.strftime(timestr)}"

        self.bot.dripfeedmonth.setdefault(m.guild.id,"None")
        month = str(datetime.utcnow().strftime("%Y-%m"))
        try:
            dripfeed = self.bot.dripfeedmonth[m.guild.id] != month and not self.bot.ach_tracking[m.guild.id][u.id][74][0]
        except:
            dripfeed = self.bot.dripfeedmonth[m.guild.id] != month
        if dripfeed:
            self.bot.dripfeedmonth[m.guild.id] = month
            basics.save(self.bot,"dripfeedmonth")

        tokens = ot.otedit(bot, u, 1, True, channel=m.channel, type="gold", extras={"disrespectcount":self.disrespectcount[u.id],"recentspeaker":recentspeaker,"delayed":self.delayed,"dripfeed":dripfeed})
        bot.preresiduecount.setdefault("gold",{})
        bot.preresiduecount["gold"].setdefault(u.id, 5)

        if bot.preresiduecount["gold"][u.id] > 0:
            bot.preresiduecount["gold"][u.id] -= 1
            await talking.say(context, "<:obamatoken:349037437827284992> "
                                    + await talking.replystring(context, "You got an Obama Token! You now have a total of {}. {}\n{} will be shown this message {} before it gets replaced with an Obama Residue.".format(
                tokens, aesthetic.hoveremoji(tokeninfo.replace(";","")), basics.truename(bot, u), ccc.pluralstr("more time", bot.preresiduecount["gold"][u.id]) ),user=u))
            basics.save(bot, "preresiduecount")
        else:
            await utility.safelyclear(bot, context.message, [[utility.get_emoji(bot, "349037437827284992")]]) # Prevents end() from removing the residue

            ObamaResidue(bot, validfor=timedelta(minutes=60), emoji=utility.get_emoji(bot, "653859091331940355"),
                    otheremojis=[basics.useremoji(self.bot, u)] + utility.reactiontext(str(tokens)),
                    info = f"{u.mention} got an Obama Token. They now have a total of {tokens}.\n>>> {tokeninfo.replace(';', ':').replace('  ',' ')}",
                    context=context)

            await asyncio.sleep(1) # Prevents end() from removing the residue

        asyncio.ensure_future(self.end())
        # if m.guild.id == 403747701566734336:
        #     await msg.delete(delay=35)