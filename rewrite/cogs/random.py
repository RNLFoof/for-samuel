import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Cog

import modules.talking as talking
import modules.basics as basics
import modules.ccc as ccc
import random
from PIL import Image
from PIL import ImageDraw

from classes.Choose import Choose
from classes.Dice import Dice


class Random(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=["8choose","choice","8choice"])
    async def choose(self, context):
        """Chooses randomly from a set.

        Choices are separated by semicolons.

        Modifiers:
        NUMBER : Changes the weight of the entry. Default weight is 1.
        + : The entry will always be picked.
        - : The entry will never be picked.
        t : The entry will instead set a title.
        These are all applied to an individual entries, and are mutually exclusive."""
        bot = self.bot
        Choose(bot, validfor=datetime.timedelta(minutes=5), messagecount=1, q=basics.contentq(context.message.content,split=False),
                 context=context)

    @commands.command(aliases=["8dice"])
    async def dice(self, context):
        """Rolls dice.

        Defaults to two d6s.

        Modifiers:
        equaloutcome|eo : Every dice combination will only happen once before all possibilities are exhausted. """
        bot = self.bot
        Dice(bot, validfor=datetime.timedelta(minutes=5), messagecount=1, q=basics.contentq(context.message.content,split=False),
                 context=context)

    @commands.command(pass_context=True)
    async def roll(self, context):
        """Picks a random number. Marks dubs.

        Generates a meter that shows how close it was to the maximum. The meter will be yellow if you got dubs, green if you were one off, aqua if you were two off, or blue if you were further. Pink replaces anything but yellow if you got the minimum or maximum.
        Start with [unclear] to get emoji responces and/or [float] to get a float. Goes from 0 to 100 by default. Give it one number to roll 0 to that number. Give it two and it will go between those two."""
        q = mf.contentq(context.message.content)
        high = 100
        low = 0
        cm = False
        fl = False
        highroll = False

        for x in range(0, 5):

            q = " ".join(q)
            if q.startswith("[unclear]"):
                q = q[9:]
                cm = True
            q = q.split(" ")

            q = " ".join(q)
            if q.startswith("[float]"):
                q = q[7:]
                fl = True
            q = q.split(" ")

        if len(q) >= 1:
            if len(q[0]) > 0:
                if q[0].replace('.', '', 1).isdigit():
                    high = float(q[0])
        if len(q) >= 2:
            if q[0].replace('.', '', 1).isdigit() and q[1].replace('.', '', 1).isdigit():
                low = float(q[1])
                high = float(q[0])
                if high < low:
                    high, low = low, high

        if fl == True:
            roll = low + ((high - low) * random.random())
        else:
            low = math.floor(low)
            high = math.floor(high)
            roll = random.randint(low, high)

        if high - low > 500000:
            highroll = True

        if highroll == False:
            dubs = []
            for x in range(low, high + 1):
                if len(str(x)) >= 2:
                    if len(str(x).replace(str(x)[0], "")) == 0:
                        dubs.append(x)
        else:
            dubs = False
            if len(str(roll)) > 2:
                dubs = True
                match = str(roll)[0]
                for x in list(str(roll))[1:]:
                    if x != match:
                        dubs = False
            # dubs=False
            # if len(str(roll))==2:
            #    if str(roll)[0]==str(roll)[1]:
            #       dubs=True

        if cm == True:
            if roll == 0:
                roll = random.choice(
                    "<:OWOBIG1:277871791635038211>,<:xat_rolling_frame01:275178298273693696>".split(","))
            elif roll == 1:
                roll = random.choice("<:01:231608404630700035>,<:upstinky:290198083554508801>".split(","))
            elif roll == 2:
                roll = random.choice("<:02:231608413547790346>".split(","))
            elif roll == 3:
                roll = random.choice("<:03:231608424662564864>,<:3_:279154839064281098>".split(","))
            elif roll == 4:
                roll = random.choice("<:04:231608431432171541>".split(","))
            elif roll == 5:
                roll = random.choice("<:05:231608440047403018>".split(","))
            elif roll == 6:
                roll = random.choice("<:06:231608856176754689>".split(","))
            elif roll == 7:
                roll = random.choice("<:07:231608868130521088>".split(","))
            elif roll == 8:
                roll = random.choice("<:08:231608877207126018>".split(","))
            elif roll == 9:
                roll = random.choice("<:09:231608885666906122>".split(","))
            elif roll == 69:
                roll = random.choice("<:69:279159715576152064>".split(","))
            elif roll == 100:
                roll = random.choice("<:100think:323237131151605772>".split(","))
            elif roll == 1000:
                roll = random.choice("<:collection_of_1000_up_stinkies:309183888163471361>".split(","))

        if highroll == True:
            await mf.reply(context, "Between {} and {}, I rolled: {}{}{}".format(low, high, ["", "**"][dubs], roll,
                                                                                 ["!", "**! 🌟"][dubs]))
            return
        # Meter
        col = None
        for d in dubs:
            if roll == d:
                col = "yellow"
            if roll == d - 1 or roll == d + 1:
                col = "green"
            if roll == d - 2 or roll == d + 2:
                col = "aqua"
        if col == None:
            col = "blue"
        if (roll == high or roll == low) and col != "yellow":
            col = "pink"
        bar = Image.open(mf.slashes("Images|Meters|{}.png".format(col)), 'r')
        back = Image.open(mf.slashes("Images|Meters|{}back.png".format(col)), 'r')
        edges = Image.open(mf.slashes("Images|Meters|edges.png"), 'r')
        canvas = Image.new('RGBA', bar.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype("arial.ttf", 14, 0)

        draw = ImageDraw.Draw(canvas)

        canvas = Image.alpha_composite(canvas, bar)
        spacing = ((roll - low) / (high - low) * (1600 - 6)) + 3
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([spacing, 0, 1600, 120], fill="red", outline="red")
        draw.line([spacing, 0, spacing, 120], fill="black", width=7)
        canvas = Image.alpha_composite(canvas, edges)

        # Get rid of red
        pixdata = canvas.load()
        width, height = canvas.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 0, 0, 255):
                    pixdata[x, y] = (0, 0, 0, 0)

        canvas = Image.alpha_composite(back, canvas)
        # Adding arrows
        newcanvas = Image.new('RGBA', (bar.size[0] + 30, bar.size[1] + 30), (255, 255, 255, 0))
        newcanvas.paste(canvas, (15, 30))
        arrow = Image.open(mf.slashes("Images|Meters|dubsarrow.png"), 'r')
        canvas = newcanvas
        for d in dubs:
            canvas.paste(arrow, (round(((d - low) / (high - low) * (1600))) + 15 - 30 + 3, 0))
        newcanvas = Image.new('RGBA', (bar.size[0] + 30 + 20, bar.size[1] + 30), (255, 255, 255, 0))
        newcanvas.paste(canvas, (10, 0))
        canvas = newcanvas
        canvas = canvas.resize((800 + 10 + 15, 60 + 15), Image.ANTIALIAS)

        time.sleep(1)
        canvas.save("output.png")
        with open('output.png', 'rb') as f:
            await self.bot.send_file(context.message.channel, f,
                                     content=context.message.author.mention + ", Between {} and {}, I rolled: {}{}{}".format(
                                         low, high, ["", "**"][roll in dubs], roll, ["!", "**! 🌟"][roll in dubs]))


def setup(bot):
    bot.add_cog(Random(bot))