import asyncio
import datetime
import random

from classes.AchievementBrowser import AchievementBrowser
from classes.ObamaSilver import ObamaSilver
from classes.ObamaToken import ObamaToken
from modules import utility


def otedit(bot, member, n, affectmax, *, channel=None, type=None, extras={}):
    import modules.basics as basics

    if member.guild.id not in bot.obamatokens.keys():
        bot.obamatokens[member.guild.id] = {}
    if member.guild.id not in bot.obamatokensmax.keys():
        bot.obamatokensmax[member.guild.id] = {}
    if member.guild.id not in bot.obamatokensgiven.keys():
        bot.obamatokensgiven[member.guild.id] = {}

    if member.id not in bot.obamatokens[member.guild.id].keys():
        bot.obamatokens[member.guild.id][member.id] = 0
    if member.id not in bot.obamatokensmax[member.guild.id].keys():
        bot.obamatokensmax[member.guild.id][member.id] = bot.obamatokens[member.guild.id][member.id]
    if member.id not in bot.obamatokensgiven[member.guild.id].keys():
        bot.obamatokensgiven[member.guild.id][member.id] = 0

    bot.obamatokens[member.guild.id][member.id] += n
    if n > 0 and affectmax == True:
        bot.obamatokensmax[member.guild.id][member.id] += n
    if n > 0 and affectmax == False:
        bot.obamatokensgiven[member.guild.id][member.id] += n
    if n < 0:
        bot.obamatokensgiven[member.guild.id][member.id] += n
    if bot.obamatokensgiven[member.guild.id][member.id] < 0:
        bot.obamatokensgiven[member.guild.id][member.id] = 0

    bot.obamatokens[member.guild.id][member.id] = round(bot.obamatokens[member.guild.id][member.id], 2)
    bot.obamatokensmax[member.guild.id][member.id] = round(bot.obamatokensmax[member.guild.id][member.id], 2)
    bot.obamatokensgiven[member.guild.id][member.id] = round(bot.obamatokensgiven[member.guild.id][member.id], 2)
    basics.save(bot,"obamatokens")
    basics.save(bot,"obamatokensmax")
    basics.save(bot,"obamatokensgiven")
    if channel != None:
        guild = channel.guild
        id = member.id

        asyncio.ensure_future(AchievementBrowser.ach_check(bot, guild.get_member(id), channel, "ot",
                                        [bot.obamatokens[guild.id][id],
                                         bot.obamatokensmax[guild.id][id],
                                         bot.obamatokensgiven[guild.id][id],
                                         type,
                                         extras]))

    return bot.obamatokens[member.guild.id][member.id]


def residueedit(bot, member, n, channel):
    import modules.basics as basics

    bot.obamaresidue.setdefault(member.guild.id, {})
    bot.obamaresidue[member.guild.id].setdefault(member.id, 0)
    bot.obamaresiduemax.setdefault(member.guild.id, {})
    bot.obamaresiduemax[member.guild.id].setdefault(member.id, 0)

    bot.obamaresidue[member.guild.id][member.id] += n
    if n > 0:
        bot.obamaresiduemax[member.guild.id][member.id] += n

    bot.obamaresidue[member.guild.id][member.id] = round(bot.obamaresidue[member.guild.id][member.id], 2)
    bot.obamaresiduemax[member.guild.id][member.id] = round(bot.obamaresiduemax[member.guild.id][member.id], 2)
    basics.save(bot,"obamaresidue")
    basics.save(bot,"obamaresiduemax")

    guild = channel.guild
    id = member.id

    asyncio.ensure_future(AchievementBrowser.ach_check(bot, guild.get_member(id), channel, "residue",{
        "residue": bot.obamaresidue[guild.id][id],
        "max": bot.obamaresiduemax[guild.id][id]
    }))

    return bot.obamaresidue[member.guild.id][member.id]

