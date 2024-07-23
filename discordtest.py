import os 
import discord
from discord import SyncWebhook
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("WEBHOOK_URL")
def main():
    webhook = SyncWebhook.from_url(url)
    embed = discord.Embed(title="SAT Test Center Available", description="A test center is available close to you!!!", color=0x00ff00)
    webhook.send("@everyone",embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True))
    

if __name__ == "__main__":
    main()