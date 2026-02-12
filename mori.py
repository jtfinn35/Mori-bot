import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'目前登入身分：{bot.user}')
    game = discord.Game('Hololive')
    await bot.change_presence(status=discord.Status.online, activity=game)
    print('Mori Calliope is ready！')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Yo Minasan, hey {ctx.author.mention}! This is your Mori! GUH! 💀')

@bot.command()
async def 午餐(ctx):
    food_list = [
        "麥當勞", "肯德基", "便利商店", 
        "牛肉麵", "水餃", "壽司", 
        "不吃！", "喝紅酒", "芋頭火鍋", "香菜洋芋片"
    ]
    food = random.choice(food_list)
    await ctx.send(f"The Reaper has decided. Today you're having **{food}**!")

bot.run('MTQ3MTQ2NTgzNDg3NzU1MDcyNQ.GgbbkM.vczFzU3LcuSeJKPIHKNDrf29hgHqCUFPOm44fs')