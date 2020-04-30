import asyncio
import collections
import copy
import random
from datetime import datetime
from datetime import timedelta
import re

import discord

import modules.ot as ot
from classes.AchievementBrowser import AchievementBrowser

from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.Daily import Daily
from modules import utility, basics, talking
from modules.basics import truename


async def on_message(bot, m):
    if not m.author.bot:
        # Spruce
        m, delete = await spruce_both(bot, m)
        mproc = await spruce_command(bot, copy.copy(m))
        m = await spruce_user(bot, m)
        # Process
        asyncio.ensure_future(processwrapper(bot, mproc, delete=delete))
        asyncio.ensure_future(run(bot,m,utility.fakecontext(bot,m)))
        # Achievements
        asyncio.ensure_future(AchievementBrowser.ach_check(bot, m.author, m.channel, "msg", m))
        if True:
            # Tokens
            asyncio.ensure_future(ot.spawntoken(bot, m))
            asyncio.ensure_future(ot.spawnsilver(bot, m))
            # asyncio.ensure_future(ot.spawnbronze(bot, m))
            asyncio.ensure_future(sdailymessage(bot, m))
            trackpriority(bot, m)
        # Stop here if the message is gonna be deleted
        if delete:
            return




    #Thennicks
    thennicktracking(bot, m)

    #Curse
    if m.author.id in []:
        l = []
        for e in list(bot.emojis):
            l.append((e.name.lower(),e))
        l.sort(key=lambda x: len(x[0]),reverse=True)

        words = set()
        ends = ["(?<!r)y","ey","ry","ing","er","in","es","s","est"]
        for x in re.finditer(r"(\w+)(" + "|".join(ends) + r")\b|(\w+)",m.content.lower().replace("'","")):
            c = x.group(1) if x.group(1) else x.group(3)
            for a in ["hippo",""]:
                for b in ends+[""]:
                    words.add(re.sub( r"(.)\1+" , r"\1" ,a+c+b.replace("(?<!r)","")))
                    #re.sub(r"[^\w]","",m.content.lower())
        el = list(bot.emojis)
        elsmall = []
        random.shuffle(el)
        print(words)
        cap=20
        for e in el:
            s = re.sub(r"\d+$","",e.name.lower())
            s = re.sub(r"(.)\1+", r"\1", s)
            if len(s)<=1:
                elsmall.append(e)
            elif s in words:
                await m.add_reaction(e)
                cap-=1
                if cap==0:
                    break
        for e in elsmall:
            if cap==0:
                break
            s = re.sub(r"\d+$","",e.name.lower())
            s = re.sub(r"(.)\1+", r"\1", s)
            if s in words:
                await m.add_reaction(e)
                cap-=1

    # HowToBasic
    asyncio.ensure_future(bottobasiceggs(bot, m))
    # Mitty
    if m.author.id == 133408564923465730 and (
        re.search(r"[Aa]{3,}",m.content) is not None or
        m.content.lower().replace("a","") == ""):
        await m.delete()


async def bottobasiceggs(bot,m):
    if m.guild is None:
        return
    if m.guild.me.display_name.lower().replace(" ","") == "howtobasic":
        bot.howtobasic_bottommessage[m.channel.id] = m.id
        for e in bot.howtobasic_eggs:
            await m.add_reaction(e)
            if bot.howtobasic_bottommessage[m.channel.id] != m.id:
                break

async def on_message_edit(bot, before, after):
    if not before.pinned and after.pinned:
        # Needs update
        # async for m in before.guild.audit_logs(limit = 15, action=discord.AuditLogAction.message_pin):
        async for m in before.channel.history(limit = 15):
            if m.type == discord.MessageType.pins_add and not m.author.bot:
                await AchievementBrowser.ach_check(bot, after.author, after.channel, "pin", [after, m])  # Getting your message pinned
                await AchievementBrowser.ach_check(bot, m.author, after.channel, "pinner",[after, m])  # Pinning someone else's message
                break

async def on_raw_message_edit(bot, payload):
    return
    # Need 1.3.0
    if payload.message_id == 112763285417263104:
        channel = bot.get_channel(payload.channel_id)
        async for m in channel.history(limit = 15):
            if m.type == discord.MessageType.pins_add and not m.author.bot:
                pinned = await channel.fetch_message(payload.message_id)
                await AchievementBrowser.ach_check(bot, m.author, channel, "pin", [pinned, m])
                await AchievementBrowser.ach_check(bot, m.author, channel, "pinner",[pinned, m])  # Pinning someone else's message
                break

async def on_raw_reaction_add(bot, payload):
    # Reaction menus
    ids = OngoingReactionMenu.get_ids_by_mid(bot,payload.message_id)
    if ids is not None:
        for x in ids:
            asyncio.ensure_future(OngoingReactionMenu.get_by_id(bot,x).inputtest(payload,"a"))