async def spawnbronze(bot, m):
    import modules.basics as basics

    if (
        (
            m.server.id not in bot.bronzetimeout.keys() or bot.bronzetimeout[m.server.id]<datetime.utcnow()
        ) and (
            (
                m.server==bot.epicord and random.randint(1,3000)<=1
            ) or (
                m.server.id=="403747701566734336" and random.randint(1,6000)<=1 and m.channel.id!="403754297277284372"
            )
        ) and False ) or (
        m.author==bot.rnl and m.content.startswith("s!triggerbronze")
    ):
                    
        bot.bronzetimeout[m.server.id]=datetime.utcnow()+timedelta(hours=24)
        basics.save(bot,"bronzetimeout")
        bronze = mf.get_emoji(bot,"394586633422372885")
        total=100
        
        msglst=[]
        async for msg in bot.logs_from(m.channel, limit=100, reverse=True):
            if msg.type==discord.MessageType.default:
                msglst.append(msg)
        random.shuffle(msglst)
        if len(msglst)<total:
            return
        
        editmsg=await mf.say(context,"<:obamabronze:393623097598803987> @here An Obama Bronze Rush has started! 100 Obama Bronzes have spawned in the above 100 messages. Snatch them up before everyone else!\n\nObama Bronze waiting to be collected: "+bronzestr(total))
        bot.bronzerushes.append([total,editmsg,{}])########
        
        await bot.send_message(bot.testserver.get_channel("382641553803444224"),"ignore pinned message;{}".format(editmsg.id))
        try:
            await bot.pin_message(editmsg)
            async for pinannouncemsg in bot.logs_from(m.channel, limit=15, reverse=False):
                if str(pinannouncemsg.type)=="MessageType.pins_add":
                    await bot.delete_message(pinannouncemsg)
                    break
        except:
            pass
            
async def spawnbronze(amsg,index):
    await bot.add_reaction(amsg,bronze)
    rea = await bot.wait_for_reaction(message=amsg,emoji=mf.get_emoji(bot,"394586633422372885"),timeout=None,check=mf.reactornotbot)
    await bot.clear_reactions(amsg)
    
    mf.otedit(bot,rea[1].id,0.04,True,channel=m.channel,type="bronze") 
    
    if rea[1].id not in bot.bronzerushes[index][2].keys():
        bot.bronzerushes[index][2][rea[1].id]=0
    bot.bronzerushes[index][2][rea[1].id]+=1
    
    bot.bronzerushes[index][0]-=1
    if bot.bronzerushes[index][0]==0:
        s="<:obamabronze:393623097598803987> All the Obama Bronze has been collected."
        try:
            await bot.unpin_message(editmsg)
        except:
            pass
    else:
        s="<:obamabronze:393623097598803987>  @here An Obama Bronze Rush has started! 100 Obama Bronzes have spawned in the above 500 messages. Snatch them up before everyone else!\n\nObama Bronze waiting to be collected: "+bronzestr(bot.bronzerushes[index][0])
    for k in bot.bronzerushes[index][2].keys():
        s+="\n{}  ➔  {}".format(mf.useremojiping(bot,k),bronzestr(bot.bronzerushes[index][2][k]))
    await bot.edit_message(bot.bronzerushes[index][1],s)
    for x in msglst[:total]:
        if x not in bot.messages:
            bot.messages.append(x)
        asyncio.ensure_future(spawnbronze(x,len(bot.bronzerushes)-1))
    
def visualtokens(n):
    s=""
    while n>=625:
        s+="<:obamadiamond:397918563354148874>"
        n-=625
    while n>=125:
        s+="<:obamaplatinum:360893654539304961>"
        n-=125
    while n>=25:
        s+="<:obamatoken:349037437827284992>"
        n-=25
    while n>=5:
        s+="<:obamasilver:349436656236888066>"
        n-=5
    while n>=1:
        s+="<:obamabronze:393623097598803987>"
        n-=1
    while n>=0.2:
        s+="<:obamacoal:517243311988408320>"
        n-=0.2
    return s

async def spawntoken(bot,m):
    if (random.randint(1,800) <= 5 and m.channel.id != 403754297277284372) or (m.author == bot.rnl and m.content.startswith("s!gold")):
        if random.randint(1, 5) == 5:
            delayed = True
            await asyncio.sleep(random.randint(60, 120))
        else:
            delayed = False
            await asyncio.sleep(random.randint(3, 5))
        ObamaToken(bot, validfor=datetime.timedelta(minutes=15), messagecount=0, context=utility.fakecontext(bot,m), foreignmessages=[m], delayed=delayed)

async def spawnsilver(bot,m):
    if (random.randint(1,200) <= 1 and m.channel.id != 403754297277284372) or (m.author == bot.rnl and m.content.startswith("s!silver")):
        await asyncio.sleep(random.randint(3, 5))
        ObamaSilver(bot, validfor=datetime.timedelta(minutes=15), messagecount=0, context=utility.fakecontext(bot,m), foreignmessages=[m])
