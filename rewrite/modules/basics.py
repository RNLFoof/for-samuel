import json
import os
import shutil
import pickle
import re
import asyncio
from copy import copy
from datetime import datetime
import collections

import discord

import modules.aesthetic as aesthetic
import modules.loops as loops

from classes.DictSavable import DictSavable
#import dill as pickle

def startup(bot):
    bot.epicord = bot.get_guild(112760669178241024)
    bot.testserver = bot.get_guild(315666280185069568)
    bot.rnl = bot.epicord.get_member(116718249567059974)
    bot.sameguy = bot.epicord.get_member(277449474476081153)
    bot.me = bot.epicord.get_member(309960863526289408)

    bot.kothcooldowndict = {}

    bot.buttons = {}
    for e in bot.get_guild(315666280185069568).emojis + bot.get_guild(331163970629271553).emojis:
        bot.buttons[e.name[3:]] = e

    bot.howtobasic_bottommessage = {}
    bot.howtobasic_eggs = []
    for e in bot.get_guild(381267983290597378).emojis:
        if e.name == "egg":
            bot.howtobasic_eggs.append(e)

    bot.dontpinthat = collections.deque([],50)
    
    asyncio.ensure_future(loops.alive(bot))
    
    loadall(bot)

def contentq(content,*,split=True):
    content = re.sub(r"^s![^ ]* *","",content)
    while "  " in content:
        content=content.replace("  "," ")
    content=content.split(" ")
    l=[]
    for w in content:
        l+=w.split("\n")
    if split:
        return content
    else:
        return " ".join(content)
        
def mentionlesscontent(content):
    return re.sub(r"<@!?[0-9]{18}>","",content).strip()
        
def spitback(s):
    ret = ""
    if s!="":
        for x in s.split(" "):
            if len(f"{ret} {x}")>200:
                if len(x)>=10:
                    ret = f"{ret} {x[:10]}…"
                else:
                    ret = f"{ret}…"
                break
            else:
                ret = f"{ret} {x}"
    ret = ret.strip()
    if not ret:
        ret="­"
    if ret.startswith("`"):
        ret="­"+ret
    if ret.endswith("`"):
        ret+="­"
    ret=ret.replace("``","`­`")
    ret=ret.replace("``","`­`")
    return f"``{ret}``"

# Types:
# aes
# none
def useremoji(bot,user,guild=None,default="aes",actualemoji=False):
    import modules.utility as utility

    if user.id==114147806469554185 and not actualemoji:
        return "<a:ppixel:458887989091893248>"
    ret = utility.get_emoji(bot,"ae_" + user.name)
    if ret==None:
        emojis = list(aesthetic.get_aes_previews_nonew(bot).values())
        if default=="aes":
            ret = aesthetic.hoveremoji("ae_" + user.name, id=emojis[user.id % len(emojis)].id)
        elif default=="none":
            ret = ""
        elif default=="ping":
            ret = user.mention
    return str(ret) if not actualemoji else utility.get_emoji(bot, str(ret))

def loadall(bot):
    load(bot,"disablereplyping","[]")
    load(bot,"suepoints","{}")
    load(bot,"cyclecomics","{}")
    load(bot, "hippoclothing", "{}")
    load(bot, "covidstats", "{}")
    load(bot, "thennicks", '{}')

    load(bot,"obamatokens","{}")
    load(bot,"obamatokensmax","{}")
    load(bot,"obamatokensgiven","{}")

    load(bot,"bronzetimeout","{}")
    load(bot,"sdailylast","{}")
    load(bot,"dripfeedmonth",{})

    load(bot,"preresiduecount",{})
    load(bot,"obamaresidue","{}")
    load(bot,"obamaresiduemax","{}")

    load(bot,"reactionmenus_msgid","{}")
    load(bot,"reactionmenus_idrm","{}")

    load(bot,"inputmenus_msgid","{}")
    load(bot,"inputmenus_serverids","{}")
    load(bot,"inputmenus_channelids","{}")
    load(bot,"inputmenus_idim","{}")

    load(bot, "ach_tracking", "{}")
    load(bot, "ach_tracking_count", "{}")
    load(bot, "ach_tracking_count_hidden", "{}")
    load(bot, "ach_tracking_history", {})

    load(bot,"globalhelprecords","{}")

    load(bot, "priority_week", "collections.deque([],8)")
    load(bot, "priority_day", "{}")
    
