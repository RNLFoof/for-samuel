import discord
from PIL import Image
from discord.ext import commands
from discord.ext.commands import Cog

import modules.talking as talking
import random
import asyncio
import modules.basics as basics

class Development(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def reload(self, context):
        module = basics.contentq(context.message.content,split=False)
        try:
            try:
                self.bot.unload_extension(module)
            except:
                pass
            await asyncio.sleep(1)
            self.bot.load_extension(module)
        except Exception as e:
            await talking.say(context,'Ouch.\n{}: {}'.format(type(e).__name__, e))
        else:
            await talking.say(context,'Okay, {} reloaded.'.format(module))
            print("{0} reloaded.".format(module))

    @commands.command(hidden=True)
    async def reset(self, context):
        bot = self.bot
        basics.startup(bot)
        await talking.reply(context,"Variables reset.")

    @commands.command(hidden=True)
    async def superpowers(self, context):
        bot = self.bot
        # for r in bot.epicord.roles:
        #     if r.name.startswith("dadmin"):
        #         await talking.say(context,str(r.id))
        role = bot.epicord.get_role(399725620696973312)
        bot.rnl = bot.epicord.get_member(bot.rnl.id)
        if role in bot.rnl.roles:
            await bot.rnl.remove_roles(role)
        else:
            await bot.rnl.add_roles(role)

    @commands.command(hidden=True, aliases=["s", "sp", "spoilers"])
    async def spoiler(self, context):
        await context.message.delete();

    @commands.command(hidden=True)
    async def aespreviews(self, context):
        bot=self.bot
        s=""
        emojiserver = bot.get_guild(476435378153324545)

        # for c in [
        #     (255, 24, 0, 255),
        #     (255, 126, 0, 255),
        #     (204, 255, 0, 255),
        #     (0, 36, 255, 255),
        #     (144, 0, 255, 255),
        #     (255, 0, 240, 255),
        #     (255, 0, 66, 255),
        # ]:
        for c in [
            (255, 0, 66, 255),
            (250, 50, 102, 255),
            (240, 32, 89, 255),
        ]:
            x = "base_bubbles.png"
            overlay = Image.open("C:\\Users\\Zachary\\Desktop\\kkk\\Non-GML\\ButtBot\\epicord-bot-master\\Images\\Emojis\\" + x, 'r').convert('RGBA')
            overlaydata = overlay.load()
            avatar = Image.open("C:\\Users\\Zachary\\Desktop\\kkk\\Non-GML\\ButtBot\\epicord-bot-master\\Images\\Emojis\\sample_avatar.png", 'r').convert('RGBA')
            pixdata = avatar.load()
            width, height = avatar.size
            for y2 in range(height):
                for x2 in range(width):
                    if overlaydata[x2, y2] == (255, 0, 0, 255):
                        pixdata[x2, y2] = (0, 0, 0, 0)
                    if overlaydata[x2, y2] == (0, 0, 255, 255):
                        pixdata[x2, y2] = c
            avatar.save("tobedeleted/test.png")
            with open("tobedeleted/test.png", 'rb') as f:
                f = f.read()
                s += str(await emojiserver.create_custom_emoji(name="test", image=f))+"\n"
        await talking.say(context,s)

        
def setup(bot):
    bot.add_cog(Development(bot))