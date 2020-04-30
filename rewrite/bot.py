import discord
from discord.ext import commands
import asyncio
import importlib
from types import ModuleType

import modules.talking as talking
import modules.core as core
import modules.loops as loops
import modules.basics as basics
import modules.ccc as ccc
import modules.utility as utility
import modules.aesthetic as aesthetic
import modules.ot as ot
import modules.koth as koth
import modules.ch as ch

import classes
from classes.DictSavable import DictSavable
from classes.OngoingReactionMenu import OngoingReactionMenu
from classes.PageMessage import PageMessage
from classes.Sue import Sue
from classes.ReactionChart import ReactionChart
from classes.Daily import Daily
from classes.InputMenu import InputMenu
from classes.ReactionReactions import ReactionReactions
from classes.Help import Help
from classes.SortableChart import SortableChart
from classes.AchievementBrowser import AchievementBrowser
from classes.Rerollable import Rerollable
from classes.Choose import Choose
from classes.ConfirmMessage import ConfirmMessage
from classes.EightBall import EightBall
from classes.SingleButton import SingleButton
from classes.ObamaToken import ObamaToken
exec(
    """from classes.ObamaSilver import ObamaSilver
from classes.ObamaResidue import ObamaResidue
from classes.OnTheFlySingleButton import OnTheFlySingleButton"""
)

bot = commands.Bot("s!")
spoilerbot = commands.Bot("s!")
bot.spoilerbot = spoilerbot

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    cogs = ["audio","development","eight","emojis","personalization","quality of life","shitposts","time","meta","users","obama tokens","serious","group input","internal games","random","images"]
    for cog in cogs:
        try:
            bot.load_extension("cogs." + cog)
            print(f"Loaded cogs.{cog}")
        except Exception as e:
            print(f"Failed to load cogs.{cog}. {type(e).__name__}: {e}")
            
    basics.startup(bot)

@spoilerbot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

@bot.event
async def on_message(m):
    await core.on_message(bot, m)

@bot.event
async def on_message_edit(before, after):
    await core.on_message_edit(bot, before, after)

@bot.event
async def on_raw_message_edit(payload):
    await core.on_raw_message_edit(bot, payload)

@bot.event
async def on_raw_reaction_add(payload):
    await core.on_raw_reaction_add(bot, payload)

@bot.event
async def on_raw_reaction_remove(payload):
    await core.on_raw_reaction_remove(bot, payload)
    
@bot.command(hidden=True)
async def mf(context):
    s = ""
    for module in [
        (talking,"Talking"),
        (core,"Core"),
        (loops,"Loops"),
        (basics,"Basics"),
        (ccc,"CCC"),
        (utility,"Utility"),
        (aesthetic,"Aesthetic"),
        (ot,"OT"),
        (koth,"koth"),
        (ch,"ch"),
        
        (classes.DictSavable,"DictSavable"),
        (classes.OngoingReactionMenu,"OngoingReactionMenu"),
        (classes.PageMessage,"PageMessage"),
        (classes.Sue,"Sue"),
        (classes.ReactionChart,"ReactionChart"),
        (classes.Daily,"Daily"),
        (classes.InputMenu,"InputMenu"),
        (classes.ReactionReactions,"ReactionReactions"),
        (classes.Help,"Help"),
        (classes.SortableChart,"SortableChart"),
        (classes.AchievementBrowser,"AchievementBrowser"),
        (classes.FlockOfInvites,"FlockOfInvites"),
        (classes.Petition,"Petition"),
        (classes.Rerollable,"Rerollable"),
        (classes.Choose,"Choose"),
        (classes.ConfirmMessage,"ConfirmMessage"),
        (classes.SingleButton,"SingleButton"),
        (classes.ObamaToken,"ObamaToken"),
        (classes.ObamaSilver, "ObamaSilver"),
        (classes.EightLineFromSonic06, "EightLineFromSonic06"),
        (classes.OnTheFlySingleButton, "OnTheFlySingleButton"),
        (classes.ObamaResidue, "ObamaResidue"),
        (classes.EightBannedUser, "EightBannedUser"),
    ]:
        try:
            importlib.reload(module[0])
        except Exception as e:
            s += f"{module[1]} failed to load. {type(e).__name__}: {e}\n"
        else:
            s += f"{module[1]} reloaded.\n"
            print(f"{module[1]} reloaded.")
    print("----------")
    for x in ["EightBall","ObamaToken"]:
        exec(f"""global {x}
from classes.{x} import {x}""")
    await talking.say(context,s)
        
loop = asyncio.get_event_loop()
loop.create_task(bot.start('token goes here lol'))
loop.run_forever()

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(bot.logout())
    # cancel all tasks lingering
finally:
    loop.close()