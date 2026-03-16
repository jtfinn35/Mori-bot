import discord
from discord.ext import commands

class ReplyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
          
        if message.content == "超好笑":
            await message.channel.send("")

async def setup(bot):
    await bot.add_cog(ReplyCog(bot))
