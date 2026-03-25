import discord
from discord.ext import commands, tasks
import aiohttp
import os

class StreamCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = "UCMwGHR0E56BWOqGzpMLRy9Q" # Mori 的 YouTube ID
        self.api_key = os.getenv("HOLODEX_API_KEY")
        self.last_video_id = None 
        self.check_stream.start() 

    def cog_unload(self):
        self.check_stream.cancel()

    @tasks.loop(minutes=2) 
    async def check_stream(self):
        target_channel = self.bot.get_channel(1471567945154171114) 
        if not target_channel:
            return

        url = f"https://holodex.net/api/v2/live?channel_id={self.channel_id}&status=live"
        headers = {"X-APIKEY": self.api_key}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data and len(data) > 0:
                            video = data[0]
                            video_id = video['id']
                            title = video['title']

                            if video_id != self.last_video_id:
                                self.last_video_id = video_id
                                stream_url = f"https://www.youtube.com/watch?v={video_id}"
                                
                                embed = discord.Embed(
                                    title="💀 GUH! Mori Calliope 開台啦！",
                                    description=f"**{title}**\n\n[Click to enter the underworld.]({stream_url})",
                                    color=0xff0000
                                )
                                embed.set_image(url=f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg")
                                
                                await target_channel.send(content="@everyone Mori開台囉！", embed=embed)
                        else:
                            pass
        except Exception as e:
            print(f"檢查直播時發生錯誤: {e}")

async def setup(bot):
    await bot.add_cog(StreamCheck(bot))
