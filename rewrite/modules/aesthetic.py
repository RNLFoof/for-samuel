import re
from os import listdir

import discord
from PIL import Image


def chart(lol,*,header=True, linelimit = None, align = []):
    # Use a list of lists. Each list if a row. For example:
    # [
        # ["RNL","0"],
        # ["MNIK","1"]
    # ]
    #Establish widths
    if align is None:
        align = []
    align=list(align)
    maxlen = []
    print(align)
    floatdecimalcount = [] # Used to determine how many characters are needed for float decimals
    for x in lol[0]:
        maxlen.append(0)
        floatdecimalcount.append(0)
    for x in lol:
        for n,y in enumerate(x):
            if len(align)<n+1:
                align.append("l")
            # Get the length based on type
            if isinstance(y, str):
                comp = len(y)
            elif isinstance(y, bool):
                comp = 1
            elif isinstance(y, int):
                comp = len(str(y))
            elif isinstance(y, float):
                a, b = str(y).split(".")
                if len(b) > floatdecimalcount[n]:
                    floatdecimalcount[n] = len(b)
                comp = len(str(a)) + floatdecimalcount[n] + 1
            elif isinstance(y, discord.Emoji):
                comp = 1
                #align[-1] = "unwrap"

            if comp > maxlen[n]:
                maxlen[n] = comp

    #Edit bools
    for x in lol:
        for n,y in enumerate(x):
            if isinstance(y, bool):
                x[n] = ("▫"*maxlen[n]*y) + (" "*maxlen[n]*(not y))
            elif isinstance(y, int):
                x[n] = str(y).rjust(maxlen[n]," ")
            elif isinstance(y, float):
                a, b = str(y).split(".")
                x[n] = (a + "." + b.ljust(floatdecimalcount[n], " ")).rjust(maxlen[n]," ")
            elif isinstance(y, discord.Emoji):
                x[n] = str(x[n])

    if len(lol)>=1:
        for x in range(len(lol[0])):
            for y in range(len(lol)):
                if not re.match(r"<a?:\w+:\d+>",lol[y][x]):
                    break
            else:
                align[x]="unwrap"

    #Make string
    s=""
    pages = [] # Used if there's a line limit
    if header:
        s="**__"
    for n2,x in enumerate(lol):
        for n,y in enumerate(x):
            #if n2==0 and header and len(lol)>=1:
            #    s+=hoveremoji(y).strip()
            if align[n] == "unwrap":
                s += f"{y}"
            elif (n2==0 and header) or (align == None or align[n] == "l"):
                s+=f"`­{y.ljust(maxlen[n],' ')}­`"
            elif (align[n] == "r"):
                s+=f"`­{y.rjust(maxlen[n],' ')}­`"
            
            if n2==0 and header:
                s+="__** **__"
            else:
                s+=" "
        s=s.strip()
        if n2==0 and header:
            s=s[:-4]
        s+="\n"
        if linelimit!=None and n2 % linelimit == 0 and n2 !=0:
            pages.append(s)
            s = ""
    if linelimit == None:
        return s
    if s!="":
        pages.append(s)
    return pages
    
def hoveremoji(s, id=520496437042216960):
    s=s.replace(" ","_")
    s=s.replace("\n","__________")
    s=re.sub(r"[']+","",s)
    s=re.sub(r"[^A-Za-z_0-9]","_",s)
    # ret=""
    # for x in list(s):
    #     if re.match(r"[A-Za-z_0-9]",x)!=None:
    #         ret+=x
    return f"<:{s}:{id}>"

async def get_aes_previews(bot):
    emojis = {}
    emojiserver=bot.get_server("476435378153324545")
    for x in listdir("C:\\Users\\Zachary\\Desktop\\kkk\\Non-GML\\ButtBot\\epicord-bot-master\\Images"):
        if x.startswith("base_"):
            wanted=x.replace("base_","").replace(".png","")
            wantedname="aespreview_"+wanted
            for y in emojiserver.emojis:
                if y.name==wantedname:
                    emojis[wanted]=y
                    break
            else:
                overlay = Image.open("Images\\Emojis\\"+x, 'r').convert('RGBA')
                overlaydata = overlay.load()
                avatar = Image.open("Images\\Emojis\\sample_avatar.png", 'r').convert('RGBA')
                pixdata = avatar.load()
                width, height = avatar.size
                for y2 in range(height):
                    for x2 in range(width):
                        if overlaydata[x2, y2] == (255, 0, 0, 255):
                            pixdata[x2, y2] = (0, 0, 0, 0)
                        if overlaydata[x2, y2] == (0, 0, 255, 255):
                            pixdata[x2, y2] = (0,127,255,255)
                avatar.save("blargh.png")
                with open("blargh.png", 'rb') as f:
                    f=f.read()
                    emojis[wanted] = await bot.create_custom_emoji(emojiserver, name=wantedname, image=f)
    return emojis

def get_aes_previews_nonew(bot):
    emojis = {}
    emojiserver=bot.get_guild(476435378153324545)
    for x in emojiserver.emojis:
        emojis[x.name] = x
    return emojis

def indentlist(s):
    return "　"+s.strip().replace("\n","\n　")

def statusemoji(bot,u):
    statusn = ["online", "idle", "dnd", "offline"].index(str(u.status))
    from modules.utility import get_emoji
    return get_emoji(bot,["<:status_online:353069536880361472>", "<:status_idle:353074751947800576>", "<:status_dnd:353069536884424714>",
     "<:status_offline:353069536884555776>"][statusn])
