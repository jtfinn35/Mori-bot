import json
import os
from pathlib import Path

import aiohttp
import discord
from discord.ext import commands, tasks

# 記錄上一次通知過的直播 ID,bot 重開也不會重複 @everyone
STATE_FILE = Path(__file__).resolve().parent.parent / "stream_state.json"

MORI_YT_CHANNEL_ID = "UCMwGHR0E56BWOqGzpMLRy9Q"  # Mori 的 YouTube ID
DEFAULT_NOTIFY_CHANNEL_ID = 1471567945154171114     # 要發通知的 Discord 頻道


class StreamCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("HOLODEX_API_KEY")
        self.notify_channel_id = int(os.getenv("NOTIFY_CHANNEL_ID", DEFAULT_NOTIFY_CHANNEL_ID))
        self.last_video_id = self._load_last_video_id()
        self.session = None

    # ---------- 狀態存檔 ----------
    def _load_last_video_id(self):
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8")).get("last_video_id")
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def _save_last_video_id(self, video_id):
        try:
            STATE_FILE.write_text(json.dumps({"last_video_id": video_id}), encoding="utf-8")
        except OSError as e:
            print(f"寫入直播狀態檔失敗:{e}")

    # ---------- cog 生命週期 ----------
    async def cog_load(self):
        if not self.api_key:
            print("警告:沒有設定 HOLODEX_API_KEY,開台通知不會啟動")
            return
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))
        self.check_stream.start()

    async def cog_unload(self):
        self.check_stream.cancel()
        if self.session:
            await self.session.close()

    # ---------- 主迴圈 ----------
    @tasks.loop(minutes=2)
    async def check_stream(self):
        channel = self.bot.get_channel(self.notify_channel_id)
        if channel is None:
            print(f"找不到通知頻道 {self.notify_channel_id},請確認 bot 有在那個伺服器且看得到該頻道")
            return

        url = "https://holodex.net/api/v2/live"
        params = {"channel_id": MORI_YT_CHANNEL_ID, "status": "live"}
        headers = {"X-APIKEY": self.api_key}

        try:
            async with self.session.get(url, params=params, headers=headers) as resp:
                if resp.status != 200:
                    print(f"Holodex 回應異常:HTTP {resp.status}")
                    return
                data = await resp.json()
        except Exception as e:
            print(f"檢查直播時發生錯誤:{e}")
            return

        if not data:
            return  # 沒在直播

        video = data[0]
        video_id = video["id"]
        if video_id == self.last_video_id:
            return  # 這場已經通知過了

        title = video.get("title", "")
        stream_url = f"https://www.youtube.com/watch?v={video_id}"

        embed = discord.Embed(
            title="💀 GUH! Mori Calliope 開台啦!",
            description=f"**{title}**\n\n[Click to enter the underworld.]({stream_url})",
            color=0xff0000,
        )
        embed.set_image(url=f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg")

        try:
            await channel.send(
                content="@everyone Mori開台囉!",
                embed=embed,
                allowed_mentions=discord.AllowedMentions(everyone=True),
            )
        except discord.HTTPException as e:
            print(f"發送開台通知失敗:{e}")
            return

        # 成功發出去才記錄,避免發送失敗後就再也不通知
        self.last_video_id = video_id
        self._save_last_video_id(video_id)

    @check_stream.before_loop
    async def before_check_stream(self):
        # 等 bot 完全登入、頻道快取好之後才開始檢查
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(StreamCheck(bot))
