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
    
### basics
    
def contentq(content,*,split=True):
    if " " not in content:
        return ""
    while content.startswith(" ")==False:
        content=content[1:]
    while content.startswith(" "):
        content=content[1:]
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
    if ret=="":
        ret="­"
    return f"``{ret}``"
        
async def say(context,string=None,embed=None,split=False,reaction=False,channel=None,file=None,viaspoilerbot=False,PIL=None):
    bot=context.bot
        
    if channel==None:
        channel=context.message.channel
        
    try:
        if [context.message.id,context.message.content] in bot.runmutemessages:
            channel=bot.testserver.get_channel("315666280185069568")
    except:
        pass
    if string!=None:
        string=detailsaystring(context,string)
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
                if context.message.author.id == 116718249567059974:
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
                            e = get_emoji(bot,e)
                            if e!=None:
                                reactlist.append(e)
                    msg = await webhook.send(string,embed=embed,tts=None,username="WHO SUMMONED ME", avatar_url="https://cdn.discordapp.com/attachments/315666280185069568/507424421430951936/owen.png")
                    # the webhook thing doesn't return a message yet so
                    async for m in context.message.channel.history():
                        if m.webhook_id!=None:
                            msg = m
                            break
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
    emoji=random.choice(["😀","😬","😂","😅","😉","😊","🙃","☺","😍","😜","😎","🤗","😏","😒","🙄","😳","😠","😩","😤","😱","😭","😵","😲","🤢","🤣","🤔","😖","😕","😆",get_emoji(bot,":whatthefuck:358083695544107019")])
    await bot.add_reaction(message,emoji)
    rea = await bot.wait_for_reaction(emoji,timeout=300,user=message.author,message=message)
    if rea==None:
        return
    await bot.clear_reactions(message)
    await bot.send_message(channel,string,embed=embed,tts=None)
    
async def reply(context,string=None,embed=None,split=False,reaction=False,channel=None,file=None, silent=False,viaspoilerbot=False,PIL=None):
    prefix=": "
    if string==None:
        return await say(context,useremoji(context.bot,context.message.author)+" "+context.message.author.mention+prefix,embed=embed,split=split,reaction=reaction,channel=channel)
    else:
        if string.startswith("asked"):
            prefix=" "
        if silent:
            return await say(context,useremoji(context.bot,context.message.author)+" "+truename(context.message.author)+prefix+string,embed=embed,split=split,reaction=reaction,channel=channel,file=file,PIL=PIL)
        else:
            return await say(context,context.message.author.mention+prefix+string,embed=embed,split=split,reaction=reaction,channel=channel,file=file,viaspoilerbot=viaspoilerbot,PIL=PIL)

async def edit(context,message,string=None,embed=None,viaspoilerbot=False):
    bot=context.bot
    channel=context.message.channel
    if string!=None:
        string=detailsaystring(context,string)
        string=trimsaystring(context,string)
    sendbot = bot
    if viaspoilerbot:
        sendbot=bot.spoilerbot
    return await sendbot.edit_message(message,string,embed=embed)

async def replyedit(context,message,string=None,embed=None,viaspoilerbot=False):
    prefix=": "
    if string==None:
        return await edit(context,message,useremoji(context.bot,context.message.author)+" "+context.message.author.mention+prefix,embed=embed)
    else:
        if string.startswith("asked"):
            prefix=" "
        return await edit(context,message,context.message.author.mention+prefix+string,embed=embed,viaspoilerbot=viaspoilerbot)
    
def detailsaystring_cleanemoji(match):
    return match.group(0).replace(f":{match.group(1)}:",":_:",1)
    
def detailsaystring(context,string):
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
    if context.message.guild!=None:
        for x in re.findall("<@!?[0-9]{18}>", string):
            id=x.replace("<","").replace(">","").replace("@","").replace("!","")
            emoji=useremoji(context.bot,id,guild=context.message.guild)
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
    #Trim copies of what the user wrote, leaving 250 characters
    q=contentq(context.message.content,split=False)
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
    
def useremoji(bot,user,guild=None):
    return "<:bl:230481089251115018>"


    
