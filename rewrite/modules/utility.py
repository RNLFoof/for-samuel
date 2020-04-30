import collections
import pickle
import re
import statistics
from datetime import datetime

import discord
import requests
import json
import random
import os
from PIL import Image
from io import BytesIO
import json
from os import listdir
import asyncio


def get_title_role(member):
    for r in member.guild.roles[::-1]:
        if r.hoist and r in member.roles:
            return r
    return None

def get_emoji(bot,s,*,exclude=[],musthavespoilerbot=False):
    exids=[]
    for e in exclude:
        try:
            exids.append(e.id)
        except:
            pass
    found=[]
    goal="0"
    on=False
    for x in list(s):
        if x=="~" and goal=="0":
            on=True
        elif on:
            try:
                int(x)
                goal+=x
            except:
                on=False
    if goal!="0":
        s=s.replace("~"+goal[1:],"")
    goal=int(goal)
    #print(goal,s)
    
    # New
    #for e in bot.unicodeemojis:
    #    if e.id in s and e.id not in found+exids:
    #        if len(found)==goal:
    #            return e
    #        found.append(e.id)
    
    findid = re.search("[0-9]{18}",s)
    if findid != None:
        s=s.replace(findid.group(),"")
        findid = findid.group()
    
    findname = re.search("[A-Za-z0-9_]{2,32}",s)
    if findname == None and findid!=None:
        findname = findid
    elif findname != None:
        findname = findname.group()
        
    if findname == None and findid == None:
        return
        
    #print(findid,findname)
    
    if findid!=None:
        for e in list(bot.emojis):# + bot.unicodeemojis:
            if e.id == int(findid) and e.id not in found+exids:
                if len(found)==goal:
                    return e
                found.append(int(e.id))
            
    sameguyservers = []
    for s in bot.guilds:
        if s.owner.id == bot.sameguy.id:
            sameguyservers.append(s.id)
    #print(sameguyservers)
            
    for sameguy in [False,True]:
        for e in list(bot.emojis):# + bot.unicodeemojis:
            if (e.guild==None or e.guild.id not in sameguyservers)!=sameguy and (e.guild==None or musthavespoilerbot==False or (musthavespoilerbot and e.guild.get_member("450867483898019840")!=None)):
                if e.name == findname and e.id not in found+exids:
                    if len(found)>=goal:
                        return e
                    found.append(e.id)
        for e in list(bot.emojis):# + bot.unicodeemojis:
            if (e.guild==None or e.guild.id not in sameguyservers)!=sameguy and (e.guild==None or musthavespoilerbot==False or (musthavespoilerbot and e.guild.get_member("450867483898019840")!=None)):
                if e.name.lower() == findname.lower() and e.id not in found+exids:
                    if len(found)>=goal:
                        return e
                    found.append(e.id)
    
    return None

def get_emoji_url(bot,s):
    m = re.search("<a?:[A-Za-z0-9_]+:([0-9]+)>",s)
    if m != None:
        url = f"https://cdn.discordapp.com/emojis/{m.group(1)}"
        print(requests.get(url + ".gif").status_code)
        if requests.get(url + ".gif").status_code == 200:
            return url + ".gif"
        return url + ".png"
    e = get_emoji(bot,s)
    if e != None:
        return str(e.url)
    return None

def get_member_or_user(bot,guild,id):
    if guild != None:
        m = guild.get_member(id)
        if m != None:
            return m
    return bot.get_user(id)
    

