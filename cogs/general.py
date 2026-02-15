import discord
from discord.ext import commands
from discord import app_commands
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.food_list = [
            "麥當勞", "肯德基", "便利商店", 
            "牛肉麵", "壽司", "八方雲集", "咖哩", 
            "不吃", "喝紅酒", "芋頭火鍋", "香菜洋芋片"
        ]

    @app_commands.command(name="hello", description="跟 Calli 打個招呼")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Yo Minasan, hey {interaction.user.mention}! This is your Mori! GUH! 💀')

    @app_commands.command(name="lunch", description="讓 Calli 幫你決定午餐吃什麼")
    async def lunch(self, interaction: discord.Interaction):
        food = random.choice(self.food_list)
        await interaction.response.send_message(f"The Reaper has decided. For lunch, you're having **{food}**!")

    @app_commands.command(name="dinner", description="讓 Calli 幫你決定晚餐吃什麼")
    async def dinner(self, interaction: discord.Interaction):
        food = random.choice(self.food_list)
        await interaction.response.send_message(f"The Reaper has decided. For dinner, you're having **{food}**!")

async def setup(bot):
    await bot.add_cog(General(bot))
