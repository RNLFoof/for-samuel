import codecs
import re
from datetime import datetime, timedelta

import discord
import requests
import json
import random
import os
from io import BytesIO
import json
from os import listdir
import asyncio

from modules import basics
from modules.utility import get_emoji

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
    l = json.load(open("json/ans_yes.json", encoding="utf-8"))
    for n,x in enumerate(l):
        l[n] = x.split(";")[0]
    return l

def allnos():
    l = json.load(open("json/ans_no.json", encoding="utf-8"))
    for n,x in enumerate(l):
        l[n] = x.split(";")[0]
    return l

def allmaybes():
    return json.load(open("json/ans_maybe.json", encoding="utf-8"))
    
def eightyes():
    return random.choice(allyeses())
    
def eightno():
    return random.choice(allnos())

def eightmaybe():
    return random.choice(allmaybes())
    
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
    print(len(bot.emojis))
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

def alllinesfromsonic06():
    return json.load(open("json/sonic_06.json", encoding="utf-8"))

def eightlinefromsonic0():
    return random.choice(alllinesfromsonic06())

def allaudies():
    l=[]
    for x in listdir("audio/audies"):
        l.append(x.replace(".mp3",""))
    return l
    
def eightaudie():
    return random.choice(allaudies())


def allanimals():
    return json.load(open("json/animals.json"))


def eightanimal():
    return random.choice(allanimals())

def allads():
    from xml.dom.minidom import parseString

    html_string = """
    <!DOCTYPE html>
    <html><head><title>title</title></head><body><div class="penis">test</div></body></html>
    """

    # extract the text value of the document's <p> tag:
    doc = parseString(html_string)
    paragraph = doc.getElementsByTagName("div")[0]
    content = paragraph.firstChild.data
    print(content)

def allconfirms():
    return ['🙄', '😱', '😒', '😚', '😔', '😨', '😟', '😜', '😤', '🤢', '😅', '☺️', '😕', '<:whatthefuck:358083695544107019>', '\U0001f97a', '😎', '😬', '😘', '😍', '😋', '\U0001f970', '😡', '\U0001f971', '😶', '😌', '\U0001f973', '\U0001f92c', '🤣', '🙃', '😂', '\U0001f92a', '😭', '\U0001f929', '😳', '😠', '😉', '🤕', '😴', '😀', '🤔', '😖', '\U0001f92b', '\U0001f92e', '🤤', '😏', '🤧', '😲', '😊', '😞', '😣', '\U0001f92f', '😩', '😵', '\U0001f928', '🤗', '\U0001f974', '😆']

def eightconfirm():
    return random.choice(allconfirms())

def repuser(bot, user):
    # from modules import basics
    return shownames(bot, user)
    # return "{} {}".format(basics.useremoji(bot, user), shownames(bot,user))

def bar(bot,size,decimal,kind="slice"):
    edict = {}

    if kind=="slice":
        variants=4
        for x in bot.get_guild(556497061072076820).emojis:
            edict[int(x.name[1])] = str(x).replace(x.name,"_")
    elif kind=="circle":
        variants=49
        for x in bot.get_guild(331163970629271553).emojis:
            try:
                edict[int(x.name)] = f"<{'a' if x.animated else ''}:_:{x.id}>"
            except:
                pass
    elif kind=="mini":
        variants=49
        for x in bot.get_guild(364995623528824832).emojis:
            try:
                edict[int(x.name.replace("_",""))] = f"<{'a' if x.animated else ''}:_:{x.id}>"
            except:
                pass
    elif kind=="unicode":
        variants=4
        for n,x in enumerate(list("○◔◑◕●")):
            edict[n] = x

    s=""
    decimal = round(decimal*variants*size)
    for x in range(size):
        if decimal>=variants:
            s+=edict[variants]
            decimal -=variants
        else:
            s+=edict[decimal]
            decimal = 0

    return s


def shownames(bot,member):
    if member.display_name == member.name or basics.truename(bot,member) == member.display_name:
        name = basics.truename(bot,member)
    else:
        name = member.display_name
    return f"{basics.useremoji(bot,member)} {name.replace('@','@­')}"
    # if member.display_name == member.name or basics.truename(bot,member) == member.display_name:
    #     return basics.truename(bot,member)
    # else:
    #     s = fonts(basics.truename(bot,member), "small")
    #
    #     dispname = str(member.display_name)
    #     dispname = dispname.replace("@everyone", "@­everyone")
    #     return "{}{}".format(dispname, s)

