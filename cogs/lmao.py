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
            await message.channel.send("https://imgur.com/gallery/up-1616-IYf0am5#/t/photo")

async def setup(bot):
    await bot.add_cog(ReplyCog(bot))
