import random

import discord
from discord import app_commands
from discord.ext import commands

FOOD_LIST = [
    "麥當勞", "肯德基", "便利商店",
    "牛肉麵", "壽司", "八方雲集", "咖哩",
    "不吃", "喝紅酒", "芋頭火鍋", "香菜洋芋片",
]


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _decide_meal(self, interaction: discord.Interaction, meal: str):
        food = random.choice(FOOD_LIST)
        await interaction.response.send_message(
            f"The Reaper has decided. For {meal}, you're having **{food}**!"
        )

    @app_commands.command(name="hello", description="跟 Calli 打個招呼")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'Yo Minasan, hey {interaction.user.mention}! This is your Mori! GUH! 💀'
        )

    @app_commands.command(name="lunch", description="讓 Calli 幫你決定午餐吃什麼")
    async def lunch(self, interaction: discord.Interaction):
        await self._decide_meal(interaction, "lunch")

    @app_commands.command(name="dinner", description="讓 Calli 幫你決定晚餐吃什麼")
    async def dinner(self, interaction: discord.Interaction):
        await self._decide_meal(interaction, "dinner")


async def setup(bot):
    await bot.add_cog(General(bot))
