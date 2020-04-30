import re
import discord
import requests
import json
import random
import os
from io import BytesIO
import json
from os import listdir
import asyncio
import modules.utility as utility

async def say(context,string=None,embed=None,split=False,reaction=False,channel=None,file=None,viaspoilerbot=False,PIL=None,nowebhook=False,specificwebhook=None, disableaes=False):
    bot=context.bot
        
    if channel==None:
        channel=context.message.channel
        
    try:
        if [context.message.id,context.message.content] in bot.runmutemessages:
            channel=bot.testserver.get_channel("315666280185069568")
    except:
        pass
    if string!=None:
        string=await detailsaystring(context,string,disableaes=disableaes)
    if string==None:
        return await channel.send(string,embed=embed)
    elif split:
        lst = []
        buildup=""
        for x in string.split("\n"):
            ecount=0
            for y in list(unicodeemojis):
                ecount+=(buildup+x).count(y)
            if len(buildup+x+"\n")+ecount>2000 or ecount>=100:
                lst.append(await channel.send(buildup))
                buildup=""
            buildup+=x+"\n"
        lst.append(await channel.send(buildup))
        return lst
    else:
        #print("HI")
        string=trimsaystring(context,string)
        #print(len(string))
        if False and reaction and context.message.author.id in bot.confirmationroationusers and context.message not in bot.disableconfirmreactions:
            asyncio.ensure_future(sayconfirmreaction(bot,context.message,string,embed,channel))
            return
        if False and context.message in bot.disableconfirmreactions:
            bot.disableconfirmreactions.remove(context.message)
        if PIL!=None:
            if not os.path.exists("tobedeleted"):
                os.makedirs("tobedeleted")
            filename = f"tobedeleted/{context.message.channel.id}-{context.message.id}.png"
            PIL.save(filename)
            file = open(filename,"rb")
        if file==None:
            if viaspoilerbot and False:
                headers = {'Authorization': 'Bot NDUwODY3NDgzODk4MDE5ODQw.De5f3g.uPdsah3IGRr-12swwSZ_N5OeBjw'}
                headers = {'Authorization': 'Bot MzA5OTYwODYzNTI2Mjg5NDA4.DBXuJA.ijF9bk3E9JJwDG5KHyc67t3Wt18'}
                url = f'https://discordapp.com/api/channels/{channel.id}/messages'
                params = {'content': "hi",'Authorization': 'Bot MzA5OTYwODYzNTI2Mjg5NDA4.DBXuJA.ijF9bk3E9JJwDG5KHyc67t3Wt18'}
                r = requests.post(url, params=params, headers=headers)
                if r.ok:
                    print("JSON: ", r.json())
                else:
                    r.raise_for_status()
            else:
                # Send as webhook
                if not nowebhook:
                    if specificwebhook==None and context.message.author.id == 116718249567059974 and False:
                        specificwebhook = ("WHO SUMMONED ME","https://cdn.discordapp.com/attachments/315666280185069568/507424421430951936/owen.png")
                    if specificwebhook=="default":
                        print(context.guild.me.avatar_url)
                        specificwebhook = (context.guild.me.display_name, context.guild.me.avatar_url)
                if specificwebhook != None:
                    if len(specificwebhook[0])<2:
                        specificwebhook = (specificwebhook[0]+"_",specificwebhook[1])
                    webhook = None
                    for wh in await channel.webhooks():
                        if wh.name == "RSRB - Webhook":
                            webhook = wh 
                            break
                    if webhook == None:
                        with open("images/main_avatar.png","rb") as f:
                            webhook = await channel.create_webhook(name = "RSRB - Webhook", avatar=f.read())
                    # List all avaliable emojis
                    elist = []
                    for e in context.message.guild.emojis:
                        elist.append(str(e))
                    # Gather all unavaliable emojis
                    reactlist = []
                    for e in re.findall(r"<a?:[A-Za-z_]+:[0-9]+>",string):
                        if e not in elist and e in string: # if it's not in the string it's been processed already
                            string = string.replace(e,"▪")
                            e = utility.get_emoji(bot,e)
                            if e!=None:
                                reactlist.append(e)
                    await webhook.send(string,embed=embed,tts=None,username=specificwebhook[0], avatar_url=specificwebhook[1])
                    # the webhook thing doesn't return a message yet so
                    msg = None
                    for x in range(10):
                        async for m in context.message.channel.history(limit=10):
                            if m.webhook_id!=None and m.content == string:
                                msg = m
                                break
                        if msg!=None:
                            break
                    else:
                        print("fuck")
                        return
                    for e in reactlist:
                        asyncio.ensure_future(msg.add_reaction(e))
                    return msg
                    return await webhook.send(string,embed=embed,tts=None,username="CIyde", avatar_url="https://discordapp.com/assets/f78426a064bc9dd24847519259bc42af.png")
                    return await webhook.send(string,embed=embed,tts=None,username="NotSoBot", avatar_url="https://cdn.discordapp.com/avatars/439205512425504771/ed79680e6df20be63efcc708a32a3eab.webp?size=1024")
                # Send normally
                else:
                    return await channel.send(string,embed=embed,tts=None)
        # Send File
        else:
            return await channel.send(file=discord.File(file,filename=file.name.split("/")[-1]),content=string,tts=None)
    