async def safelyclear(bot,msg,lst):
    #lst is a list of lists of emojis followed by the users to take from. If it's just the emoji, that means all users.
    msg = await msg.channel.fetch_message(msg.id)
    reactions = msg.reactions
    manually = False
    goagain=False
    for r in reactions:
        for l in lst:
            #print(l)
            if str(r.emoji)==str(l[0]): #If they have mauching emojis
                if len(l)==1: #Matches everyone. If so this is valid
                    #print(1)
                    break
                reactors = []
                async for u in r.users():
                    reactors.append(u)
                #print(reactors)
                #Will now attempt to match every reactor. If it's not exact, no go.
                if len(l[1:])<len(reactors):#If there's more people who reacted than people you want to remove, then it can't be valid.
                    manually = True
                    #print(2)
                    break
                #Put all the IDs into two lists. Remove everything in l from r. If r is empty, it's safe.
                idlist=[]
                for x in reactors:
                    idlist.append(x.id)
                #print(l[1:])
                #print(idlist)
                for x in l[1:]:
                    while x.id in idlist:
                        idlist.remove(x.id)
                if len(idlist)!=0:
                    manually = True
                #print(3)
                break
        else: #If it gets here the reaction emoji isn't in the list at all
            #print(4)
            manually=True
        if manually: # Break out of thos loop too if need be
            break
    #Actually do stuff
    if manually:
        #print(5)
        for l in lst:
            for r in reactions:
                if not r.custom_emoji:
                    continue
                if r.emoji.id==l[0].id:
                    if len(l)>1:
                        for u in l[1:]:
                            #try:
                                goagain=True
                                await msg.remove_reaction(l[0],u)
                            #except:
                            #    pass
                    else:
                        async for u in r.users():
                            #try:
                                goagain=True
                                await msg.remove_reaction(l[0],u)
                            #except:
                            #    pass
                        break
        
    else:
        msg = await msg.channel.fetch_message(msg.id)
        reactions = msg.reactions
        old=msg.reactions
        await msg.clear_reactions()
        msg = await msg.channel.fetch_message(msg.id)
        if msg.reactions!=old:
            goagain=True
    if goagain:
        #print("AGAIN")
        await asyncio.sleep(2)
        await safelyclear(bot,msg,lst)    

def nodups(lst):
    l=len(lst)+1
    while l>len(lst):
        l=len(lst)
        for x in lst:
            if lst.count(x)>1:
                lst.remove(x)
    return lst
    
async def referencemessage(context, displayerror = True, s=None):
    from modules.talking import reply
    from modules.basics import contentq
    m = context.message
    if s!=None:
        q = s
    else:
        q = contentq(m.content, split=False)

    try:
        n = int(q)
    except:
        n = None

    # By ID, same channel
    if n != None:
        try:
            return await m.channel.fetch_message(n)
        except:
            pass
    # By ID, any channel
    #     for c in m.guild.channels:
    #         if c != m.channel:
    #             print(c)
    #             try:
    #                 return await c.get_message(n)
    #             except:
    #                 pass

    # Case sensitive content
    async for msg in m.channel.history(limit=100, before=m):
        if q in msg.content and msg.type == discord.MessageType.default:
            return msg

    # Case insensitive context
    async for msg in m.channel.history(limit=100, before=m):
        if q.lower() in msg.content.lower() and msg.type == discord.MessageType.default:
            return msg

    # Fuck
    if displayerror:
        msg = await reply(context,"I couldn't figure out what message you were referring to.")
        context.bot.dontpinthat.append(msg.id)
    return None

async def referenceimage(context, displayerror = True, s=None, returnurl=False):
    from modules.talking import reply
    from modules.basics import contentq
    bot = context.bot
    m = context.message
    defaults = False
    if s == None:
        defaults = True
        s = contentq(m.content, split=False)

    i=None

    if not i:
        i = re.search(r"\bhttps?:\/\/[^ ]*\b",s)
        if i:
            i = i.group(0)

    if not i:
        u = re.search(r"<@!?(\d+)>", s)
        print(1)
        if u:
            print(2)
            u = bot.get_user(int(u.group(1)))
            if u:
                print(3)
                i = str(u.avatar_url)

    if not i:
        if context.message.attachments:
            i = context.message.attachments[0].url

    if not i:
        i = get_emoji_url(bot, s)

    if i:
        if returnurl:
            return i
        else:
            return imagefromurl(i)

    # Fuck
    if displayerror:
        if defaults:
            await reply(context, "I couldn't figure out what you were referring to.")
        else:
            await reply(context, f"I couldn't figure out what `{s}` is referring to.")
    return None

