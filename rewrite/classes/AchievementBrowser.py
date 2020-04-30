import asyncio
import json
import math
import random
import re

import discord

import modules.utility as utility
import modules.ccc as ccc

from classes.DictSavable import DictSavable
from classes.InputMenu import InputMenu
from modules import basics, aesthetic, ot, talking

arrow_r = "<:_:541089103551266827>"


class AchievementBrowser(InputMenu):
    def __init__(self,bot,**kwargs):
        InputMenu.__init__(self,bot,**kwargs)
        # Setup
        defaults = {

        }
        self.reactions = {}
        DictSavable.__init__(self, defaults, kwargs, exclude=["validfor"])

        for x in [328724374540779522,328724374498836500,328724374465282049,328062456905728002]:
            self.adddict[x] = self.movecursor


        if self.context.message.author.id == self.bot.rnl.id:
            self.adddict[331164192776126464] = self.removeachievement

        # Add to dict if needed
        if len(self.context.message.mentions) != 0:
            self.u = self.context.message.mentions[0]
            self.title = "{}'s Achievements, viewed by {}".format(ccc.repuser(self.bot, self.u), ccc.repuser(self.bot, self.context.message.author))
        else:
            self.u = self.context.message.author
            self.title = "{}'s Achievements ".format(ccc.repuser(self.bot, self.u))

        u = self.u
        title = self.title

        AchievementBrowser.establishbaseline(bot, u.id, self.context.message.guild.id)
        achievements = self.getachievements()

        """if self.u.id not in self.bot.ach_tracking.keys():
            self.bot.ach_tracking[u.id] = {}
        for n,x in enumerate(achievements):
            # Add achivement to tracking if missing
            if n not in self.bot.ach_tracking[u.id].keys():
                self.bot.ach_tracking[u.id][n] = []
                for x in range(0, len(x["check"])):
                    self.bot.ach_tracking[u.id][n].append(False)"""

        # Set up grid
        self.width = 9
        self.numberofachs = 0
        typeallowed = json.load(open("json/achievements_allowed.json"))
        for name in json.load(open("json/achievement_order.json")):
            for n,x in enumerate(achievements):
                server = "global" if achievements[n]["global"] else self.context.message.guild.id
                fuck = False
                for y in x["check"]:
                    if y[0] not in typeallowed:
                        fuck = True
                        break
                if fuck:
                    continue
                if (False not in self.bot.ach_tracking[server][u.id][n] or x["special"] == False) and \
                        x["name"] == name:
                    self.numberofachs += 1
        self.height = math.ceil(self.numberofachs / self.width)

        self.grid = []
        for x in range(self.width):
            self.grid.append([])
            for y in range(math.ceil(self.numberofachs / self.width)):
                self.grid[x].append(None)
        x = 0
        y = 0
        for name in json.load(open("json/achievement_order.json")):
            for n,xx in enumerate(achievements):

                server = "global" if achievements[n]["global"] else self.context.message.guild.id

                fuck = False
                for yy in xx["check"]:
                    if yy[0] not in typeallowed:
                        fuck = True
                        break
                if fuck:
                    continue

                if (False not in self.bot.ach_tracking[server][u.id][n] or xx["special"] == False) and \
                        xx["name"] == name:
                    self.grid[x][y] = n
                    x += 1
                    if x == self.width:
                        x = 0
                        y += 1
        self.cursor = [0, 0]

    async def start(self):
        await InputMenu.start(self)

        for x in [":bn_ba:328062456905728002", ":bn_do:328724374498836500", ":bn_up:328724374540779522",":bn_fo:328724374465282049"]:
            asyncio.ensure_future(self.messages[0].add_reaction(x))

        await self.updatemessage(0)

    async def getlayout(self,index,*,final=False):
        width = self.width
        height = self.height
        title = self.title
        numberofachs = self.numberofachs
        grid = self.grid
        u = self.u
        context = self.context
        cursor = self.cursor
        achievements = self.getachievements()

        progress = [0, 0]  # 0/1
        s = ""
        n = 0
        added = 0
        secretsearned = 0
        for y in range(height):
            x = 0
            # for x in range(width+1):
            while x <= width and added <= numberofachs:
                # Secret?
                try:
                    secret = achievements[grid[x][y]]["secret"]
                except:
                    secret = False
                # Progress
                try:
                    server = "global" if achievements[grid[x][y]]["global"] else context.message.guild.id
                    if False not in self.bot.ach_tracking[server][u.id][grid[x][y]]:
                        if secret:
                            secretsearned += 1
                        else:
                            progress[0] += 1
                    if secret == False:
                        progress[1] += 1
                except:
                    pass
                # Skip when past what's needed
                if n > numberofachs:
                    x += 1
                    continue

                # Figure out what to highlight
                try:
                    server = "global" if achievements[grid[x][y]]["global"] else context.message.guild.id
                except:
                    pass
                try:
                    serverm1 = "global" if achievements[grid[x - 1][y]]["global"] else context.message.guild.id
                except:
                    pass

                left = True
                right = True
                # This stuff is from the edges
                if x == 0:
                    left = False
                if x == width:
                    right = False
                if n == numberofachs:
                    right = False
                # This stuff is for earned
                try:
                    if left == True:
                        if False in self.bot.ach_tracking[serverm1][u.id][grid[x - 1][y]]:
                            left = False
                    if right == True:
                        if False in self.bot.ach_tracking[server][u.id][grid[x][y]]:
                            right = False
                except:
                    pass
                # Set arrow thing
                arrowtype = 0  # No arrow
                if cursor == [x, y]:
                    arrowtype = 1  # Left
                if cursor == [x - 1, y]:
                    arrowtype = 2  # Right
                # Add highlight emojis
                if [left, right] == [True, True]:
                    s += ["<a:__:406627625109422080>", "<a:__:406627723621171200>", "<a:__:406628574041473026>"][
                        arrowtype]
                if [left, right] == [False, True]:
                    s += ["<a:__:406629250825715723>", "<a:__:406629695938101278>", "<a:__:406631834043285514>"][
                        arrowtype]
                if [left, right] == [True, False]:
                    s += ["<a:__:406633397868298240>", "<a:__:406633398069624832>", "<a:__:406633397960835083>"][
                        arrowtype]
                if [left, right] == [False, False]:
                    s += ["<:__:406626779965685762>", "<:__:406627050959536129>", "<:__:406627335471759371>"][arrowtype]
                # Add the achivement emoji, it'll fail if there isn't one
                try:
                    s += achievements[grid[x][y]]["icon"]
                    added += 1
                except:
                    pass
                n += 1
                x += 1
            s += "\n"
            n -= 1

        # Secret?
        server = "global" if achievements[self.getgridpos()]["global"] else context.message.guild.id

        secret = achievements[self.getgridpos()]["secret"]
        if context.message.guild == None and False not in self.bot.ach_tracking[server][u.id][self.getgridpos()]:
            secret = False

        # Who else has?
        others = []
        for uk in context.message.guild.members:
            uk = uk.id
            #try:
            if uk in self.bot.ach_tracking[server]:
                if self.getgridpos() in self.bot.ach_tracking[server][uk]:
                    m = context.message.guild.get_member(uk)
                    if False not in self.bot.ach_tracking[server][uk][
                        self.getgridpos()] and m != None:
                        others.append(basics.useremoji(self.bot, m, default="aes"))
            #except:
                #pass

        # Make embed
        embed = discord.Embed(
            title=title)  # (round(fill)*"█")+(round(50-fill)*" ")+"­`­   {}%".format(round(fill/50*100),2)
        # description="{}/{} Achievements Earned.\n{}  {}%".format(progress[0],progress[1], "`­"+str(math.floor(progress[0]/progress[1]*50)*"█")+str((50-math.floor(progress[0]/progress[1]*50))*" ")+"­`" ,math.floor(progress[0]/progress[1]*100))

        pos = self.getgridpos()
        s3 = ""
        for n, x in enumerate(self.bot.ach_tracking[server][u.id][pos]):
            if x:
                    s3 += ccc.bar(self.bot, 1, 1, kind="circle")
            else:

                history = "fuckyou"
                if server in self.bot.ach_tracking_history:
                        if u.id in self.bot.ach_tracking_history[server]:
                                if pos in self.bot.ach_tracking_history[server][u.id]:
                                        history = self.bot.ach_tracking_history[server][u.id][pos]

                self.bot.ach_tracking_count_hidden.setdefault(server,{})
                if len(achievements[pos]["check"][n]) == 3 and type(achievements[pos]["check"][n][2]) == str:
                    try:
                        s3 += ccc.bar(self.bot, 1, eval(achievements[pos]["check"][n][2]), kind="circle")
                    except:
                        s3 += ccc.bar(self.bot, 1, 0, kind="circle")
                elif achievements[self.getgridpos()][
                    "secret"] and u.id in self.bot.ach_tracking_count_hidden[server] and (pos, n) in \
                        self.bot.ach_tracking_count_hidden[server][
                            u.id].keys():  # Checks if secret, can't use secret variable because it'll reveal in DMs
                                        s3 += ccc.bar(self.bot, 1, self.bot.ach_tracking_count_hidden[server][u.id][(pos, n)] /
                        achievements[pos]["check"][n][2], kind="circle")
                elif achievements[self.getgridpos()][
                    "secret"] == False and u.id in self.bot.ach_tracking_count[server] and (pos, n) in \
                        self.bot.ach_tracking_count[server][u.id]:
                                                            s3 += ccc.bar(self.bot, 1,
                        self.bot.ach_tracking_count[server][u.id][(pos, n)] /
                        achievements[pos]["check"][n][2], kind="circle")
                else:
                                        s3 += ccc.bar(self.bot, 1, 0, kind="circle")

        s2 = ""
        index = achievements[self.getgridpos()]
        user = u
        for x in index["reward"]:
            if x[0] == "clothing":
                s2 += "\n{}".format(x[1])#""\n{}".format(self.bot.chinfo[x[1]][2])
            if x[0] == "ot":
                s2 += "\n{} Obama Tokens".format(x[1])
            if x[0] == "en":
                s2 += "\nEvernick Character Discount"
        if s2 != "":
            s2 = "\n\nRewards:" + s2

        add = ""
        for n, x in enumerate(s.split("\n")[:-1]):
            add += x + "\n"
            if add.count("\n") == 1:
                embed.add_field(name="­", value=add, inline=False)
                add = ""
        if add != "":
            embed.add_field(name="­", value=add, inline=False)
        # embed.add_field(name="­", value=s, inline=False)

        propertiesstr=""
        if index["global"]:
            propertiesstr += " " + aesthetic.hoveremoji("GLOBAL")
        if propertiesstr!="":
            propertiesstr="　　　　　　　"+propertiesstr

        if secret:
            embed.add_field(name="{} __**{}**__".format(index["icon"], "???") + propertiesstr,
                            value="???" + "\n\n" + "Progress:\n" + s3 + s2 + "\n­", inline=False)
        else:
            embed.add_field(name="{} __**{}**__".format(index["icon"], index["name"]) + propertiesstr,
                            value=index["desc"] + "\n\n" + "Progress:\n" + s3 + s2 + "\n­", inline=False)

        # Progress

        # How many people have
        havestr = "{} people have this achievement.".format(len(others))
        if havestr == "1 people have this achievement.":
            havestr = "1 person has this achievement."
        if havestr == "0 people have this achievement.":
            havestr = "Nobody has this achievement."
        embed.add_field(name=havestr, value="".join(others) + "­", inline=False)
        if secretsearned == 0:
            secretstr = ""
        else:
            secretstr = f" (+{secretsearned})"  # "`­"+str(math.floor((progress[0]+secretsearned)/progress[1]*50)*"█")+str((50-math.floor((progress[0]+secretsearned)/progress[1]*50))*" ­")+"`"
        embed.add_field(
            name="　" * 15 + "­" + "You've earned {}/{}{} achievements.".format(progress[0], progress[1], secretstr),
            value="{}  {}%".format(ccc.bar(self.bot, 16, (progress[0] + secretsearned) / progress[1]),
                                   math.floor((progress[0] + secretsearned) / progress[1] * 100)), inline=False)

        return embed

    async def movecursor(self,payload):
        if payload.message_id == self.messages[0].id:
            grid = self.grid
            cursor = self.cursor
            
            if payload.emoji.name == "bn_fo":
                cursor[0] += 1
                if cursor[0] == self.width:
                    cursor[0] = 0
                while self.getgridpos() == None:
                    cursor[0] += 1
                    if cursor[0] == self.width:
                        cursor[0] = 0
            elif payload.emoji.name == "bn_ba":
                cursor[0] -= 1
                if cursor[0] == -1:
                    cursor[0] = self.width - 1
                while self.getgridpos() == None:
                    cursor[0] -= 1
                    if cursor[0] == -1:
                        cursor[0] = self.width - 1
            elif payload.emoji.name == "bn_do":
                cursor[1] += 1
                if cursor[1] == self.height:
                    cursor[1] = 0
                while self.getgridpos() == None:
                    cursor[1] += 1
                    if cursor[1] == self.height:
                        cursor[1] = 0
            elif payload.emoji.name == "bn_up":
                cursor[1] -= 1
                if cursor[1] == -1:
                    cursor[1] = self.height - 1
                while self.getgridpos() == None:
                    cursor[1] -= 1
                    if cursor[1] == -1:
                        cursor[1] = self.height - 1

            await self.removeinputreaction(payload)
            await self.updatemessage(0)

    @staticmethod
    def getachievements():
        l = json.load(open("json/achievements.json",encoding="utf-8"))
        for d in l:
            d.setdefault("global",False)
            d.setdefault("history",[])
        return l

    @staticmethod
    async def ach_display(bot, user, channel, index):
        achievements = AchievementBrowser.getachievements()
        index = achievements[index]
        embed = discord.Embed(title="**__Achievement Unlocked!__**")

        s = ""
        for x in index["reward"]:
            if x[0] == "clothing":
                s += "\n{} (equip with `s!ch {}`)".format(x[1], x[1])
                server = "global" if index["global"] else channel.guild.id
                bot.hippoclothing.setdefault(server,{})
                bot.hippoclothing[server].setdefault(user.id, set())
                bot.hippoclothing[server][user.id].add(x[1])
                basics.save(bot, "hippoclothing")
            if x[0] == "ot":
                oooooo = ot.otedit(bot, user, x[1], True, channel=channel)
                s += "\n{} Obama Tokens (total is now {})".format(x[1], oooooo)
            if x[0] == "en":
                s += "\nEvernick Character Discount"
        if s != "":
            # embed.set_footer(text="Rewards:\n"+s)
            s = "\n\nRewards:" + s

        embed.add_field(name="{} **{}**".format(index["icon"], index["name"]), value=index["desc"] + s, inline=False)

        if index["secret"]:
            embed.set_footer(
                text="Because of the ease of obtaining this achievement, it's more valuable as a surprise than a challenge. Keep its requirements to yourself.")
            await user.send(embed=embed)
            # await asyncio.sleep(random.randint(60*2,60*5))

            # ADD A DAILY POST ANNOUNCEMENT

            # main = bot.epicord.get_channel("112760669178241024")
            # for x in range(random.randint(200, 1000)):
            #     await bot.wait_for_message(channel=main)
            # embed = discord.Embed(title="**__Achievement Unlocked!__**")
            # embed.add_field(name="❔ **???**", value="???", inline=False)
            # await talking.say(main, content=ccc.repuser(bot, user), embed=embed, tts=bot.tts)
        else:
            embed.set_footer(text="Use s!ach to see all achievements.")
            await channel.send(user.mention, embed=embed)
        # Achievements for getting achiemenets
        info = []
        for n, i in enumerate(achievements):
            server = "global" if i["global"] else user.guild.id
            if n not in bot.ach_tracking[server][user.id].keys():
                bot.ach_tracking[server][user.id][n] = []
                for x in range(0, len(achievements[n][3])):
                    bot.ach_tracking[server][user.id][n].append(False)
            info.append(bot.ach_tracking[server][user.id][n])
            await AchievementBrowser.ach_check(bot, user, channel, "ach", info)

    @staticmethod
    async def ach_check(bot, user, channel, achtype, info):
        # if user.id == "277449474476081153":
        #     bot.ach_tracking["277449474476081153"] = {}  # Wipes same guy constantly
        if user.bot: return
        if type(channel) != discord.TextChannel: return

        bot.ach_tracking.setdefault("global",{})
        bot.ach_tracking.setdefault(user.guild.id,{})
        bot.ach_tracking["global"].setdefault(user.id,{})
        bot.ach_tracking[user.guild.id].setdefault(user.id,{})

        bot.ach_tracking_count.setdefault("global",{})
        bot.ach_tracking_count.setdefault(user.guild.id,{})
        bot.ach_tracking_count["global"].setdefault(user.id,{})
        bot.ach_tracking_count[user.guild.id].setdefault(user.id,{})
            
        achievements = AchievementBrowser.getachievements()
        
        for n, i in enumerate(achievements):
            server = "global" if i["global"] else user.guild.id
            # Add achivement to tracking if missing
            if n not in bot.ach_tracking[server][user.id].keys():
                bot.ach_tracking[server][user.id][n] = []
                for x in range(0, len(achievements[n]["check"])):
                    bot.ach_tracking[server][user.id][n].append(False)
            # Check what's important
            if False in bot.ach_tracking[server][user.id][n]:
                try:
                    for x in range(0, len(achievements[n]["check"])):
                        # Make true or add to if requirements met
                        if bot.ach_tracking[server][user.id][n][x] == False:
                            # INTERMISSION: Add to history
                            bot.ach_tracking_history.setdefault(server,{})
                            bot.ach_tracking_history[server].setdefault(user.id,{})
                            if len(i["history"]) >= x+1:
                                if achtype == i["history"][x][0]:
                                    bot.ach_tracking_history[server][user.id].setdefault(n,{})
                                    history = bot.ach_tracking_history[server][user.id][n]
                                    history.setdefault(x,[])
                                    m = info
                                    if eval(achievements[n]["history"][x][1]):
                                        history[x].append(eval(achievements[n]["history"][x][2]))
                            # INTERMISSION OVER
                            u = user
                            if achtype == achievements[n]["check"][x][0]:
                                # basic True/False, str means it's just for display
                                if len(achievements[n]["check"][x]) == 2 or (
                                        len(achievements[n]["check"][x]) == 3 and type(achievements[n]["check"][x][2]) is str):
                                    m = info
                                    history="fuckyou"
                                    if n in bot.ach_tracking_history[server][user.id]:
                                        history = bot.ach_tracking_history[server][user.id][n]
                                    bot.ach_tracking[server][user.id][n][x] = eval(
                                        achievements[n]["check"][x][1])
                                # Numbers
                                else:
                                    if (n, x) not in bot.ach_tracking_count[server][user.id].keys():
                                        bot.ach_tracking_count[server][user.id][(n, x)] = 0
                                    m = info
                                    bot.ach_tracking_count[server][user.id][(n, x)] += eval(achievements[n]["check"][x][1])
                                    if bot.ach_tracking_count[server][user.id][(n, x)] >= achievements[n]["check"][x][2]:
                                        bot.ach_tracking[server][user.id][n][x] = True
                        # Reset if needed
                        if achtype == achievements[n]["reset"][x][0]:
                            if eval(achievements[n]["reset"][x][1]):
                                if server in bot.ach_tracking_history:
                                    if user.id in bot.ach_tracking_history[server]:
                                        if n in bot.ach_tracking_history[server][user.id]:
                                            if x in bot.ach_tracking_history[server][user.id][n]:
                                                del bot.ach_tracking_history[server][user.id][n][x]
                                if (n, x) in bot.ach_tracking_count[server][user.id]:
                                    bot.ach_tracking_count[server][user.id][(n, x)] = 0
                                bot.ach_tracking[server][user.id][n][x] = False
                    if False not in bot.ach_tracking[server][user.id][n]:
                        asyncio.ensure_future(AchievementBrowser.ach_display(bot, user, channel, n))
                except Exception as e:
                    f"Achievement Error {type(e).__name__}: {e}\n{i['name']}\n{i['check']}\n{info}"
        basics.save(bot, "ach_tracking")
        basics.save(bot, "ach_tracking_count")
        basics.save(bot, "ach_tracking_history")

    @staticmethod
    def establishbaseline(bot,userid,serverid):
        achievements = AchievementBrowser.getachievements()

        bot.ach_tracking.setdefault("global",{})
        bot.ach_tracking.setdefault(serverid,{})
        bot.ach_tracking["global"].setdefault(userid,{})
        bot.ach_tracking[serverid].setdefault(userid,{})

        for n, i in enumerate(achievements):
            server = "global" if i["global"] else serverid
            # Add achivement to tracking if missing
            if n not in bot.ach_tracking[server][userid].keys():
                bot.ach_tracking[server][userid][n] = []
                for x in range(0, len(achievements[n]["check"])):
                    bot.ach_tracking[server][userid][n].append(False)

    async def removeachievement(self, payload):
        if payload.user_id == self.bot.rnl.id:
            bot = self.bot
            context = self.context
            pos = self.getgridpos()
            ach = self.getachievements()[pos]
            u = self.u.id
            server = "global" if ach["global"] else context.message.guild.id
            s = ""

            if u in bot.ach_tracking[server]:
                if pos in bot.ach_tracking[server][u]:
                    s += str(bot.ach_tracking[server][u][pos]) + "\n"
                    del bot.ach_tracking[server][u][pos]
            if u in bot.ach_tracking_count[server]:
                for x in list(bot.ach_tracking_count[server][u].keys()):
                    if x[0] == pos:
                        s += str(bot.ach_tracking_count[server][u][x]) + "\n"
                        del bot.ach_tracking_count[server][u][x]
            if u in bot.ach_tracking_history[server]:
                if pos in bot.ach_tracking_history[server][u]:
                    s += str(bot.ach_tracking_history[server][u][pos]) + "\n"
                    del bot.ach_tracking_history[server][u][pos]

            basics.save(bot, "ach_tracking")
            basics.save(bot, "ach_tracking_count")
            basics.save(bot, "ach_tracking_history")
            self.establishbaseline(bot, u, context.message.guild.id)

            if ach["secret"]:
                await talking.say(context, f"<@{u}>, RNL has removed your progress on {ach['icon']} because he doesn't think it was earned properly, most likley because of a bug. Feel free to correct him if he's dumb.")
                await talking.say(context, f"<@{u}> {ach['name']}\n{s}", channel=bot.rnl)
            else:
                await talking.say(context, f"<@{u}>, RNL has removed your progress on {ach['name']} because he doesn't think it was earned properly, most likley because of a bug. Feel free to correct him if he's dumb.\n\nOld values:\n{s}")

            await self.removeinputreaction(payload)
            await self.updatemessage(0)
        
    def getgridpos(self):
        return self.grid[self.cursor[0]][self.cursor[1]]