###utility
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
    
    for e in list(bot.emojis):# + bot.unicodeemojis:
        if e.id == findid and e.id not in found+exids:
            if len(found)==goal:
                return e
            found.append(e.id)
            
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
        for e in list(bot.get_all_emojis()):# + bot.unicodeemojis:
            if (e.guild==None or e.guild.id not in sameguyservers)!=sameguy and (e.guild==None or musthavespoilerbot==False or (musthavespoilerbot and e.guild.get_member("450867483898019840")!=None)):
                if e.name.lower() == findname.lower() and e.id not in found+exids:
                    if len(found)>=goal:
                        return e
                    found.append(e.id)
    
    return None
    
### cumcom compatible
ans_no = [
            "OF COURSE NOT",
            "YOU'RE GOING TO GET YOURSELF KILLED",
            "ehhhhhhhhhhhhhh",
            "You dumbass!!",
            "<:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280><:hippounamused:284498351733473280>",
            "You should burn in Hell for even thinking that.",
            "Stop drinking paint.",
            "FUCK YOU DAD",
            "<:fuck:230420172526059520> :regional_indicator_n: :regional_indicator_o:",
            "FOOLISH SAMURAI!",
            "Try to die in a way that has more dignity.",
            "No. Never again.",
            "We Are Number One but Every One is Replaced With That Stupid Fucking Idea",
            "Apparently not, Bubsy. Apparently not. <:jontron:340195175848476682>",
            "I'M GONNA EVISCERATE YOU AND USE YOUR GASTRO-INTESTINAL TRACT AS A CONDOM WHILE I FORNICATE﻿ WITH YOUR SKULL!",
            "If you were hoping I'd tell you to not do something important, you've come to the right place.",
            "DON'T <:freak:273882457286246401>",
            "https://cdn.discordapp.com/attachments/315666280185069568/480626011990654996/xidnaf.gif",
            "https://media1.tenor.com/images/9a460311e00a57799aa8906080865ad3/tenor.gif?itemid=8712094",
            "https://media.giphy.com/media/9XXJspa2J6wLnG32Ul/giphy.gif",
            """
N
　   O
　　　 O
　　　　 o
　　　　　o
　　　　　 o
　　　　　o
　　　　 。
　　　 。
　　　.
　　　.
　　　 .
　　　　."""
        ]
        
