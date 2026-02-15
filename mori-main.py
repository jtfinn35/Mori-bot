import discord
from discord.ext import commands
import os
from keep_alive import keep_alive 

class MoriBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        await self.tree.sync()

bot = MoriBot()
keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))