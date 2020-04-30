import math

#Figure out how much atime is worth.
def pixelcalc(starttime,endtime):
    delt=endtime-starttime
    n=delt.days*24*60*60
    n+=delt.seconds
    n=math.floor(n/60/15)
    ret=0
    for x in range(1,n+1):
        if x>4*3:
            x=4*3
        ret+=x/100*30
    return math.ceil(ret)

async def kothincreasecooldown(bot,serverid):
    if serverid not in bot.kothcooldowndict.keys():
        bot.kothcooldowndict[serverid]=15
    bot.kothcooldowndict[serverid]+=0.5
    time = copy.deepcopy(bot.koth[4])
    print(f"Cooldown increased to {bot.kothcooldowndict[serverid]}.")
    await asyncio.sleep(10*60)
    if time == bot.koth[4]:
        bot.kothcooldowndict[serverid]-=0.5
        print(f"Cooldown decreased to {bot.kothcooldowndict[serverid]}.")
    else:
        print(f"Cooldown would be decreased, but the hill changed hands.")