ans_chat = [
        "Hi!",
        "Hello!",
        "Hi there!",
        "Hey!",
        "Howdy!",
        "Hi everybody!",
        "Welcome to Toontown!",
        "What's up?",
        "How are you doing?",
        "Hello?",
        "Bye!",
        "Later!",
        "See ya!",
        "Have a nice day!",
        "Have fun!",
        "Good luck!",
        "I'll be right back.",
        "I'll be back later!",
        "I only have a few minutes.",
        "I need to go.",
        ":-)",
        "Yay!",
        "Hooray!",
        "Cool!",
        "Woo hoo!",
        "Yeah!",
        "Ha ha!",
        "Hee hee!",
        "Wow!",
        "Great!",
        "Whee!",
        "Oh boy!",
        "Whoopee!",
        "Yippee!",
        "Yee hah!",
        "Toontastic!",
        ":-(",
        "Oh no!",
        "Uh oh!",
        "Rats!",
        "Drat!",
        "Ouch!",
        "Oof!",
        "No!!!",
        "Yikes!",
        "Huh?",
        "I need more Laff Points.",
        "You look nice.",
        "You are awesome!",
        "You rock!",
        "You are a genius!",
        "I like your name.",
        "I like your look.",
        "I like your shirt.",
        "I like your skirt.",
        "I like your shorts.",
        "I like this game!",
        "Thanks!",
        "No problem.",
        "You're welcome!",
        "Any time!",
        "No thank you.",
        "Good teamwork!",
        "That was fun!",
        "Please be my friend!",
        "Let's work together!",
        "You guys are great!",
        "Are you new here?",
        "Have you been here before?",
        "Did you win?",
        "I think this is too risky for you.",
        "Would you like some help?",
        "Can you help me?",
        "Oops!",
        "Sorry!",
        "Sorry, I'm busy fighting cogs!",
        "Sorry, I'm busy getting Jellybeans!",
        "Sorry, I'm busy completing a Toontask!",
        "Sorry, I'm busy fishing!",
        "Sorry, I'm busy kart racing!",
        "Sorry, I'm busy gardening!",
        "Sorry, I'm busy golfing!",
        "Sorry, I'm in a building!",
        "Sorry, I'm helping a friend!",
        "Sorry, my Friends List is full.",
        "Sorry, I had to leave unexpectedly.",
        "Sorry, I was delayed.",
        "Sorry, I can't.",
        "I can't get on the elevator now.",
        "I couldn't wait any longer.",
        "I can't understand you.",
        "Use the SpeedChat.",
        "Hey!",
        "Please go away!",
        "Stop that!",
        "That wasn't nice!",
        "Don't be mean!",
        "You stink!",
        "I'm stuck.",
        "Let's go on the trolley!",
        "Let's go back the the playground!",
        "Let's go to Toontown Central!",
        "Let's go to Donald's Dock!",
        "Let's go to Minnie's Melodyland!",
        "Let's go to Daisy Gardens!",
        "Let's go to The Brrrgh!",
        "Let's go to Donald's Dreamland!",
        "Let's go to Goofy Speedway!",
        "Let's go fishing!",
        "Let's go to Chip 'n Dale's Acorn Acres!",
        "Let's go to Chip 'n Dale's Minigolf!",
        "Let's go fight the Cogs!",
        "Lets go take over a Cog building!",
        "Let's go in the elevator!",
        "Let's go to Sellbot HQ!",
        "Let's go fight the VP!",
        "Let's go in the Factory!",
        "Let's go to Cashbot HQ!",
        "Let's go fight the CFO!",
        "Let's go in the Mint!",
        "Let's go to Lawbot HQ!",
        "Let's go fight the Chief Justice!",
        "Let's go in the District Attorney's office!",
        "Let's go to Bossbot HQ!",
        "Let's go fight the CEO!",
        "Let's go in the Cog Golf Course!",
        "Let's go take over a Field Office!",
        "Let's go to my house!",
        "Let's go to your house!",
        "Can you come to my house?",
        "Let's go fishing at my house!",
        "Come check out my garden.",
        "Let's go to a party.",
        "See you at the party!",
        "My party has started!",
        "Come to my party!",
        "Wait!",
        "Wait for me!",
        "Let's wait for my friend.",
        "Wait here.",
        "Wait a minute.",
        "Don't wait for me.",
        "Let's catch the next one.",
        "Let's go!",
        "Can you teleport to me?",
        "Shall we go?",
        "Where should we go?",
        "Which way?",
        "This way.",
        "Follow me.",
        "Let's find other toons.",
        "Meet here.",
        "I think you should choose Toon-up.",
        "I think you should choose Sound.",
        "I think you should choose Drop.",
        "I think you should choose Lure.",
        "I think you should choose Trap.",
        "I need more Merits.",
        "I need more Cogbucks.",
        "I need more Jury Notices.",
        "I need more Stock Options.",
        "I need more Sellbot Suit Parts.",
        "I need more Cashbot Suit Parts.",
        "I need more Lawbot Suit Parts.",
        "I need more Bossbot Suit Parts.",
        "What Toontask are you working on?",
        "Let's work on that.",
        "This isn't what I'm looking for.",
        "This isn't what you need.",
        "I'm going to look for that.",
        "I found what you need.",
        "It isn't on this street.",
        "I haven't found it yet.",
        "Let's use toon-up!",
        "Let's use trap!",
        "Let's use lure!",
        "Let's use sound!",
        "Let's use throw!",
        "Let's use squirt!",
        "Let's use drop!",
        "Nice shot!",
        "Nice gag!",
        "I need more gags.",
        "Missed me!",
        "Bring it on!",
        "Rock and roll!",
        "That's gotta hurt.",
        "Catch!",
        "Special delivery!",
        "Are you still here?",
        "I'm SO scared!",
        "That's going to leave a mark!",
        "Piece of cake!",
        "That was easy!",
        "I need a Toon-Up.",
        "I'm going to use trap.",
        "I'm going to use lure.",
        "I'm going to use drop.",
        "You should pass.",
        "You should use a different gag.",
        "Let's all go for the same cog.",
        "You should choose a different cog.",
        "Go for the weakest cog first.",
        "Go for the strongest cog first.",
        "Save your powerful gags.",
        "Don't use sound on lured cogs.",
        "Hurry!",
        "We can do this!",
        "You did it!",
        "We did it!",
        "Run!",
        "Help!",
        "Phew!",
        "We are in trouble.",
        "I have enough gags.",
        "I need more jellybeans.",
        "Me too.",
        "Hurry up!",
        "One more?",
        "Play again?",
        "Let's play again.",
        "Yes",
        "No",
        "OK",
        ]
        
