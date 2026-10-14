import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class MoriBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        for file in sorted((BASE_DIR / "cogs").glob("*.py")):
            if file.name.startswith("_"):
                continue
            await self.load_extension(f"cogs.{file.stem}")
            print(f"已載入 cog:{file.stem}")
        await self.tree.sync()
        print("--- 指令同步完成 ---")

    async def on_ready(self):
        print(f'Mori 已登入:{self.user}')
        await self.change_presence(activity=discord.Game('Hololive'))
        print('Finney\'s Izakaya Mori Bot 準備營業!')


if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise SystemExit("找不到 DISCORD_TOKEN,請確認 .env 檔案")

    if os.getenv("PORT"):
        from keep_alive import keep_alive
        keep_alive()

    bot = MoriBot()
    bot.run(token)