def load(bot,var,default):
    exec("""bot.{0} = {1}
if os.path.isfile('saves/{0}.pkl'):
    bot.{0} = pickle.load((open('saves/{0}.pkl', 'rb')))""".format(var,default))
    
def save(bot,var):
    thisisthethingthatactuallysaves(var, getattr(bot, var))

# def dictsave(bot,var):
#     save(bot,dictsavehelper(var))

def thisisthethingthatactuallysaves(name, value):
    pickle.dump(value,open(f'saves/{name}.temp', 'wb'))
    if os.path.exists(f'saves/{name}.pkl'):
        os.remove(f'saves/{name}.pkl')
    os.rename(f'saves/{name}.temp', f'saves/{name}.pkl')

def dictsavehelper(x, debug=False):
    x = copy(x)
    if isinstance(x, list):
        for n,y in enumerate(x):
            x[n] = dictsavehelper(y, debug)
    elif isinstance(x, dict):
        print(x.keys())
        for k,i in x.items():
            x[k] = dictsavehelper(i, debug)
    elif type(x).__mro__[-2].__name__ == "DictSavable":
        print(type(x.getdict()))
        x = dictsavehelper(x.getdict(), debug)
    if debug:
        print("---")
        print(x)
        pickle.dump(x, open("tobedeleted/lol", "w"))
    return x

def dictload(bot,var,default):
    dictloadhelper(bot, load(bot, var, default))

def dictloadhelper(bot, var):
    if var is list:
        for n,y in list(var):
            var[n] = dictloadhelper(bot, var)
    elif var is tuple and len(var)==3 and var[0] == "DictSave":
        var = var[1](bot, **var[2])
    return var

def truename(bot,member):
    s = member.name
    while s != "" and re.match("[A-Za-z]", s[0]) == None:
        s = s[1:]
    while s != "" and re.match("[A-Za-z]", s[-1]) == None:
        s = s[:-1]
    if s != "" and " " not in s and s[0].islower():
        s = s[0].upper() + s[1:]
    s = s.strip()
    if s == "":
        s = member.name
    return s
    
def subcommands(context, q, regexlist, riggedaliases=[]):
    q=q.strip()
    tf=[]
    for x in range(len(regexlist)):
        tf.append(None)
    done=False
    while not done:
        for n,x in enumerate(regexlist):
            if tf[n]==None:
                match=re.match(r"\[("+x+r")\]",q)
                if match != None:
                     tf[n]=match
                     q=q.replace(match.group(0),"",1).strip()
                     break
        else:
            done=True

    # rigged aliases
    for ra in riggedaliases:
        if not tf[ra["slot"]]:
            if re.match(ra["regex"], context.invoked_with):
                tf[ra["slot"]] = re.match(r"\[("+regexlist[ra["slot"]]+r")\]", "["+ra["value"]+"]")

    return tuple([q]+tf)

