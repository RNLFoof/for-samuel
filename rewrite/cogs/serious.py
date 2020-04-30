import asyncio
import json

import discord
from discord.ext import commands
from discord.ext.commands import Cog
from future.backports.datetime import timedelta

import modules.talking as talking
import modules.basics as basics
import modules.ccc as ccc
import datetime
import re

import modules.utility as utility
import modules.aesthetic as aesthetic

from classes.PageMessage import PageMessage
from classes.SortableChart import SortableChart


class Serious(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["con"])
    async def content(self, context):
        """Shows the raw content of a message given an ID.

        Adds zero-width spaces to make everything properly visible. Be aware."""

        q = basics.contentq(context.message.content)
        msg = await utility.referencemessage(context)
        if msg is None:
            return
        else:
            s = msg.content
            while "```" in s:
                s = s.replace("```", "``­`",1)
            if s=="":
                s="­"
            await talking.say(context, f"```{s}```")

    @commands.command(pass_context=True)
    async def jump(self, context):
        """Provides a link to a message, given a message reference.

        Modifiers:
        old|original|classic|legacy|pin : Pins a message for 30 seconds given an ID."""
        q=basics.contentq(context.message.content, split=False)

        q, pin, = basics.subcommands(context, q, ["old|original|classic|legacy|pin"])

        msg = await utility.referencemessage(context, s=q)
        if msg == None:
            return

        if pin==None:
            await talking.say(context,embed=discord.Embed(description=utility.portal(msg,"Jump to the message.")))
        else:
            # await talking.say(self.bot.testserver.get_channel("382641553803444224"),"ignore pinned message;{}".format(msg.id))
            await msg.pin()
            #await asyncio.sleep(5)
            async for pinannouncemsg in msg.channel.history(limit=15, reverse=False):
                if str(pinannouncemsg.type)=="MessageType.pins_add":
                    await pinannouncemsg.delete()
                    break
            await talking.reply(context,"The message with ID {} has been pinned in {} for the next 30 seconds.".format(msg.id,msg.channel.mention))
            await asyncio.sleep(30)
            await msg.unpin()

    @commands.command(pass_context=True, aliases=["userlist", "ml", "ul"])
    async def memberlist(self, context):
        """Lists the members of a server.

        Along with their online statuses, in order of importance."""
        types = ["high", "medium", "low", "none", "bot"]
        bot = self.bot
        m = context.message
        strings = ["­","­","­","­","­"]
        prihigh = utility.getcoolpeople(self.bot, context.message.guild, priority="high")
        primedium = utility.getcoolpeople(self.bot, context.message.guild, priority="medium")
        prilow = utility.getcoolpeople(self.bot, context.message.guild, priority="low")
        d = bot.priority_day["servers"][m.guild.id]

        valuelength = 1
        for x in d.values():
            if len(str(x)) > valuelength:
                valuelength = len(str(x))

        for m in sorted(context.message.guild.members, key=lambda x: d[x.id], reverse=True):
            statusn = ["online", "idle", "dnd", "offline"].index(str(m.status))
            addstr = f'`{str(d[m.id]).rjust(valuelength+1, " ")}` {["<:status_online:353069536880361472>", "<:status_idle:353074751947800576>","<:status_dnd:353069536884424714>", "<:status_offline:353069536884555776>"][statusn]} {basics.useremoji(self.bot, m)}{m.mention}\n'
            if m.bot:
                strings[4] += addstr
            elif m in prihigh:
                strings[0] += addstr
            elif m in primedium:
                strings[1] += addstr
            elif m in prilow:
                strings[2] += addstr
            else:
                strings[3] += addstr

        embeds = [discord.Embed(type="rich", title=f"{context.message.guild.name}'s Members")]

        def splitfields(title, content, embeds, total):
            embed = embeds[-1]
            add = ""
            total += len(title)
            for x in content.split("\n"):
                if len(x) + total >= 6000:
                    embed.add_field(name=title, value=add, inline=False)
                    print(total)
                    add = x + "\n"
                    title = "­"

                    embeds.append(discord.Embed(type="rich"))
                    embed = embeds[-1]
                    total = len(title+x)
                    continue
                total += len(x)+1
                if len(add + x) <= 1023:
                    add += x + "\n"
                else:
                    embed.add_field(name=title, value=add, inline=False)
                    add = x + "\n"
                    title = "­"
                    total += len(title)
            embed.add_field(name=title, value=add, inline=False)
            return embeds, total

        total = len(f"{context.message.guild.name}'s Members") # To avoid the 6000 limit
        embeds, total = splitfields("High Priority", strings[0], embeds, total)
        embeds, total = splitfields("Medium Priority", strings[1], embeds, total)
        embeds, total = splitfields("Low Priority", strings[2], embeds, total)
        embeds, total = splitfields("No Priority", strings[3], embeds, total)
        embeds, total = splitfields("Bots", strings[4], embeds, total)

        await talking.reply(context, embed=embeds[0])
        for embed in embeds[1:]:
            await talking.say(context, embed=embed)

    @commands.command(pass_context=True, aliases=["sms"])
    async def rawtext(self, context):
        """Loosely recreates Discord's formatting in raw text.

        The return text is in an inline code block, so unicode emojis are replaced with their actual unicode.
        Custom emojis are replaced with [ URL | NAME ].
        Bold, italics, bold+italics, underline, and strikeout are replaced with unicode characters of the same. They're mutually exclusive.
        Starting with /shrug, /tableflip, or /unflip will add the corresponding text to the end."""
        bot = self.bot
        q = basics.contentq(context.message.content,split=False)
        await talking.say(context,f"``{ccc.sms(bot, q).replace('``','`­`').replace('``','`­`')}``")

    @commands.command(pass_context=True,aliases=["si"])
    async def servericon(self, context):
        """Shows the server icon.

        The format defaults to .gif if the server icon is animated and .webp otherwise. You can pick .webp, .jpeg., .jpg, or .png as the format by saying them in your message."""
        m = context.message
        q = basics.contentq(m.content, split=False)
        guild = m.guild

        format = "gif" if guild.is_icon_animated() else "webp"
        for x in ["webp","jpeg","jpg","png"]:
            if x in q:
                format=x
                break

        url = guild.icon_url_as(format=format)
        await talking.reply(context,str(url))

    @commands.command(pass_context=True,hidden=True)
    async def chart(self, context):
        """WIP"""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)

        lol=[]
        for x in q.split("\n"):
            x = x.split(";")
            for n,y in enumerate(x):
                x[n] = y.strip()
            lol.append(x)

        base = len(lol[0])
        fuckstr = ""
        for x in lol[1:]:
            if len(x) != base:
                fuckstr+=f"\n{basics.spitback((';'.join(x)))}"
        if fuckstr:
            await talking.reply(context,"The following row(s) have the wrong number of columns."+fuckstr)
            return

        SortableChart(bot, validfor=timedelta(minutes=10), context=context, lol=lol)

    @commands.command(pass_context=True, aliases=["restore","restoreembed","restoreemb","restorelink","recover","recoverembed","recoveremb","recoverlink","reembed","reemb","relink","desuppress","desuppressemb","desuppresslink","des","desembed","desemb","deslink","dse"])
    async def desuppressembed(self, context):
        """Brings back closed embeda from a referenced message."""
        m = await utility.referencemessage(context)
        if m == None:
            return

        await m.edit(flags=3)
        await talking.reply(context, "Okay, I've desupprbbbbessed any embeds in that message.", reaction=True)

    @commands.command(pass_context=True, aliases=["compact","comp","compress","crushfetish"])
    async def condense(self, context):
        """WIP"""
        m = context.message
        q = basics.contentq(m.content, split=False)
        q, all = basics.subcommands(context, q, [r"list|all"])

        d = json.load(open("json/compact.json", encoding="utf8"))
        l = []
        for x in d.items():
            l.append(x)

        l = sorted(l, key=lambda x: x[0])
        l = sorted(l, key=lambda x: len(x[0]))[::-1]

        if all is not None:
            s = "This is a list of all replacements. Let me know if I missed anything good."
            for x in l:
                s += f"`{x[0]}` **➜** {x[1]}\n"
            await talking.reply(context, s, split=True)
            return

        new = q

        for x in l:
            new = new.replace(x[0], x[1])
        for x in l:
            print(x)
            new = re.sub(re.escape(x[0]), x[1], new, flags=re.IGNORECASE)

        if len(q) == len(new):
            await talking.reply(context, "Wasn't able to remove any characters.")
        else:
            await talking.reply(context, f"Removed {len(q)-len(new)} characters, going from {len(q)} to {len(new)}.\n{basics.spitback(new)}")

def setup(bot):
    bot.add_cog(Serious(bot))