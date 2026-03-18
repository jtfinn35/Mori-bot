import discord
from discord.ext import commands
import os
from keep_alive 
import keep_alive

class MoriBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        await self.tree.sync()
        print("--- 指令同步完成 ---")

    async def on_ready(self):
        print(f'Mori 已登入：{self.user}')
        await self.change_presence(activity=discord.Game('Hololive'))
        print('Finney\'s Izakaya Mori Bot 準備營業！')

if __name__ == "__main__":
    bot = MoriBot()
    keep_alive()
    token = os.getenv('DISCORD_TOKEN')
    bot.run(token)
