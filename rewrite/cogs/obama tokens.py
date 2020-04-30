import re

import discord
import random
from discord.ext import commands
from datetime import datetime, timedelta

from discord.ext.commands import Cog

import modules.ccc as ccc
import modules.talking as talking
import modules.basics as basics
from classes.AchievementBrowser import AchievementBrowser
from classes.ConfirmMessage import ConfirmMessage
from classes.SortableChart import SortableChart
from modules import ot, utility, ch
from modules.aesthetic import chart


class Obama_Tokens(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["dailies"])
    async def daily(self, context):
        """Opt in or out of free tokens for people you like.

        Once a day, after a random message, you'll be shown three random people and be offered to give a token to one of them.
        Use [list] to see which people have opted in and if they've gotten their token today.
        Use [dm] to toggle getting informed that you recieved a token in DMs rather than the same channel."""
        if context.message.guild.id not in self.bot.sdailylast.keys():
            self.bot.sdailylast[context.message.guild.id] = {}
            basics.save(self.bot, "sdailylast")

        bot=self.bot
        q = basics.contentq(context.message.content, split=False)
        if "[dm]" in q:
            bot = self.bot
            u = context.message.author

            if u.id in bot.dmdaily:
                bot.dmdaily.remove(u.id)
                await talking.reply(context, "You'll now be informed about getting a daily in the same channel.")
            else:
                bot.dmdaily.append(u.id)
                await talking.reply(context, "You'll now be informed about getting a daily in a DM.")
            basics.save(bot, "dmdaily")
            return
        if "[list]" in q:
            lol=[["User","Last","Today"]]
            for k, i in self.bot.sdailylast[context.message.guild.id].items():
                try:
                    m = utility.get_member_or_user(bot,context.message.guild,int(k))
                    if m is not None:
                        lol.append([basics.truename(bot,m), i.replace("DEFAULT",""), i == str(datetime.utcnow().date())])
                except ValueError:
                    pass
            SortableChart(bot, validfor=timedelta(minutes=10), context=context, lol=lol, initialsort=[0,1], defaultreverse={1})
            return

        id = str(context.message.author.id)
        if id not in self.bot.sdailylast[context.message.guild.id].keys():
            if id + "DISABLED" in self.bot.sdailylast[context.message.guild.id].keys():
                self.bot.sdailylast[context.message.guild.id][id] = \
                self.bot.sdailylast[context.message.guild.id][id + "DISABLED"]
                del self.bot.sdailylast[context.message.guild.id][id + "DISABLED"]
            else:
                self.bot.sdailylast[context.message.guild.id][id] = "DEFAULT"
            basics.save(self.bot, "sdailylast")
            await talking.reply(context,
                           "You will now be offered once a day after a random message three potential people to give a token to. Use this command again to turn it off.",
                           reaction=True)
            return
        else:
            self.bot.sdailylast[context.message.guild.id][id + "DISABLED"] = self.bot.sdailylast[context.message.guild.id][id]
            del self.bot.sdailylast[context.message.guild.id][id]
            basics.save(self.bot, "sdailylast")
            await talking.reply(context,
                           "You've opted back out of dailies. Use this command again to pick up where you left off.")
            return

    @commands.command(pass_context=True, aliases=["obama", "tokens", "ot", "obamatoken","yomama"])
    async def obamatokens(self, context):
        """Shows how many Obama Tokens you have. Mention somebody to check how much they have instead.

        Use [all] to see how many everyone has and their maxes, sorted by their maxes. Use [now] to sort by how many they have instead. Use [visual] to see it in emojis."""
        q = basics.contentq(context.message.content)
        bot = self.bot

        ot.otedit(self.bot, context.message.author, 0, False, channel=context.message.channel)
        if "[all]" in " ".join(q) or "[now]" in " ".join(q) or "[top]" in " ".join(q) or "[max]" in " ".join(q):
            l = [["User", "Max", "Now", "Given", "Me","Mentioned"]]
            for k in self.bot.obamatokens[context.message.guild.id].keys():
                k = context.message.guild.get_member(k)
                if k is None:
                    continue
                ot.otedit(self.bot, k, 0, False, channel=context.message.channel)
                if k != None:
                    l.append([basics.truename(bot, k),
                              float(self.bot.obamatokensmax[context.message.guild.id][k.id]),
                              float(self.bot.obamatokens[context.message.guild.id][k.id]),
                              float(self.bot.obamatokensgiven[context.message.guild.id][k.id]),
                              k.id == context.message.author.id,
                              k in context.message.mentions])


            # charlst = [["User", "Max", "Now", "Given", "Me","Mentioned"]]
            # for n, x in enumerate(l):
            #     max = str(x[0])
            #     if "." not in max:
            #         max += "."
            #     while list(max).index(".") > len(max) - 3:
            #         max += "0"
            #
            #     now = str(x[2])
            #     if "." not in now:
            #         now += "."
            #     while list(now).index(".") > len(now) - 3:
            #         now += "0"
            #     charlst.append([x[1], max, now, x[3], x[4], x[5]])

            SortableChart(bot, validfor=timedelta(minutes=5), context=context, lol=l, initialsort=[5,1,4,2,3,6], addnumbers=True, resetnumbers={2,3,4}, defaultreverse={2,3,4,5,6})

            return
        target = context.message.author
        if len(context.message.mentions) > 0:
            target = context.message.mentions[0]
            ot.otedit(self.bot, target, 0, False, channel=context.message.channel)
        if "[visual]" in " ".join(q):
            if target == context.message.author:
                targetstr = "Your"
            else:
                targetstr = "{}'s".format(shownames(target))
            await talking.saysplit(self, "{} current Obama Tokens:\n{}\n\n{} all-time Obama Tokens:\n{}".format(targetstr,
                                                                                                           ot.visualtokens(
                                                                                                               self.bot.obamatokens[
                                                                                                                   target.id] / 0.04),
                                                                                                           targetstr,
                                                                                                                ot.visualtokens(
                                                                                                               self.bot.obamatokensmax[
                                                                                                                   target.id] / 0.04)),
                              [">"])
        else:
            if target == context.message.author:
                targetstr = "You currently have"
                targetstr2 = "Your"
            else:
                targetstr = "{} currently has".format(mf.shownames(target))
                targetstr2 = "Their".format(mf.shownames(target))
            await talking.reply(context,
                           "{} {} Obama Tokens, {} of which were given. {} all-time count is {}.".format(targetstr,
                                                                                                         self.bot.obamatokens[target.guild.id][
                                                                                                             target.id],
                                                                                                         self.bot.obamatokensgiven[target.guild.id][
                                                                                                             target.id],
                                                                                                         targetstr2,
                                                                                                         self.bot.obamatokensmax[target.guild.id][
                                                                                                             target.id]))

    @commands.command(pass_context=True, aliases=["pay"])
    async def give(self, context):
        """Gives x Obama Tokens to the mentioned user."""
        async def SAVETODICT_give(self):
            bot=self.bot
            gifter=self.gifter
            giftee=self.giftee
            value=self.cost

            giftertokens = ot.otedit(self.bot, gifter, 0, False, channel=context.message.channel)
            gifteetokens = ot.otedit(self.bot, giftee, 0, False, channel=context.message.channel)

            ot.otedit(self.bot, gifter, -value, False, channel=context.message.channel)
            ot.otedit(self.bot, giftee, value, False, channel=context.message.channel)

            self.message = "You've given `{}` Obama Token{} to {}.\n\n{}'s Tokens:\n{} ➔ {}\n\n{}'s Tokens:\n{} ➔ {}".format(
                value,
                ["", "s"][value != 1],
                basics.truename(bot, giftee),
                basics.truename(bot, gifter),
                giftertokens,
                round(giftertokens - value, 2),
                basics.truename(bot, giftee),
                gifteetokens,
                round(gifteetokens + value, 2))
            await AchievementBrowser.ach_check(bot, gifter, self.context.message.channel, "give", {"giftee":giftee,"value":value})


        ammount = basics.contentq(context.message.content)
        bot=self.bot
        value = re.sub("[^0-9\.]", "", re.sub("<@!?[0-9]{18}>", "", " ".join(ammount)))
        gifter = context.message.author
        giftertokens = ot.otedit(self.bot, gifter, 0, True, channel=context.message.channel)

        if len(value) == 0:
            await talking.reply(context, "Please give a value!")
            return
        value = round(float(value), 2)
        if len(context.message.mentions) == 0:
            await talking.reply(context, "Please mention someone!")
            return
        if context.message.mentions[0] == gifter:
            await talking.reply(context, "You can't give Obama Tokens to yourself!")
            return

        giftee = context.message.mentions[0]
        gifteetokens = ot.otedit(self.bot, giftee, 0, True, channel=context.message.channel)
        message = "Are you sure you want to give `{}` Obama Token{} to {}?\n\n{}'s Tokens:\n{} ➔ {}\n\n{}'s Tokens:\n{} ➔ {}".format(
                                 value,
                                 ["", "s"][value != 1],
                                 basics.truename(bot,giftee),
                                 basics.truename(bot,gifter),
                                giftertokens,
                                 round(giftertokens - value, 2),
                                 basics.truename(bot,giftee),
                                 gifteetokens,
                                 round(gifteetokens + value, 2)
                             )

        ConfirmMessage(bot, validfor=timedelta(minutes=5),
                       message=message, gifter=gifter,
                       giftee=giftee, cost=value
                       , yesscript=SAVETODICT_give, context=context)

    @commands.command(pass_context=True, aliases=["residue", "res", "rez", "or"])
    async def obamaresidue(self, context):
        """Shows how much Obama Residue you have. Mention somebody to check how much they have instead.

        Modifiers:
        all|max|now|top|list : Displays a chart of server-wide residue counts."""
        q = basics.contentq(context.message.content, split=False)
        q, max = basics.subcommands(context, q, [r"all|max|now|top|list"])
        bot = self.bot

        ot.otedit(self.bot, context.message.author, 0, False, channel=context.message.channel)
        if max is not None:
            l = [["User", "Max", "Now", "Me","Mentioned"]]
            for k in self.bot.obamaresidue[context.message.guild.id].keys():
                k = context.message.guild.get_member(k)
                if k is None:
                    continue
                ot.otedit(self.bot, k, 0, False, channel=context.message.channel)
                if k != None:
                    l.append([basics.truename(bot, k),
                              round(self.bot.obamaresiduemax[context.message.guild.id][k.id]/1000, 3),
                              round(self.bot.obamaresidue[context.message.guild.id][k.id]/1000, 3),
                              k.id == context.message.author.id,
                              k in context.message.mentions])


            SortableChart(bot, lol=l, validfor=timedelta(minutes=5), context=context, initialsort=[4,1,2,3,5], addnumbers=True, resetnumbers={2,3}, defaultreverse={2,3,4,5})

            return
        target = context.message.author
        if len(context.message.mentions) > 0:
            target = context.message.mentions[0]
            ot.otedit(self.bot, target, 0, False, channel=context.message.channel)

        if target == context.message.author:
            targetstr = "You currently have"
            targetstr2 = "Your"
        else:
            targetstr = "{} currently has".format(ccc.shownames(bot, target))
            targetstr2 = "Their"
        await talking.reply(context,
                       "{} {} Obama Residue. {} all-time count is {}.".format(targetstr,
                                                                              round(self.bot.obamaresidue[target.guild.id][
                                                                                                         target.id]/1000, 3),
                                                                                                     targetstr2,
                                                                                                     round(self.bot.obamaresiduemax[target.guild.id][
                                                                                                         target.id]/1000, 3)))
    @commands.command(pass_context=True, aliases=["eatmyass"], hidden=True)
    async def chnew(self, context):
        """WIP"""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)

        try:
            clothing, slots = ch.determineclothing(bot, m.author.id, q)
        except Exception as e:
            await talking.reply(context, f"{e.args[1]}")
        else:
            clothing = ch.editclothingperhippo(clothing, slots, hippos=['hippo','hippowink'])
            layers, needed = ch.determinelayers(clothing)
            images = ch.imagesfromlayers(layers)
            for x in ch.combineimages(layers, needed).values():
                await talking.reply(context, PIL=x)

def setup(bot):
    bot.add_cog(Obama_Tokens(bot))