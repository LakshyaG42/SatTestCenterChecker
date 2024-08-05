import os 
import discord
from discord import SyncWebhook
from dotenv import load_dotenv
import time

load_dotenv()
url = os.getenv("WEBHOOK_URL")
def main():
    webhook = SyncWebhook.from_url(url)
    embed = discord.Embed(title="This is a test disregard.", description="Testing", color=0x00ff00)
    message = webhook.send(embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True), wait=True)
    time.sleep(5)
    message.delete()
    

if __name__ == "__main__":
    main()