ans_time = [
        "BILLION YEARS",
        "century",
        "day",
        "decade",
        "era",
        "fiscal year",
        "fortnight",
        "galactic year",
        "hour",
        "instant",
        "jiffy",
        "long weekend",
        "millennium",
        "minute",
        "month",
        "season",
        "week"
        ]
        
ans_time_plural = [
    "BILLION YEARS",
    "centuries",
    "days",
    "decades",
    "eras",
    "fiscal years",
    "fortnights",
    "galactic years",
    "hours",
    "instants",
    "jiffies",
    "long weekends",
    "millennia",
    "minutes",
    "months",
    "seasons",
    "weeks"
    ]
    
ans_xavier = ["Frittata!",
"Nobody has ever survived our initiation process.",
"Really? Is he disabled?",
"Hold. Hold. Hold. Hold. Hold. Hold. Hold. Hold. Hold. Hold. Hold. Hold. Hold.",
"That's why you don't like cereal.",
"Here. 20 bucks. Get out of town. Start a new life.",
"Instead of eating tacos, let's just talk. Oh.",
"I'd like to see this guy pray an abortion.",
"Stay off that knee for a week.",
"This is spreadable bread.",
"Threeito.",
"There's more to life than life.",
"You'd feel so proud of me, mom. I'm not gonna be another Einstein.",
"Bloomin onion on a stick!",
"THEY'RE ALL GONNA LAUGH AT ME",
"Does anyone know how to get to the lake?",
"I'll never sell these arrows.",
"Could use a little coconut.",
"Always tough to kill your dad, but you made the right choice.",
"Fate. Destiny. Fatestiny.",
"I'll take care of that!",
"You're just making me horny!",
"Smells... EXACTLY like my ass.",
"He died during childbirth.",
"You may have just gotten checkmate, but we're playing chinese checkers!",
"I'm gonna name him after me. C'mon, Me.",
"Idiot. He totally missed the board.",
"Let's play a bored game. I'm bored. I win. What's my prize?",
"THINK OF SOME KIDS.SOME KIDS.",
"RIGGINGTON SPORT RIGGER",
"I learned from watching you.",
"Computer! Analysis!",
"OOGA BOOGA CHINAM'N",
"What's the matter? Pussy got your tounge?",
">peak of disappointment",
"I no longer fear your pain fries. (WHOOBOY)",
"Sucker! I would have settled for every other day!",
"I can't remember the memory jogging dance!",
">puke here",
"We're gonna get this little guy laid.",
"I feel like someone is raping me with their eyes.",
"VOW LOCKED IN",
"You don't want it, it's Jap Crap.",
"I could never say no to a virgin.",
"Get me the Hell out of Heaven.",
"Just two more Xaviers left.",
"I fingered myself to death.",
'''"you seem like smart guys" "that's slander"''',
"5-185550-170",
"I swear to Chekhov, I'll cock your clock off.",
"Know when you're defeated. Accept your defecation.",
"Ladies first. (16 HOURS LATER)",
"I assume you're familliar with St. Louis Rules?",
"Well, I think a lot of things, but you're prob'ly gonna cut--",
"Send it where? You decide!",
"But did I whine? No, I turned to the bottle.",
"Flesh colored? How offensive.",
"I'm still holding that raw meat from years ago.",
"This isn't a real Kwanzaa bean.",
"SEXUAL DIARRHEA",
"Dos Ex Machina?",
"Thank you for closing your legs, mommy.",
"This is the 9/11 of noise.",
"I'm going to search far and wide so I can totally tattle to my mom.",
"Chicken bone bread.",
"You seem awfully nervous for a guy who's totally freaked out right now.",
"THE SIX CODE WORDS!",
"You're in the mob?! No wonder I didn't suspect a thing!",
"One grunt for yes. \*grunts twice* Hmm, you want it double bad, huh?",
">building bones",
"Don't worry! Your panties will be bloody soon enough!",
'''Peterson, shut up! New Ryan, say that again! "Peterson, shut up."''',
"WE CAN NO LONGER RELY ON THE SUN'S LIFE-SUSTAINING HEAT!",
"Xavier DOWN UNDA!",
"He's passed on to a better, more euphemistic place.",
"He's coming.. he's coming... INSIDE ME!",
"What do you think I'm back from the dead for, for my health?",
"Do you want some hot coco? Good, and fruity...",
"And if you look to your left, you'll want to look to your right...",
'''"Get away from me! You make me sick!" That's what she said.''',
"Women here have the freedom to do whatever they want! It totally sucks...",
"I even gold polished the Quran! (Can't polish a turd...)",
"SAUSAGE MILK ENERGY BAR",
"I don't feel myself today. That means someone else is feeling me!",
"Okay, I'll see you at church.",
"I've been running for so long, it's like the background is repeating...",
"To be self consumed, sometimes, one must consume one self.",
"Mom spelled backwards is Wow!",
"We can't abort it this far into the pregnancy. The best we can do is torture it a little.",
"Now chow down, or I'll break my vow of nonviolence against your face.",
"Here's the funhouse mirrors for the anorexics.",
"broke-ass pony",
"Dammit! I had money on that game!",
"You were my first, (not counting rape)!",
"This is rubbing against my pole! My princi-pole! Of nonviolence!",
"Trick shot.",
"Cured? Who said there was anything wrong with you?"]
        
