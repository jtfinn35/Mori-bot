import discord
from discord.ext import commands
from discord import app_commands  
import random
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Mori is online!" 

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'目前登入身分：{bot.user}')
    
    game = discord.Game('Hololive')
    await bot.change_presence(status=discord.Status.online, activity=game)
    
    try:
        synced = await bot.tree.sync()
        print(f"成功同步了 {len(synced)} 個斜線指令！")
    except Exception as e:
        print(f"同步指令時發生錯誤: {e}")
        
    print('Mori Calliope is ready！')

@bot.tree.command(name="hello", description="跟 Mori 打個招呼")
async def hello(interaction: discord.Interaction):

    await interaction.response.send_message(f'Yo Minasan, hey {interaction.user.mention}! This is your Mori! GUH! 💀')


@bot.tree.command(name="lunch", description="讓死神幫你決定午餐吃什麼")
async def lunch(interaction: discord.Interaction):
    food_list = [
        "麥當勞", "肯德基", "便利商店", 
        "牛肉麵", "水餃", "壽司", 
        "不吃！", "喝紅酒", "芋頭火鍋", "香菜洋芋片"
    ]
    food = random.choice(food_list)
    await interaction.response.send_message(f"The Reaper has decided. Today you're having **{food}**!")


if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    keep_alive()
    bot.run(token)