async def on_raw_reaction_remove(bot, payload):
    # Reaction menus
    ids = OngoingReactionMenu.get_ids_by_mid(bot,payload.message_id)
    if ids is not None:
        for x in ids:
            asyncio.ensure_future(OngoingReactionMenu.get_by_id(bot,x).inputtest(payload,"r"))


async def sdailymessage(bot, m):
    context = utility.fakecontext(bot, m)
    if (m.content.startswith("s!triggerdaily") and m.author.id == bot.rnl.id) or (
            random.randint(1, 40) == 1 and m.guild.id in bot.sdailylast.keys() and str(m.author.id) in bot.sdailylast[
        m.guild.id].keys() and bot.sdailylast[m.guild.id][str(m.author.id)] != str(datetime.utcnow().date())):

        rm = Daily(bot, validfor=timedelta(hours=24), messagecount=1, context=utility.fakecontext(bot, m))


async def sdailysun(bot, m):
    e = "🌤"
    await m.add_reaction(e)
    already = [bot.me.id]
    context = utility.fakecontext(bot, m)
    while True:
        rea = await bot.wait_for_reaction(message=m, emoji="🌤", timeout=300)
        if rea == None:
            break
        else:
            u = rea[1]
            if u.id not in already:
                already.append(u.id)
                await talking.say(context, u.mention, channel=bot.epicord.get_channel("488516474735034389"))
                await bot.remove_reaction(m, rea[0].emoji, rea[1])

                async def spruce_both(m):
                    return m

async def spruce_both(bot, m):
    q = basics.contentq(m.content, split=False)
    deleteregex = r"{D(?:EL(?:ETE)?)?}"
    delete = bool(re.search(deleteregex,q))
    m.content = re.sub(deleteregex,"",m.content)
    return m, delete


async def spruce_user(bot, m):
    return m


async def spruce_command(bot, m):
    if isinstance(m.channel, discord.TextChannel):
        ml = m.guild.members
        rl = m.guild.roles

        memberlayers=[]
        for u in m.guild.members:
            memberlayers.append({"ret":["!" + str(u.id), u],"equals":[[truename(bot,u)],[u.name],[u.display_name],[str(u.id)]]})

        rolelayers = []
        for r in m.guild.roles:
            rolelayers.append({"ret": ["&" + str(r.id), r], "equals": [[str(r.id)], [r.name] ]})

        for x in re.findall("{[^}]*}", m.content):
            if x in ["CONT"]:
                continue
            s = x[1:-1]
            found = utility.layeredsearch(memberlayers,s)
            if found is None:
                found = utility.layeredsearch(rolelayers,s)

            if found is not None:
                m.content = m.content.replace(x, "<@{}>".format(found[0]), 1)
                if found[0].startswith("!"):
                    m.mentions.append(found[1])
                else:
                    m.role_mentions.append(found[1])
    return m

#Run
async def run(bot,m,context):
    if m.content.startswith("s!rrun ") and m.author in (bot.rnl,bot.sameguy):
        s=m.content[7:]
        bot.ret=None
        if s.startswith("await "):
            s=s[6:]
            s=s.replace("bot.say(","bot.send_message(m.channel,").replace("ret=","bot.ret=")
            bot.ret=await eval(s)
        else:
            s=s.replace("bot.say(","bot.send_message(m.channel,").replace("ret=","bot.ret=")
            exec(s)
        print("OUTPUT: "+str(bot.ret))
        if bot.ret!=None:
            await talking.say(context,str(bot.ret))


def trackpriority(bot,m):
    if m.author.bot:
        return
    date=str(datetime.utcnow().date())
    if len(bot.priority_week)==0 or bot.priority_week[-1]["date"]!=date:
        bot.priority_week.append({"date":date, "servers":{}})
    bot.priority_week[-1]["servers"].setdefault(m.guild.id,{})
    bot.priority_week[-1]["servers"][m.guild.id].setdefault(m.author.id,0)
    bot.priority_week[-1]["servers"][m.guild.id][m.author.id] += 1
    basics.save(bot,"priority_week")

async def processwrapper(bot, mproc, **kwargs):
    await bot.process_commands(mproc)
    if "delete" in kwargs and kwargs["delete"]:
        await mproc.delete()

def thennicktracking(bot, m):
    bot.thennicks.setdefault(m.channel.id, collections.OrderedDict())
    bot.thennicks[m.channel.id][m.id] = m.author.display_name
    while len(bot.thennicks[m.channel.id])>250:
        bot.thennicks[m.channel.id].popitem(last=False)
    basics.save(bot,"thennicks")