async def help(context,input,onappartment,*,iteration=0):
    print(input)
    print(iteration)

    embed = discord.Embed()
    bot = context.bot

    #Create a message right away
    from modules.talking import say
    if input not in bot.globalhelprecords and onappartment:
        c = bot.get_guild(529176156398682115).get_channel(546389783539351563)
        msg = await say(context,embed=embed,channel=c)
        bot.globalhelprecords[input] = {"msgid":msg.id, "hash":None}
        save(bot,"globalhelprecords")

    categoriestocommands = {}
    commandnamestocategories = {}
    commandnamestocommands = {}
    features = json.load(open("json/features.json"))
    faq = json.load(open("json/faq.json"))

    path = [""]
    text=""
    buttonnum = 1

    for x in bot.commands:
        if x.cog_name!=None and x.hidden==False:
            n = x.cog_name.replace("_"," ")
            categoriestocommands.setdefault(n,set())
            categoriestocommands[n].add(x)
            commandnamestocategories[x.name] = n
            commandnamestocommands[x.name] = x

    #if input!="":
    #    embed.add_field(name="", value="")  # To be edited later

    # Main text
    notfound = False
    if input=="":
        embed.add_field(name="Introduction", value=json.load(open('json/desc.json')), inline=False)
        s = ""
        for x in ["Commands","Features","Frequently Asked Questions"]:
            hl = await helplink(context,x,onappartment,iteration=iteration)
            s += f"{hl}\n"
        embed.add_field(name="Sections",value=s,inline=False)



    elif input=="Commands":
        s = ""
        for x in sorted(categoriestocommands.keys()):
            hl = await helplink(context,x,onappartment,iteration=iteration)
            s += f"{hl}\n"
        text = s
        #embed.add_field(name="­",value=s[:1000],inline=False)


    elif input in categoriestocommands:
        path.append("Commands")
        s = ""
        for x in sorted(categoriestocommands[input], key=lambda x : x.name):
            hl = await helplink(context,x,onappartment,iteration=iteration)
            s += f"{hl}\n"
        text = s #embed.add_field(name="­",value=s[:1000],inline=False)



    elif input in commandnamestocommands:
        path.append("Commands")
        path.append(commandnamestocategories[input])
        text = commandnamestocommands[input].help




    elif input=="Features":
        s = ""
        for k in features.keys():
            hl = await helplink(context,k,onappartment,iteration=iteration)
            s += f"{hl}\n"
        embed.add_field(name="­",value=s[:1000],inline=False)



    elif input in features:
        path.append("Features")
        embed.add_field(name="­",value=features[input],inline=False)



    elif input=="Frequently Asked Questions":
        s = ""
        for k in faq.keys():
            hl = await helplink(context,k,onappartment,iteration=iteration)
            s += f"{hl}\n"
        embed.add_field(name="­",value=s,inline=False)



    elif input in faq:
        path.append("Frequently Asked Questions")
        embed.add_field(name="­",value=faq[input],inline=False)



    else:
        notfound = True
        text="Not sure what you're looking for."
        if onappartment:
            return

    # Footer
    if onappartment:
        embed.set_footer(text="Search here")
    else:
        embed.set_footer(text="The links work if you're in RSRB's Low Budget Apartment. Use s!ap for a link.")

    # Path
    embed.description = ""
    if input != "" and not notfound:
        path.append(input)
        s = ""
        for x in path[:-1]:
            hl = await helplink(context,x,False,iteration=iteration)
            s+=f"{hl} __*__/__*__ "
        s += input
        embed.title = input
        embed.description = f"{s}__*\n\n"
        #embed.set_field_at(0,name=input,value=s,inline=False)
    embed.description += re.sub('\n*[A-Z](?:[^\n]*?):\n[\W\w]*', "", text,flags=re.MULTILINE)

    # Numbers
    if not onappartment:
        n = 0
        for x in re.findall("\[.+?\]\([^ ]+?\)" ,embed.description):
            n += 1
            rem = embed.description
            embed.description = embed.description.replace(x,re.sub(r"(<a?:\w+:\d+>)",f"\\1{bot.buttons[str(n)]}",x,1))
            if rem == embed.description:
                embed.description = embed.description.replace(x, f"{bot.buttons[str(n)]}{x}",1)

    for x in re.finditer(r'([A-Z](?:[^\n]*?)):\n([\W\w]*?)\n\n+',text):
        embed.add_field(name=x.group(1),value=x.group(2))

    # Wrap up
    if onappartment:

        h = hash(str(embed.to_dict()))
        c = bot.get_guild(529176156398682115).get_channel(546389783539351563)
        from modules.talking import edit
        # Add new
        try:
            if input in bot.globalhelprecords:
                await c.get_message(bot.globalhelprecords[input]["msgid"])
        except:
            del bot.globalhelprecords[input]
        if input not in bot.globalhelprecords:
            msg = await say(context,embed=embed,channel=c)
            bot.globalhelprecords[input] = {"msgid":msg.id, "hash":h}
            save(bot,"globalhelprecords")
        # Check if changed
        elif bot.globalhelprecords[input]["hash"] != h:
            msg = await c.get_message(bot.globalhelprecords[input]["msgid"])
            await edit(context,msg,embed=embed)
            bot.globalhelprecords[input]["hash"] =  h
            save(bot,"globalhelprecords")
    else:
        return embed

async def updateglobalhelp(context):
    await help(context, "", True)

async def helplink(context,input,force,*,iteration=0):
    bot = context.bot
    input = str(input)
    if input not in bot.globalhelprecords or force:
        await help(context, input, True,iteration=iteration+1)
        
    s = ""
    if input == '':
        s+= f"[{'<a:hippovortex:395505717374877696> *__Introduction__*'}](https://discordapp.com/channels/529176156398682115/546389783539351563/{bot.globalhelprecords[input]['msgid']})*__"
    else:
        s += f"[{input}](https://discordapp.com/channels/529176156398682115/546389783539351563/{bot.globalhelprecords[input]['msgid']})"

    return s
