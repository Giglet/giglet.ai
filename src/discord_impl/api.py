import requests
import discord
import os
import random
from dotenv import load_dotenv
from src.ai_chat.chat import is_msg_spam

# from dot
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot_emoji_exp = {
    "spam": "🚫",
}

def mention_str(user_id):
    return "<@{0}>".format(user_id)

class GigletAIBot(discord.Client):
    def mention_str(self):
        return mention_str(self.user.id)

    async def send_alert_msg(self, msg, userID):
        channel_id = 1111320761731387432
        channel = self.get_channel(channel_id)
        await channel.send("{0} spam detected: {1} {2}".format(bot_emoji_exp["spam"], mention_str(userID), msg))


    async def on_ready(self):
        print('logged on as {0}'.format(self.user))

    async def on_message(self, message):
        msg_content = message.content
        if message.author == self.user:
            return

        if is_msg_spam(msg_content):
            await self.send_alert_msg(msg_content, message.author.id)
            return

# init bot
intents = discord.Intents.default()
intents.message_content = True
client = GigletAIBot(intents=intents)
