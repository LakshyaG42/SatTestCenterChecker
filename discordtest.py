import os 
from discord import SyncWebhook
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("WEBHOOK_URL")
def main():
    webhook = SyncWebhook.from_url(url)
    webhook.send("Hello World")

if __name__ == "__main__":
    main()