def fonts(s, kind):
    fonts = json.load(open("json/fonts.json", encoding='utf-8'))
    if kind in fonts:
        characters = fonts[kind]["characters"]
    else:
        for k,i in fonts.items():
            if kind in i["aliases"]:
                characters = i["characters"]
                break
        else:
            raise Exception(f"{kind} isn't a valid font.")
    ret = ""
    for x in list(s):
        if x in characters:
            ret += characters[x]
        else:
            ret += x
    return ret

    return
    font = []
    finalstring = ""
    f = codecs.open('json/fonts.txt', encoding='utf-8')
    for line in f:
        font.append(line)
    for l in list(s):
        if kind == "aes":
            if l[
               :1] in """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""":
                finalstring += font[0][
                    """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""".index(
                        l[:1]) + 1]
            else:
                finalstring += l[:1]
        elif kind == "small":
            if l[
               :1] in """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""":
                finalstring += font[1][
                    """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""".index(
                        l[:1])]
            else:
                finalstring += l[:1]
        elif kind == "fancy":
            if l[
               :1] in """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""":
                finalstring += font[2][
                    """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""".index(
                        l[:1])]
            else:
                finalstring += l[:1]
        elif kind == "circles":
            if l[
               :1] in """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""":
                finalstring += font[3][
                    """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""".index(
                        l[:1])]
            else:
                finalstring += l[:1]
        elif kind == "jank":
            if l[
               :1] in """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""":
                finalstring += font[4][
                    """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""".index(
                        l[:1])]
            else:
                finalstring += l[:1]
        elif kind == "old":
            if l[
               :1] in """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""":
                finalstring += font[5][
                    """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""".index(
                        l[:1])]
            else:
                finalstring += l[:1]
        elif kind == "lines":
            if l[
               :1] in """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""":
                finalstring += font[6][
                    """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""".index(
                        l[:1])]
            else:
                finalstring += l[:1]
        elif kind == "squares":
            if l[:1].lower() in "opab":
                finalstring += "\\"
            if l[
               :1] in """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""":
                finalstring += font[7][
                    """`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? \\""".index(
                        l[:1])]
            else:
                finalstring += l[:1]
    return finalstring

def highest(l):
    h=l[0]
    for x in l[1:]:
        if x>h:
            x=h
    return h

def lowest(l):
    h=l[0]
    for x in l[1:]:
        if x<h:
            x=h
    return h

async def lit(m, binary=False,ach=False):
    mps = 0
    users = set()
    async for msg in m.channel.history(limit=120000, oldest_first=False, before=m):
        mps +=1
        uh = datetime.utcnow() - timedelta(minutes=2)
        users.add(msg.author)
        if msg.created_at <= uh: break
    if mps == 1:
        mps = 0
    else:
        mps = (mps - 1) / 120
    if binary:
        return mps >= 1 / 4
    if ach:
        return {"mps": mps, "binary": mps >= 1 / 4, "users": users}
    return mps

def pluralstr(string, num):
    if int(num) == num:
        num = int(num)
    if num == 1:
        return str(num) + " " + string
    else:
        return str(num) + " " + string + "s"

def andstr(l,*,an="and"):
    if len(l) == 0:
        return ""
    elif len(l) == 1:
        return l[0]
    elif len(l) == 2:
        return f"{l[0]} {an} {l[1]}"
    else:
        s = ""
        for x in l[:-1]:
            s += f"{x}, "
        return f"{s}{an} {l[-1]}"

def sms(bot, s):
    if s.startswith("/shrug"):
        s = s.replace("/shrug","",1) + " ¯\_(ツ)_/¯"
    elif s.startswith("/tableflip"):
        s = s.replace("/tableflip","",1) + " (╯°□°）╯︵ ┻━┻"
    elif s.startswith("/unflip"):
        s = s.replace("/unflip","",1) + " ┬─┬ ノ( ゜-゜ノ)"

    for e in re.findall(r"<a?:\w+:\d+>",s):
        actualemoji = get_emoji(bot,e)
        if actualemoji != None:
            s = s.replace(e,f"[ {actualemoji.name} : {actualemoji.url} ]")

    return s

def echo(s):
    match = re.match(r"[\s\S]*?([^ ]+)$",s)
    if not match:
        return ""
    else:
        return f'**{match.group(0)}** {match.group(1)} {fonts(match.group(1),"small")} {"ॱ"*len(match.group(1))}'

def covid(bot, country, section, includedate=False):
    if bot.covidstats["confirmed"]["last_updated"].split("T")[0] != str(datetime.utcnow().date()):
        response = requests.get("https://coronavirus-tracker-api.herokuapp.com/all")
        bot.covidstats =  json.loads(response.text)
        basics.save(bot, "covidstats")
        print("Updated covid.")
    j = bot.covidstats[section]
    n = 0
    found = False
    if country:
        for x in j["locations"]:
            if country.lower() in [x["country"].lower(), x["country_code"].lower(), x["province"].lower()]:
                found = True
                n += max(x["history"].values())
    if includedate:
        return n if found else None, j["last_updated"].replace("T", " ").split(".")[0]
    else:
        return n if found else None