def imagefromurl(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert('RGBA')

async def hasemoji(bot,emoji,*,musthavespoilerbot=False):
    from modules.aesthetic import hoveremoji
    if re.search(":[A-Za-z0-9_]+:",str(emoji)) == None:
        return str(emoji)
    e = get_emoji(bot,str(emoji),musthavespoilerbot=musthavespoilerbot)
    if e == None:
        return hoveremoji(re.search(":[A-Za-z0-9_]+:",str(emoji)).group())
    else:
        return str(e)
        
# def add_reaction_menu(bot,rm):
    # for m in rm.messages:
    # if rm.message.guild.id not in bot.ongoingreactionmenus.keys():
        # bot.ongoingreactionmenus[rm.message.guild.id] = {}
    # if rm.message.channel.id not in bot.ongoingreactionmenus[rm.message.guild.id].keys():
        # bot.ongoingreactionmenus[rm.message.guild.id][rm.message.channel.id] = {}
    # if rm.message.id not in bot.ongoingreactionmenus[rm.message.guild.id][rm.message.channel.id].keys():
        # bot.ongoingreactionmenus[rm.message.guild.id][rm.message.channel.id][rm.message.id] = []
    # bot.ongoingreactionmenus[rm.message.guild.id][rm.message.channel.id][rm.message.id].append(rm)

# Makes a fake "context" using a bot and a message for use outside of commands.
FakeContext = collections.namedtuple("FakeContext", ["bot", "message", "command"])
def fakecontext(bot, message):
    return FakeContext(bot=bot, message=message, command=None)

def getcoolpeople(bot,server,*,priority="low"):

    from modules.basics import save

    cap = [1,15,30][["low","medium","high"].index(priority)]
    ret = []

    bot.priority_day.setdefault("date", None)
    if bot.priority_day["date"] != str(datetime.utcnow().date()):
        bot.priority_day["date"] = str(datetime.utcnow().date())
        bot.priority_day["servers"] = {}
    bot.priority_day["servers"].setdefault(server.id, {})

    for u in server.members:
        if u.id not in bot.priority_day["servers"][server.id]:
            numbers = []
            for x in range(len(bot.priority_week)):
                x = bot.priority_week[x]
                if server.id in x["servers"]:
                    numbers.append(x["servers"][server.id].get(u.id, 0))
            if not numbers:
                numbers = [0]
            bot.priority_day["servers"][server.id][u.id] = round(statistics.median(numbers))
            save(bot, "priority_day")

        if bot.priority_day["servers"][server.id][u.id] >= cap:
            ret.append(u)

    return ret

def portal(msg,s="<a:hippovortex:395505717374877696>"):
    return f"[{s}]({msg.jump_url})"

def layeredsearch(layers,searchfor):
    # Needs a list of dicts, with a "ret" for what is returned, and a "equals",
    # for what you go through. It's a list of lists. All first lists are equal
    # priority, all second lists are equal priority.

    # Go through all firsts, then all seconds. Is, starts, in. Case sensitive, insensitive.
    for strictness in ["is","st","in"]:
        for case in ["cs","ci"]:
            for pos in range(len(layers[0])): # First, second...
                for layer in layers: # All layers, only the pos will be used
                    for s in layer["equals"][pos]: # All equal strings in that position
                        regex = re.escape(searchfor)
                        if strictness=="is":
                            regex = f"^{regex}$"
                        elif strictness=="st":
                            regex = f"^{regex}"
                        flag = 0 if case=="cs" else re.IGNORECASE

                        if re.search(regex,s,flag) != None:
                            return layer["ret"]
    return None

async def reactionsbyuser(m,u):
    l = []
    for r in m.reactions:
        if u in await r.users().flatten():
            l.append(r.emoji)
    return l

def reactiontext(s):
    # You'll have to add bls later. woo
    fonts = json.load(open("json/fonts.json", encoding='utf-8'))
    used = {}
    colors = ["blue","green","yellow","orange","red","pink","purple","white","grey","black","brown","gay"]
    ret = []
    for x in list(s):
        if x not in fonts["red"]["characters"]:
            continue
        for c in colors:
            used.setdefault(c,set())
            if x not in used[c]:
                ret.append(fonts[c]["characters"][x])
                used[c].add(x)
                break
    return ret