import asyncio
import copy
from datetime import datetime

import discord
import random
from discord.ext import commands
from discord.ext.commands import Cog

import modules.ccc as ccc
import modules.talking as talking
import modules.basics as basics
from modules import koth, utility


class Time(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True) #,
                      #aliases=["kingofthehill", "qoth", "queenofthehill", "loth", "loliofthehill", "foth",
                      #         "furryofthehill", "coth", "cheeseofthehill"])
    async def kothnew(self, context):
        """Makes you king. Or whatever.

        The king of the hill will get an automatic crown reaction to their messages. You can also become the queen/loli/furry/cheese, based on what alias you use. Or whatever you type after the command. Use [bot] to make the bot take it. After that, you can put an emoji in brackets to get any emoji.
        You get an increasingly sexy secondary reaction as you hit 15 minutes, two hours, six hours, and 24 hours uninterupted.
        You can view the top 10 with [top], [high], or [score]. You can use [long] to view the top 500. You can view everyone's best scores with [best], [one], or [records].
        See who's currently king and for how long with [time].
        When taking the hill, whoever is already on it gets 5 seconds to say something and defend their title. If you try to take it from somebody you didn't want to take it from, if you say . before they defend, it gets canceled.
        The command has a starting cooldown of 15 seconds. When the hill is defended successfully, and the attacker isn't the king, that cooldown is increased by half a second for the next 10 minutes.
        Scores earned after koth's death have a skull next to them. You can hide all the death scores with [legacy]."""
        bot = self.bot
        m = context.message

        q = basics.contentq(context.message.content)
        q, specialemoji = basics.subcommands(context, q, ["EMOJI"])

        words = " ".join(q)
        legacy = "[legacy]" in words
        if "[bs]" in words and context.message.author.id == self.bot.rnl.id:
            self.bot.koth = copy.deepcopy(self.bot.kothlast)
            basics.save(bot,"koth")
            await talking.reply(context, "Cool.")
            return

        if "[time]" in words:
            secs = (datetime.utcnow() - self.bot.koth[4]).seconds + (
                        (datetime.utcnow() - self.bot.koth[4]).days * 24 * 60 * 60)
            mins = 0
            hours = 0
            while secs >= 60:
                mins += 1
                secs -= 60
            while mins >= 60:
                hours += 1
                mins -= 60
            await talking.reply(context,
                           "{} has been {} for the last {}, {}, and {}. If the hill was lost now, it would be worth {} pixels.".format(
                               self.bot.koth[1],
                               self.bot.koth[2],
                               ccc.pluralstr("hour", hours),
                               ccc.pluralstr("minute", mins),
                               ccc.pluralstr("second", secs),
                               koth.pixelcalc(self.bot.koth[4], datetime.utcnow()))
                           )
            return
        if "[top]" in words or "[high]" in words or "[score]" in words:
            embed = discord.Embed(title="King of the Hill Highscores", type="rich")
            high = self.bot.kothhigh[::-1][:10]
            numbers = "<:bn_1:327896448232325130> <:bn_2:327896448505217037> <:bn_3:327896452363976704> <:bn_4:327896452464508929> <:bn_5:327896454733627403> <:bn_6:327896456369274880> <:bn_7:327896458067968002> <:bn_8:327896459070537728> <:bn_9:327896459292704769> <:bn_10:327896459477385226>".split(
                " ")

            s = ""
            for x in range(0, len(high)):
                if legacy and high[x][4]:
                    continue
                u = self.bot.epicord.get_member(high[x][0])
                limit = 23
                if len(u.display_name) > limit:
                    name = u.display_name[:limit - 3] + "..."
                else:
                    name = "<@!" + high[x][0] + ">"
                if x <= 9:
                    s += numbers[x] + basics.useremoji(self.bot, high[x][0]) + name + "\n"
                else:
                    s += "`" + str(x + 1) + "`" + basics.useremoji(self.bot, high[x][0]) + name + "\n"
            embed.add_field(name="#　User", value=s, inline=True)

            s = ""
            for x in high:
                if legacy and x[4]:
                    continue
                if x[2] == None:
                    emoji = "👑"
                elif len(x[2]) == 1:
                    emoji = x[2]
                else:
                    emoji = "<" + x[2] + ">"
                name = x[1]
                limit = 15
                if len(name) > limit:
                    name = name[:limit - 3] + "..."
                s += emoji + name + "\n"
            embed.add_field(name="Title", value=s, inline=True)

            s = ""
            for x in high:
                if legacy and x[4]:
                    continue
                seconds = x[3]
                emoji = "<:bl:230481089251115018>"
                if seconds > (60 * 60) * 24:
                    emoji = "<:tier4:348277627598929922>"
                elif seconds > (60 * 60) * 6:
                    emoji = "<:tier3:348279546765901826>"
                elif seconds > (60 * 60) * 2:
                    emoji = "<:tier2:348276583741521921>"
                elif seconds > 60 * 15:
                    emoji = "<:tier1:348266722526101505>"
                if x[4]:
                    emoji = "💀"
                minutes = 0
                while seconds >= 60:
                    seconds -= 60
                    minutes += 1
                hours = 0
                while minutes >= 60:
                    minutes -= 60
                    hours += 1
                minutes += round(seconds / 60, 2)
                s += emoji + str(hours) + " hours, " + str(minutes) + " min.\n"
            embed.add_field(name="Time", value=s, inline=True)

            s = "You don't have a score on this list."
            high = self.bot.kothhigh
            for x in range(0, len(high)):
                if high[x][0] == context.message.author.id:
                    s = "Your highest placement is {} out of {}.".format(len(high) - x, len(high))
            embed.set_footer(text=s)

            await mf.say(context, embed=embed)
            return
        # WOAH MAMA
        if "[long]" in words:
            numbers = "<:bn_1:327896448232325130> <:bn_2:327896448505217037> <:bn_3:327896452363976704> <:bn_4:327896452464508929> <:bn_5:327896454733627403> <:bn_6:327896456369274880> <:bn_7:327896458067968002> <:bn_8:327896459070537728> <:bn_9:327896459292704769> <:bn_10:327896459477385226>".split(
                " ")
            msg = await talking.say(context, "­")
            for n in numbers + [":bn_up:328724374540779522", ":bn_do:328724374498836500"]:
                asyncio.ensure_future(self.bot.add_reaction(msg, n.replace("<", "").replace(">", "")))
            page = 0
            while True:
                embed = discord.Embed(title="Extended King of the Hill Highscores (Page {})".format(page + 1),
                                      type="rich")
                place = 0
                names = ["#　User", "Title", "Time"]
                for place in range(0 + (page * 5), 5 + (page * 5)):
                    # print("uh")
                    high = self.bot.kothhigh[::-1][(place * 10):10 + (place * 10)]
                    s = ""
                    for x in range(0, len(high)):
                        if legacy and high[x][4]:
                            continue
                        u = context.message.guild.get_member(high[x][0])
                        if u == None:
                            u = self.bot.epicord.get_member(high[x][0])
                        limit = 16
                        if len(u.display_name) > limit:
                            name = u.display_name[:limit - 3] + "…"
                        else:
                            name = "<@!" + high[x][0] + ">"
                        if x + (place * 10) <= 9:
                            s += numbers[x] + basics.useremoji(self.bot, high[x][0]) + name + "\n"
                        else:
                            s += "`" + str(x + 1 + (place * 10)) + ")`" + basics.useremoji(self.bot,
                                                                                       high[x][0]) + name + "\n"
                    embed.add_field(name=names[0], value=s, inline=True)

                    s = ""
                    for x in high:
                        if legacy and x[4]:
                            continue
                        if x[2] == None:
                            emoji = "👑"
                        elif len(x[2]) <= 10:
                            emoji = x[2]
                        else:
                            if utility.get_emoji(self.bot, x[2]) != None:
                                emoji = "<" + x[2] + ">"
                            else:
                                emoji = str(utility.get_emoji(self.bot, x[2].split(":")[1]))
                        name = x[1]
                        limit = 15
                        if len(name) > limit:
                            name = name[:limit - 3] + "…"
                        s += emoji + name + "\n"
                    embed.add_field(name=names[1], value=s, inline=True)

                    s = ""
                    for x in high:
                        if legacy and x[4]:
                            continue
                        seconds = x[3]
                        emoji = "<:bl:230481089251115018>"
                        if seconds > (60 * 60) * 24:
                            emoji = "<:tier4:348277627598929922>"
                        elif seconds > (60 * 60) * 6:
                            emoji = "<:tier3:348279546765901826>"
                        elif seconds > (60 * 60) * 2:
                            emoji = "<:tier2:348276583741521921>"
                        elif seconds > 60 * 15:
                            emoji = "<:tier1:348266722526101505>"
                        if x[4]:
                            emoji = "💀"
                        minutes = 0
                        while seconds >= 60:
                            seconds -= 60
                            minutes += 1
                        hours = 0
                        while minutes >= 60:
                            minutes -= 60
                            hours += 1
                        minutes += round(seconds / 60, 2)
                        s += emoji + str(hours) + "h, " + str(round(minutes, 2)) + "m\n"
                    embed.add_field(name=names[2], value=s, inline=True)

                    names = ["­", "­", "­"]

                s = "You don't have a score on this list."
                high = self.bot.kothhigh
                for x in range(0, len(high)):
                    if high[x][0] == context.message.author.id:
                        s = "Your highest placement is {} out of {}.".format(len(high) - x, len(high))
                embed.set_footer(text=s)

                msg = await talking.edit(context, msg, embed=embed)

                def tempcheck(reaction, user):
                    return user.id != self.bot.me.id

                rea = await self.bot.wait_for_reaction(self.bot.buttons, message=msg, check=tempcheck, timeout=120)
                if rea == None:
                    await self.bot.clear_reactions(msg)
                    break
                else:
                    await self.bot.remove_reaction(msg, rea[0].emoji, rea[1])
                    if rea[0].emoji.name == "bn_up":
                        page -= 1
                    elif rea[0].emoji.name == "bn_do":
                        page += 1
                    else:
                        page = int(rea[0].emoji.name.replace("bn_", "")) - 1
                    if page == -1:
                        page = 9
                    elif page == 10:
                        page = 0
            return
        # WOAH MAMA again
        if "[best]" in words or "[one]" in words or "[records]" in words:
            embed = discord.Embed(title="Top King of the Hill Scores For Each Player", type="rich")
            high = self.bot.kothhigh[::-1]
            numbers = "<:bn_1:327896448232325130> <:bn_2:327896448505217037> <:bn_3:327896452363976704> <:bn_4:327896452464508929> <:bn_5:327896454733627403> <:bn_6:327896456369274880> <:bn_7:327896458067968002> <:bn_8:327896459070537728> <:bn_9:327896459292704769> <:bn_10:327896459477385226>".split(
                " ")
            playersshown = []

            s = ""
            s2 = ""
            s3 = ""
            for x in range(0, len(high)):
                if legacy and high[x][4]:
                    continue
                if high[x][0] not in playersshown:
                    playersshown.append(high[x][0])
                    u = context.message.server.get_member(high[x][0])
                    if u == None:
                        u = self.bot.epicord.get_member(high[x][0])
                    limit = 16
                    name = "<@!" + high[x][0] + ">"
                    if u != None:
                        if len(u.display_name) > limit:
                            name = u.display_name[:limit - 3] + "…"
                        else:
                            name = "<@!" + high[x][0] + ">"
                    if x <= 9:
                        s += numbers[x] + basics.useremoji(self.bot, high[x][0]) + name + "\n"
                    else:
                        s += "`" + str(x + 1) + "`" + basics.useremoji(self.bot, high[x][0]) + name + "\n"

                    if high[x][2] == None:
                        emoji = "👑"
                    elif len(high[x][2]) == 1:
                        emoji = high[x][2]
                    else:
                        emoji = str(utility.get_emoji(self.bot, high[x][2].split(":")[1]))
                    name = high[x][1]
                    limit = 15
                    if len(name) > limit:
                        name = name[:limit - 3] + "…"
                    s2 += emoji + name + "\n"

                    seconds = high[x][3]
                    emoji = "<:bl:230481089251115018>"
                    if seconds > (60 * 60) * 24:
                        emoji = "<:tier4:348277627598929922>"
                    elif seconds > (60 * 60) * 6:
                        emoji = "<:tier3:348279546765901826>"
                    elif seconds > (60 * 60) * 2:
                        emoji = "<:tier2:348276583741521921>"
                    elif seconds > 60 * 15:
                        emoji = "<:tier1:348266722526101505>"
                    if high[x][4]:
                        emoji = "💀"
                    minutes = 0
                    while seconds >= 60:
                        seconds -= 60
                        minutes += 1
                    hours = 0
                    while minutes >= 60:
                        minutes -= 60
                        hours += 1
                    minutes += round(seconds / 60, 2)
                    s3 += emoji + str(hours) + " hours, " + str(minutes) + " min.\n"
            embed.add_field(name="#　User", value=s[:1024], inline=True)
            embed.add_field(name="Title", value=s2[:1024], inline=True)
            embed.add_field(name="Time", value=s3[:1024], inline=True)

            s = "You don't have a score on this list."
            high = self.bot.kothhigh
            for x in range(0, len(high)):
                if high[x][0] == context.message.author.id:
                    s = "Your highest placement is {} out of {}.".format(len(high) - x, len(high))
            embed.set_footer(text=s)

            await talking.say(context, embed=embed)
            return

        if context.message.channel.id != "160197704226439168" and context.message.guild.id != self.bot.testserver.id:
            await talking.reply(context, "This only works in the bot channel.")
            return

        if context.message.author.bot:
            await talking.reply(context,
                           "Non-RSRB bots can't become king, because multiple people would be able to defend the hill.")
            return

        seconds = (datetime.utcnow() - self.bot.kothcooldown).seconds
        if m.guild.id not in self.bot.kothcooldowndict.keys():
            self.bot.kothcooldowndict[m.guild.id] = 15
        if seconds < self.bot.kothcooldowndict[m.guild.id]:
            if m.guild.id not in self.bot.kothcooldownnotovertolddict.keys():
                self.bot.kothcooldownnotovertolddict[m.guild.id] = []
            if m.author.id not in self.bot.kothcooldownnotovertolddict[m.guild.id]:
                await talking.reply(context, "Please wait, the cooldown's not over yet.")
                self.bot.kothcooldownnotovertolddict[m.guild.id].append(m.author.id)
            else:
                await self.bot.delete_message(m)
            return
        self.bot.kothcooldownnotovertolddict[m.guild.id] = []

        bot = False
        if words.startswith("[bot]"):
            bot = True
            words = words[5:]

        specialemoji = None
        if words.startswith("[") and words.count("]") != 0:
            words = words.split("]")
            specialemoji = words[0][1:].replace("<", "").replace(">", "").strip()
            errorspecialemoji = str(specialemoji)
            words = "]".join(words[1:])
            msg = await self.bot.send_message(self.bot.testserver.get_channel("329187094620667906"), "hi")
            try:
                await self.bot.add_reaction(msg, specialemoji)
            except:
                specialemoji = str(utility.get_emoji(self.bot, specialemoji)).replace("<", "").replace(">", "")
                try:
                    await self.bot.add_reaction(msg, specialemoji)
                except:
                    await talking.reply(context, "`{}` is not a valid emoji!".format(errorspecialemoji))
                    return
        if specialemoji != None:
            if "hippofrumplequest" in specialemoji:
                await talking.reply(context, "no")
                return
            if "obama" in specialemoji:
                await talking.reply(context, "no")
                return

        self.bot.kothcooldown = datetime.utcnow()

        if seconds < 15:
            await talking.reply(context, "Please wait, the cooldown's not over yet.")
            return

        seconds = (datetime.utcnow() - self.bot.kothcooldown).seconds

        u = self.bot.epicord.get_member(self.bot.koth[0])
        timestampmsg = await talking.say(context,
                                    u.mention + ": Quick! Fight off {} by saying something!\n{}: Say . if this was a mistake.".format(
                                        ccc.shownames(context.message.author), context.message.author.mention))
        statement = "doesn't defend the hill."
        if u.id != self.bot.me.id:
            def tempcheck(m):
                return m.author == u or (m.author == context.message.author and m.content == ".")

            reply = await self.bot.wait_for_message(timeout=15, author=None, channel=context.message.channel,
                                                    content=None, check=tempcheck)
            if reply != None and reply.author == context.message.author:
                await talking.reply(context, "Heh. Nice going, mate.")
                return
            statement = ""
            if reply == None:
                statement = "never defended the hill."
                # await mf.say(context,u.mention+", nice work. The hill is yours... for now.".format(mf.shownames(context.message.author)))
                # return
            else:
                seconds = (reply.timestamp - timestampmsg.timestamp).seconds
                if seconds <= 5:
                    await talking.say(context, u.mention + ", nice work. You've defended the hill with {} to spare.".format(
                        ccc.pluralstr("second", round(5 - seconds, 2))))
                    if context.message.author != u:
                        asyncio.ensure_future(mf.kothincreasecooldown(self.bot, m.guild.id))
                    return
                else:
                    statement = "attempted to defend the hill, but was late by {}.".format(
                        ccc.pluralstr("second", round(seconds - 5, 2)))

        self.bot.kothlast = copy.deepcopy(self.bot.koth)
        self.bot.kothcooldowndict[m.guild.id] = 15

        if self.bot.koth == "":
            self.bot.koth = [context.message.author.id, ccc.shownames(context.message.author), "king"]
            basics.save(bot,"koth")
        elif context.message.author.id == "238459957811478529" or context.message.author.id == "208304366719860737":
            await talking.reply(context, "FUCK OFF!!!")
        elif context.message.guild != self.bot.epicord and context.message.guild != self.bot.testserver:
            await talking.reply(context, "You can't overthrow the {} in secret.".format(self.bot.koth[2]))
        else:
            if context.message.content[2] == "k":
                type = "king"
            if context.message.content[2] == "q":
                type = "queen"
            if context.message.content[2] == "l":
                type = "loli"
            if context.message.content[2] == "f":
                type = "furry"
            if context.message.content[2] == "c":
                type = "cheese"
            # if context.message.content[2]=="h":
            #    type = "hippo"
            if len(words) > 0:
                type = words.strip()

            if specialemoji != None:
                if ":markedforpinning:" in specialemoji:
                    await talking.reply(context, "FUCK OFF!!!")
                    return

            # Save highscore stuff
            seconds = (datetime.utcnow() - self.bot.koth[4]).seconds
            seconds += (datetime.utcnow() - self.bot.koth[4]).days * 24 * 60 * 60
            add = [self.bot.koth[0], self.bot.koth[2], self.bot.koth[3], seconds, True]
            added = False
            rank = 0
            for x in range(0, len(self.bot.kothhigh)):
                if add[3] < self.bot.kothhigh[x][3]:
                    added = True
                    rank = x
                    self.bot.kothhigh.insert(x, add)
                    break
            if added == False:
                rank = len(self.bot.kothhigh)
                self.bot.kothhigh.append(add)
            basics.save(bot,"kothhigh")

            emoji = ""
            if seconds > (60 * 60) * 24:
                emoji = "<:tier4:348277627598929922>"
            elif seconds > (60 * 60) * 6:
                emoji = "<:tier3:348279546765901826>"
            elif seconds > (60 * 60) * 2:
                emoji = "<:tier2:348276583741521921>"
            elif seconds > 60 * 15:
                emoji = "<:tier1:348266722526101505>"
            minutes = 0
            while seconds >= 60:
                seconds -= 60
                minutes += 1
            hours = 0
            while minutes >= 60:
                minutes -= 60
                hours += 1
            minutes += round(seconds / 60, 2)
            highs = emoji + str(hours) + " hours and " + str(minutes) + " minutes"
            try:
                highs = "\n\n<@{}> lasted {}, ranking at #{}. They've earned {} pixels for a total of {}.".format(
                    self.bot.koth[0], highs, len(self.bot.kothhigh) - rank,
                    koth.pixelcalc(self.bot.koth[4], datetime.utcnow()),
                    mf.pixeledit(self.bot, self.bot.koth[0], mf.pixelcalc(self.bot.koth[4], datetime.utcnow())))
            except:
                pass

            previouskoth = list(self.bot.koth)
            if bot == False:
                await talking.reply(context,
                               "<@{}> {} As such, you've become {} of the hill, overthrowing the previous {}!".format(
                                   self.bot.koth[0], statement, type, self.bot.koth[2]) + highs)

                self.bot.koth = [context.message.author.id, ccc.shownames(context.message.author), type,
                                 specialemoji, datetime.utcnow()]
            else:
                await talking.reply(context,
                               "<@{}> {} As such, the bot has become {} of the hill, overthrowing the previous {}!".format(
                                   self.bot.koth[0], statement, type, self.bot.koth[2]) + highs)
                # await mf.reply(context,"The bot has become {} of the hill, overthrowing <@{}>, the previous {}!".format(type,self.bot.koth[0],self.bot.koth[2])+highs)
                self.bot.koth = [self.bot.me.id, ccc.shownames(context.message.guild.me), type, specialemoji,
                                 datetime.utcnow()]

            basics.save(bot,"koth")
            #await mf.ach_check(self.bot, await self.bot.get_user_info(previouskoth[0]), context.message.channel,
            #                   "kothloss", previouskoth)
        
def setup(bot):
    bot.add_cog(Time(bot))