import discord
from discord.ext import commands

class Lmao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author == self.bot.user:
            return

        if message.content == "超好笑":
            embed = discord.Embed(color=discord.Color.brand_red())
            
            embed.set_image(url="https://imgur.com/gallery/up-1616-IYf0am5#/t/photo")
            
            await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Lmao(bot))
