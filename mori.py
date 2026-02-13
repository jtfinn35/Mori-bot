import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
import os
import feedparser
from flask import Flask
from threading import Thread

# --- 1. Flask Keep Alive (確保機器人不間斷運行) ---
app = Flask('')

@app.route('/')
def home():
    return "Mori is online!" 

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. MoriBot 核心類別 ---
class MoriBot(commands.Bot):
    def __init__(self):
        # 設定 Intents 權限
        intents = discord.Intents.all() 
        super().__init__(command_prefix='!', intents=intents)
        
        # 決定午晚餐名單
        self.food_list = [
            "麥當勞", "肯德基", "便利商店", 
            "牛肉麵", "水餃", "壽司", 
            "不吃！", "喝紅酒", "芋頭火鍋", "香菜洋芋片"
        ]
        
        # --- 推特追蹤設定 ---
        self.last_tweet_id = None
        self.twitter_rss_url = "https://nitter.net/moricalliope/rss" 
        self.twitter_discord_channel = 1471567440449245255 
        
        # --- YouTube 追蹤設定 ---
        self.last_yt_id = None
        self.yt_rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCvInbdad9HTW7gM8_6mI6Ew"
        self.yt_discord_channel = 1471567945154171114 

    async def setup_hook(self):
        # 啟動背景任務循環
        self.check_twitter_task.start()
        self.check_youtube_task.start()
        # 同步 Slash 指令
        synced = await self.tree.sync()
        print(f"成功同步了 {len(synced)} 個斜線指令！")

    async def on_ready(self):
        print(f'目前登入身分：{self.user}')
        await self.change_presence(activity=discord.Game('Hololive'))
        print('Finney\'s Izakaya Mori Bot 上線中！')

    # --- 任務一：YouTube 直播/影片通知 ---
    @tasks.loop(minutes=3.0)
    async def check_youtube_task(self):
        channel = self.get_channel(self.yt_discord_channel)
        if not channel: return

        feed = feedparser.parse(self.yt_rss_url)
        if not feed.entries: return

        latest_video = feed.entries[0]
        video_id = latest_video.link 

        if self.last_yt_id != video_id:
            if self.last_yt_id is not None:
                # --- 抓取縮圖內容 ---
                thumbnail_url = ""
                if 'media_thumbnail' in latest_video:
                    thumbnail_url = latest_video.media_thumbnail[0]['url']
                
                embed = discord.Embed(
                    title="🔴 Mori is in the room!",
                    description=f"**{latest_video.title}**\n\n[點擊此處前往觀看]({latest_video.link})",
                    url=latest_video.link,
                    color=0x7f0020 
                )
                
                if thumbnail_url:
                    embed.set_image(url=thumbnail_url)
                    
                # 修改為與推特一致的「特報」風格
                embed.set_footer(text="Finney's Izakaya • 本日開演特報")
                await channel.send(content="Deadbeats, listen up! New stream or video is out!", embed=embed)
            self.last_yt_id = video_id

    # --- 任務二：Twitter (X) 貼文通知 ---
    @tasks.loop(minutes=5.0)
    async def check_twitter_task(self):
        channel = self.get_channel(self.twitter_discord_channel)
        if not channel: return

        feed = feedparser.parse(self.twitter_rss_url)
        if not feed.entries: return

        latest_tweet = feed.entries[0]
        tweet_id = latest_tweet.id

        if self.last_tweet_id != tweet_id:
            if self.last_tweet_id is not None:
                embed = discord.Embed(
                    title="🏮 冥界特報 (Twitter)",
                    description=latest_tweet.summary,
                    url=latest_tweet.link,
                    color=0x7f0020 
                )
                # 維持你設定的店內轉播風格
                embed.set_footer(text="Finney's Izakaya • 本日特選推報")
                await channel.send(content="Deadbeats, assemble!", embed=embed)
            self.last_tweet_id = tweet_id

    @check_youtube_task.before_loop
    @check_twitter_task.before_loop
    async def before_tasks(self):
        await self.wait_until_ready()

# --- 3. 指令定義 ---
bot = MoriBot()

@bot.tree.command(name="hello", description="跟 Mori 打個招呼")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Yo Minasan, hey {interaction.user.mention}! This is your Mori! GUH! 💀')

@bot.tree.command(name="lunch", description="讓死神幫你決定午餐吃什麼")
async def lunch(interaction: discord.Interaction):
    food = random.choice(bot.food_list)
    await interaction.response.send_message(f"The Reaper has decided. For lunch, you're having **{food}**!")

@bot.tree.command(name="dinner", description="讓死神幫你決定晚餐吃什麼")
async def dinner(interaction: discord.Interaction):
    food = random.choice(bot.food_list)
    await interaction.response.send_message(f"The Reaper has decided. For dinner, you're having **{food}**!")

# --- 4. 啟動 ---
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    keep_alive()
    bot.run(token)