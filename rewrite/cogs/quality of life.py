import datetime
import re

import discord
from discord.ext import commands
from discord.ext.commands import Cog

import modules.talking as talking
import modules.basics as basics
import random
import asyncio

from classes.AchievementBrowser import AchievementBrowser
from classes.ConfirmMessage import ConfirmMessage
from classes.FlockOfInvites import FlockOfInvites
from classes.SortableChart import SortableChart
from modules import utility, aesthetic


class Quality_Of_Life(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True,aliases=["change"])
    async def edit(self, context):
        """Shortcut to editing stuff.

        WIP
        
        Start with # to edit the channel name.
        Start with T to edit the topic.
        Start with ^ to edit your hoisted role."""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)

        if len(q) == 0:
            await talking.reply(context,"I need a character to indicate what to do with your message. See `s!help edit` for more details.")
            return

        credit="."
        action, q = q[0], q[1:].strip()



        if action == "#":
            q = q.replace(" ","-")

            # Icons
            icon = re.match(r"[^\x00-\x7F]-?", q)
            if icon is None:
                icon = re.match(r"[^\x00-\x7F]-?", m.channel.name)
            else:
                q = q.replace(icon.group(0),"",1)
            if icon is None:
                icon = ""
            else:
                icon = icon.group(0)
            q = icon + q

            perm = "manage_channels"
            permdesc = f"edit {m.channel.mention}"
            operation = m.channel.edit(name=q, reason=f"Requested through an s!edit by {context.message.author.name}.")
            finish = f"Okay, I've renamed `#{m.channel.name}` to {m.channel.mention} for you"

        elif action == "T":
            if len(q)>100:
                await talking.reply(context,"Channel topics cannot go over 100 characters. You're at {}.".format(len(q)))
                return
            perm = "manage_channels"
            permdesc = f"edit {m.channel.mention}"
            operation = m.channel.edit(topic=q, reason=f"Requested through an s!edit by {context.message.author.name}.")
            finish = f"Okay, I've changed the topic of {m.channel.mention} for you"

        elif action == "^":
            title = utility.get_title_role(context.message.author)
            if title is None:
                await talking.reply(context,"You don't have a hoisted role.")
                return
            perm = "manage_roles"
            permdesc = f"edit roles"
            operation = title.edit(name=q, reason=f"Requested through an s!edit by {context.message.author.name}.")
            finish = f"Okay, I've renamed `@{title.name}` to @{q} for you"

        else:
            await talking.reply(context,"I don't have an action associated to that starting character. See `s!help edit` for more details.")
            return



        allowed = True
        if not getattr(m.author.permissions_in(m.channel), perm):
            allowed = False
            msg = await talking.reply(context,f"You don't have permission to {permdesc}. However, if someone who does clicks <:bn_do:328724374498836500>, the change will go through.")
            await msg.add_reaction(":bn_do:328724374498836500")

            def check(reaction, user):
                return reaction.emoji.name.replace("bn_", "") in self.bot.buttons and\
                    reaction.message.id == msg.id and\
                    getattr(user.permissions_in(m.channel), perm) and\
                    user.id != bot.me.id

            try:
                rea = await self.bot.wait_for("reaction_add", check=check, timeout=300)
            except asyncio.TimeoutError:
                pass
            else:
                allowed = True
                credit = ", thanks to {}.".format(rea[1].mention)

            asyncio.ensure_future( utility.safelyclear(bot, msg, [["328724374498836500"]]) )



        if allowed:
            try:
                await operation
            except Exception as e:
                await talking.reply(context, f"Sorry, I wasn't able to make that change for some reason. Details below.\n```{e}```")
            else:
                await talking.reply(context, finish + credit)

    @commands.command(pass_context=True, aliases=["getmember","gu"])
    async def getuser(self, context):
        """Mentions a mentioned user in an embed.

        This is intended for use in conjunction with a silent mention so that you don't need to find people in the member list. When somebody is mentioned in an embed, they aren't pinged, but the mention is still clickable."""
        if len(context.message.mentions)==0:
            await talking.reply(context,"Please silently mention someone! Or mention them normally if you want to be super redundant.")
        else:
            embed=discord.Embed(description=basics.useremoji(self.bot, context.message.mentions[0], guild=context.message.guild)+context.message.mentions[0].mention)
            await talking.say(context,"",embed=embed,nowebhook=True)

    @commands.command(pass_context=True, aliases=["foi","foil"])
    async def flockofinvites(self, context):
        """Gets invites based on your input.

        Gets invites to all servers in which you and the bot have the ability to get invites, and your input is somewhere in the server name.
        Lists off all the matched servers before posting them so that you don't accidentally invite to somewhere you wanted private.
        The invites last ten minutes.

        Modifiers:
        regex : Searches with regex instead."""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)
        q, regex = basics.subcommands(context, q, ["regex"])

        if not regex:
            q = re.escape(q)

        try:
            q = re.compile(q)
        except:
            await talking.reply(context,"That's not valid regex, ya dingus. This might help: <https://regexr.com/>")
        else:
            sl = []
            for s in bot.guilds:
                for u in s.members:
                    if u.id == context.author.id:
                        break
                else:
                    continue

                if (u.guild_permissions.administrator or u.guild_permissions.create_instant_invite) and (
                    s.me.guild_permissions.administrator or s.me.guild_permissions.create_instant_invite) and \
                    re.search(q, s.name):
                        sl.append(s)

            sl.sort(key=lambda x: x.name)
            # sls = []
            # for s in sl:
            #     sls.append(s.name)
            FlockOfInvites(bot, validfor=datetime.timedelta(minutes=5), messagecount=1, userids=[m.author.id], sl=sl, context=context)

    @commands.command(pass_context=True, aliases=["poann", "pointoutanevernick","poaen","pollen","polen","quote"])
    async def pointoutanickname(self, context):
        """Points out the nickname that a referenced message was posted under.

        Posts in all caps by default. Both modifiers remove this.

        Modifiers:
        quote|q : Changes the format to one additionally pointing out the content of the referenced message.
        ANYTHING : Changes the format to whatever was entered. The nickname is inserted at -s. If no -s are included, one is added to the end of your input.

        Rigged Aliases:
        quote : Uses the quote formatting.

        Meta:
        Use > as a modifier in order to use the default format without caps. It seemed more intuitive to have you trigger the ANYTHING this way than to have a seprate modifier."""
        bot = self.bot
        m = context.message
        q = basics.contentq(m.content, split=False)
        q, quote, custom = basics.subcommands(context, q, ["quote|q",".*?"],
            riggedaliases=[
               {
                   "regex": r"quote",
                   "slot": 0,
                   "value": "quote"
               }])

        msg = await utility.referencemessage(context, s=q)
        if msg == None:
            return

        upper = False
        if quote is not None:
            post = f'"{msg.content}"\- -'
        elif custom is not None:
            post = custom.group(1)
            if re.search(r"(?<!\\)-", post) is None:
                while post.endswith("\\"):
                    post = post[:-1]
                post += "-"
        else:
            upper = True
            post = ">-"

        try:
            if upper:
                await talking.say(context, re.sub(r"(?<!\\)-" , bot.thennicks[msg.channel.id][msg.id], post).upper())
            else:
                await talking.say(context, re.sub(r"(?<!\\)-" , bot.thennicks[msg.channel.id][msg.id], post))
        except:
            await talking.reply(context, "I don't have a nickname associated with that message.")
        await AchievementBrowser.ach_check(bot, msg.author, m.channel, "polen",[])

    @commands.command(pass_context=True, aliases=["cycle", "comic", "ccomic", "cyclec", "csection","cc"])
    async def cyclecomic(self, context):
        """Cycle comic manager.

        Cyclecomics being comics where, repeatedly, one person adds two panels, and then shows only the newest panel to another person. Then they add two panels and pass on only the last panel, and so on.

        Modifiers:
        new|create|add : Create a new cyclecomic.
        join|enter : Add yourself to a previously created cyclecomic.
        upload|panel|append : Add a panel to a cyclecomic on which it's your turn.
        pass|give : Make it somebody else's turn on a cycleomic on which it's your turn.
        view|show|release|spew|display : Display a completed cyclecomic.
        """
        async def SAVETODICT_give(self):
            await talking.say(self.context, f"Hey loser. You've been passed this panel ||{self.url} || by {basics.truename(self.bot,context.message.author)} as part of {q}.", channel=self.passonto)
            self.bot.cyclecomics[self.q]["turn"] = self.passonto.id
            basics.save(self.bot, "cyclecomics")
            self.message = "Okay, done."

        async def SAVETODICT_upload(self):
            self.bot.cyclecomics[q]["panelurls"].append(self.image)
            self.bot.cyclecomics[q]["panelcreators"].append(self.context.message.author.id)
            basics.save(bot, "cyclecomics")
            await talking.reply(context, f"Okay, {self.image} has been added. I'm saving the URL, not the actual image. I'm also not your mom(unless you want me to be <:blob_wink:423672830316511232>), so I'm not adding a failsafe if you delete the message and thus an attached image. It'll just not show up and you'll lose all your friends.")

        async def SAVETODICT_view(self):
            for n,x in enumerate(self.bot.cyclecomics[self.q]["panelurls"]):
                await talking.say(self.context,f"Panel {n+1}, by <@{self.bot.cyclecomics[self.q]['panelcreators'][n]}>.\n{x}")
                await asyncio.sleep(30)

        bot = self.bot
        m = context.message
        q = basics.contentq(m.content,split=False)

        q, new, join, upload, give, view = basics.subcommands(context,q,[r"new|create|add",r"join|enter",r"upload|panel|append",r"pass|give",r"view|show|release|spew|display"])

        refnum = " ".join(q.split(" ")[1:])
        q = q.split(" ")[0]
        qcaps = q
        q = q.lower()

        current = bot.cyclecomics

        if new is not None:
            for k,i in current.items():
                if i["owner"] == m.author.id != bot.rnl.id:
                    await talking.reply(context, "You can only create one cyclecomic at a time per server to prevent spam.")
                    return
            if not q:
                await talking.reply(context,'Add a nickname to this comic, so that it can be identified by something besides an autogenerated number. Like, I dunno. "penis" or "Chris" or something. Six characters max, limited to numbers, letters, and underscores.')
            elif not re.match(r"^\w{1,6}$",q):
                await talking.reply(context,'Six characters max, limited to numbers, letters, and underscores.')
            else:
                if q in current:
                    await talking.reply(context, f"{basics.spitback(qcaps)} is taken already!")
                else:
                    current[q] = {
                                    "owner": m.author.id,
                                    "turn": m.author.id,
                                    "creationtime": str(datetime.datetime.utcnow().date()),
                                    "panelurls": [],
                                    "panelcreators": [],
                                    "users": [m.author.id],
                                    "qcaps": qcaps,
                                    "server": m.guild.id
                                 }
                    await talking.reply(context, f"Okay, {basics.spitback(qcaps)} is now added. People can join using `s!cc [join]{current[q]['qcaps']}`")
                    basics.save(bot,"cyclecomics")
        elif join is not None:
            if not q:
                await talking.reply(context, "You need to specify which cyclecomic you want to join!")
            elif q not in current:
                await talking.reply(context, f"{basics.spitback(qcaps)} doesn't seem to exist.")
            elif m.author.id in current[q]["users"]:
                await talking.reply(context, "You're already in this cyclecomic!")
            else:
                current[q]["users"].append(m.author.id)
                basics.save(bot, "cyclecomics")
                await talking.reply(context, "Coolio, you've been added to this cyclecomic.")
        elif upload is not None:
            if not q:
                await talking.reply(context, "You need to specify which cyclecomic you want to add a panel to!")
            elif q not in current:
                await talking.reply(context, f"{basics.spitback(qcaps)} doesn't seem to exist.")
            elif m.author.id not in current[q]["users"]:
                await talking.reply(context, f"You aren't a member of this cyclecomic. You can join with `s!cc [join]{current[q]['qcaps']}`.")
            elif current[q]["turn"] != m.author.id:
                await talking.reply(context, f"It's not your turn on this cyclecomic.")
            else:
                image = await utility.referenceimage(context,returnurl=True)
                if image:
                    ConfirmMessage(bot, validfor=datetime.timedelta(minutes=5),
                                   message=f"Are you sure you want to add ||{image} || to {q}?", image=image, q=q
                                   , yesscript=SAVETODICT_upload, context=context)
        elif give is not None:
            if not q:
                await talking.reply(context, "You need to specify which cyclecomic you want to pass off on!")
            elif q not in current:
                await talking.reply(context, f"{basics.spitback(qcaps)} doesn't seem to exist.")
            elif m.author.id not in current[q]["users"]:
                await talking.reply(context, f"You aren't a member of this cyclecomic. You can join with `s!cc [join]{current[q]['qcaps']}`.")
            elif current[q]["turn"] != m.author.id:
                await talking.reply(context, f"It's not your turn on this cyclecomic.")
            else:
                try:
                    server = bot.get_guild(current[q]['server'])
                    u = utility.get_member_or_user(bot, server, current[q]['users'][int(refnum)])
                except:
                    await talking.reply(context, f"I couldn't figure out who {basics.spitback(refnum)} referred to. Use s!cc {current[q]['qcaps']} and give me the reference number of the peron you want to pass to.")
                else:
                    if u.id ==  m.author.id:
                        await talking.reply(context,f"*You're* {basics.truename(bot,u)}, dummy!")
                    else:
                        if current[q]['panelurls']:
                            url = current[q]['panelurls'][-1]
                        else:
                            url = "I lied. I decieved you. Nothing has been added to this cyclecomic yet."
                        ConfirmMessage(bot, validfor=datetime.timedelta(minutes=5), message=f"Are you sure you want to pass ||{url} || to {basics.truename(bot,u)}?", passonto=u, url=url, q=q
                                       , yesscript=SAVETODICT_give, context=context)
        elif view is not None:
            if not q:
                await talking.reply(context, "You need to specify which cyclecomic you want to show!")
            elif q not in current:
                await talking.reply(context, f"{basics.spitback(qcaps)} doesn't seem to exist.")
            elif m.author.id != current[q]["owner"]:
                await talking.reply(context, f"You don't own this cyclecomic, so you can't set it off.")
            else:
                ConfirmMessage(bot, validfor=datetime.timedelta(minutes=5), message=f"Are you sure you want to display the entirety of {q}? You can't turn back. It'll be EVERYWHERE.", q=q
                                       , yesscript=SAVETODICT_view, context=context)
        else:
            if not q:
                s="Here's a list of cyclecomics in this server. Specify one to get more info on it.\n`"
                for x in current.keys():
                    s+=f"\n{x}"
                s+="`"
                await talking.reply(context, s)
            elif q not in current:
                await talking.reply(context, f"{basics.spitback(qcaps)} isn't a cyclecomic on this server.")
            else:
                lol=[["User","Turn","Owner","Panels","Ref. #","Status"]]
                for n,x in enumerate(current[q]["users"]):
                    u = utility.get_member_or_user(bot, m.guild, x)
                    lol.append([
                        basics.truename(bot,u),
                        u.id==current[q]["turn"],
                        u.id==current[q]["owner"],
                        current[q]["panelcreators"].count(u.id),
                        n,
                        aesthetic.statusemoji(bot,u)])
                SortableChart(bot, validfor=datetime.timedelta(minutes=5), context=context, lol=lol, initialsort=[1, 0])

    @commands.command(pass_context=True,aliases=["pt"])
    async def pinthat(self, context):
        """Pins a message containing what you wrote."""
        q=basics.contentq(context.message.content,split=False)
        bot=self.bot
        m = context.message

        bot.dontpinthat.append(context.message.id)

        pinmsg = await utility.referencemessage(context)
        if pinmsg == None:
            return

        if pinmsg.id in bot.dontpinthat:
            msg = await talking.reply(context,"EAT A DICK")
            bot.dontpinthat.append(msg.id)
        else:
            try:
                await pinmsg.pin()
            except:
                await talking.reply(context, "Unable to pin. Maybe there's no more room for pins?")
            else:
                await AchievementBrowser.ach_check(bot, pinmsg.author, m.channel, "pin",
                                                   [pinmsg, m])  # Getting your message pinned
                await AchievementBrowser.ach_check(bot, m.author, pinmsg.channel, "pinner",
                                                   [pinmsg, m])  # Pinning someone else's message

def setup(bot):
    bot.add_cog(Quality_Of_Life(bot))