def allyeses():
    return json.load(open("json/ans_yes.json"))
    
def allnos():
    return ans_no
    
def eightyes():
    return random.choice(allyeses())
    
def eightno():
    return random.choice(allnos())
    
def allhippos(bot):
    the_e_list = []
    the_e_name_list = []
    for e in bot.emojis:
        if "hippo" in e.name.lower() and e.name not in the_e_name_list and not e.name[-1].isnumeric():
            the_e_list.append(e)
            the_e_name_list.append(e.name)
    return the_e_list

def eighthippo(bot):
    return random.choice(allhippos(bot))
    
def allchannels(guild):
    l = []
    for x in guild.text_channels:
        l.append(x.mention)
    return l
    
def eightchannel(guild):
    l = allchannels(guild)
    if len(l) == 0:
        return "Somehow there's no text channels yet this command is happening"
    return random.choice(l)
    
def allcustomemojis(bot):
    l = []
    for e in bot.emojis:
        if not(e.name.startswith("bn_") or e.name.startswith("owo") or e.name.startswith("dd_") or e.name.startswith("tbc") or e.name.startswith("dickdick") or e.name.startswith("SMILE") or e.name.startswith("dick2") or e.name.startswith("dick3") or e.name.startswith("dick4") or e.name.startswith("dick5") or e.name.startswith("cus_") or e.name.startswith("rot") or e.name.startswith("cera") or e.name.startswith("LR") or "hippo" in e.name or e.guild.id=="306149758320508928"):
            l.append(str(e))
    return l
            
def eightcustomemoji(bot):
    return random.choice(allcustomemojis(bot))
    
def allchats():
    return ans_chat
    
def eightchat():
    return random.choice(allchats())
    
def alltimes(plural):
    if plural:
        return ans_time_plural
    return ans_time
    
def eighttime(plural):
    return random.choice(alltimes(plural))
    
def eightcolor():
    return "#"+str(hex(random.randint(0,0xffffff)))[2:].ljust(6,"0")
    
def allxaviers():
    return ans_xavier
    
def eightxavier():
    return random.choice(allxaviers())

def allaudies():
    l=[]
    for x in listdir("audio/audies"):
        l.append(x.replace(".mp3",""))
    return l
    
def eightaudie():
    return random.choice(allaudies())