async def sayconfirmreaction(bot,message,string,embed,channel):
    #emoji=random.choice(["😂","😊","😜","😎","🤗","😏","😒","🤔","😤","😩"])
    from modules.ccc import eightconfirm
    emoji=eightconfirm()
    await bot.add_reaction(message,emoji)
    rea = await bot.wait_for_reaction(emoji,timeout=300,user=message.author,message=message)
    if rea==None:
        return
    await bot.clear_reactions(message)
    await bot.send_message(channel,string,embed=embed,tts=None)
    
async def reply(context,string=None,embed=None,split=False,reaction=False,channel=None,file=None, silent=False,viaspoilerbot=False,PIL=None,nowebhook=False,specificwebhook=None,disableaes=False,user=None):
    tosay = await replystring(context,string=string,channel=channel, silent=silent, user=user)

    return await say(context, tosay,embed=embed,split=split,reaction=reaction,channel=channel,file=file,PIL=PIL,nowebhook=nowebhook,specificwebhook=specificwebhook,disableaes=disableaes)

async def replystring(context,string=None,channel=None, silent=False,user=None):
    import modules.basics as basics

    if user==None:
        user = context.message.author

    if (channel == None or channel.id == context.message.channel.id)\
            and user.id in context.bot.disablereplyping:
        silent=True

    tosay = basics.useremoji(context.bot,user)+" "
    if silent:
        tosay += basics.truename(context.bot,user)
    else:
        tosay += user.mention

    if string is not None and string.startswith("asked"):
        tosay += " "
    else:
        tosay += ": "

    if string is not None:
        tosay += string

    return tosay

async def edit(context,message,string=None,embed=None,viaspoilerbot=False):
    bot=context.bot
    channel=context.message.channel
    if string!=None:
        string=await detailsaystring(context,string)
        string=trimsaystring(context,string)
    sendbot = bot
    if viaspoilerbot:
        sendbot=bot.spoilerbot
    return await message.edit(content=string,embed=embed)

async def replyedit(context,message,string=None,embed=None,viaspoilerbot=False):
    import modules.basics as basics

    prefix=": "
    if string==None:
        return await edit(context,message,basics.useremoji(context.bot,context.message.author)+" "+context.message.author.mention+prefix,embed=embed)
    else:
        if string.startswith("asked"):
            prefix=" "
        return await edit(context,message,context.message.author.mention+prefix+string,embed=embed,viaspoilerbot=viaspoilerbot)
    
def detailsaystring_cleanemoji(match):
    return match.group(0).replace(f":{match.group(1)}:",":_:",1)
    
