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
            await message.channel.send("https://raw.githubusercontent.com/jtfinn35/Mori-bot/main/%E8%B6%85%E5%A5%BD%E7%AC%91-%E5%BD%A9.png")

async def setup(bot):
    await bot.add_cog(ReplyCog(bot))