async def detailsaystring(context,string,*,disableaes=False):
    import modules.basics as basics

    # string=string.replace("O","OwO")
    # string=string.replace("o","OwO")
    
    #string=re.sub("<@!?[0-9]{18}>","<@113852329832218627>",string)
    
    #if context.command!=None and context.command.name!="drop" and (context.command.name=="8ball" and context.message.author.id=="113457314106740736")==False:
    #    string=string.replace(f"`{' '.join(contentq(context.message.content))}­`","^that").replace(f"`­{' '.join(contentq(context.message.content))}`","^that").replace(f"`{' '.join(contentq(context.message.content))}`","^that").replace(f"`­{' '.join(contentq(context.message.content))}­`","^that")#.replace("``^that``",f"```­{contentq(context.message.content)}```")
    
    string=string.replace("@everyone","@­everyone")
    #string=re.sub("<a?:([A-Za-z0-9_]{2,32}):[0-9]{18}>",detailsaystring_cleanemoji,string)
    
    # split=string.split(" ")
    # string=""
    # for x in split:
        # string+=x
        # if re.sub('[^a-z]*', '', x.lower()) in ["porn","horny","sexy","did","asshole","butthole","hole","moist","do","dirty","fuck","piss","shit","dick","penis","vagina","pussy","touch","press","compress","hit","punch","whip","foot","feet","eat","stuff","vore","girl","boy","loli","kid","child","trample","tread","heavy","weight","fat","pull","ass","butt","rock","eat","lick","tongue","hair","hill","ball","balls","round"]:
            # string+="<a:hipposeductive:397622396401745932>"
        # string+=" "
    if context.message.guild!=None and not disableaes:
        for x in re.findall("<@!?[0-9]{18}>", string):
            id=x.replace("<","").replace(">","").replace("@","").replace("!","")
            dude = context.bot.get_user(int(id))
            if dude == None:
                dude = await context.bot.fetch_user(int(id))
            emoji = basics.useremoji(context.bot, dude, guild=context.message.guild)
            string=string.replace(emoji+x,x)
            string=string.replace(emoji+" "+x,x)
            string=string.replace(x,emoji+" "+x)
        """if context.bot.admin[context.message.server.id]["avataremojiserver"]!=None:
            for k in context.bot.admin[context.message.server.id]["avataremojiserver"][1].keys():
                m1=f"<@{k}>"
                m2=f"<@!{k}>"
                emoji = mf.emojiser(context.bot,context.bot.admin[context.message.server.id]["avataremojiserver"][1][k][0])
                string=string.replace(emoji+m1,m1)
                string=string.replace(emoji+" "+m1,m1)
                string=string.replace(emoji+m2,m2)
                string=string.replace(emoji+" "+m2,m2)
                string=string.replace(m1,emoji+" "+m1)
                string=string.replace(m2,emoji+" "+m2)"""
    for x in [
    ["112760669178241024","🌐"],
    ["288058913985789953","🎮"],
    ["249968792346558465","🎨"],
    ["122155380120748034","🖥"],
    ["160197704226439168","🤖"],
    ["134477188899536898","📺"],
    ["132423337019310081","🇯🇵"],
    ["331390333810376704","📌"],
    ["413152451345121280","⚔"],
    ["410596805445681162","🏰"],
    ["189898393705906177","⌨"],
    ["398661111869865985","😘"],
    ["265998010092093441","🎳"],
    ["312054608535224320","📽"],
    ["265617582126661642","🎼"],
    ["373335332436967424","🗣"],
    ["392141322863116319","😐"],
    ["191487489943404544","👅"],
    ["113414562417496064","🐦"],
    ["359903425074561024","💭"],
    ]:
        string=string.replace(f"<#{x[0]}>",f"{x[1]}<#{x[0]}>")
        
    #Re-Enable when custom hippos exist
    # userchids=[]
    # for u in context.bot.activecustomhippos.keys():
        # for slot in context.bot.activecustomhippos[u]:
            # if slot!=None:
                # for k,i in slot.items():
                    # userchids.append(i[0].id)
    # #Custom hippo
    # for k,i in context.bot.activecustomhippos[context.bot.me.id][0].items():
        # string=re.sub("(<a?:"+k+":[0-9]{18}(?<!("+"|".join(userchids)+"))>)",emojistr(context.bot,i[0]),string)
    
    return string#.replace(" ","👏")
    
def trimsaystring(context,string):
    import modules.basics as basics

    #Trim copies of what the user wrote, leaving 250 characters
    q=basics.contentq(context.message.content,split=False)
    if len(string)>2000 and len(q)>250:
        #print(len(string))
        #print(len(string)-1999)
        #print(len(q)-(len(string)-1999))
        trim=len(q)-(len(string)-1999)
        if trim<249:
            trim=249
        string=string.replace("`"+q+"`","`"+q[:trim]+"…`")
    #Trim end, save for obvious footers
    if len(string)>2000:
        conserve=""
        paras=string.split("\n\n")
        if paras[-1].count("\n")<=2 and len(paras[-1])<=500:
            conserve="\n\n"+paras[-1]
        string=string[:1999-len(conserve)]+"…"+conserve
    
    return string