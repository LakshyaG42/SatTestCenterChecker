import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
email = os.getenv("EMAIL")
zip_code = os.getenv("ZIP_CODE")
radius = os.getenv("RADIUS")

class SATChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.driver = None
        self.check_sat_availability.start()

    def setup_driver(self):
        service = Service('chromedriver.exe') 
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(30)
        self.actions = ActionChains(self.driver)
    
    def teardown_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def check_availability(self):
        if not self.driver:
            self.setup_driver()
        
        self.driver.get("https://satsuite.collegeboard.org/sat/test-center-search")

        zipcode_enter = self.driver.find_element(By.ID, "apricot_input_5")
        zipcode_enter.send_keys(zip_code)

        script = f'''
        var select = document.getElementById('apricot_select_6');
        var option = document.createElement('option');
        option.value = '{radius}';
        option.text = '{radius} miles';
        select.add(option);
        select.value = '{radius}';
        select.setAttribute('data-cb-value', '{radius}');
        var event = new Event('change', {{ bubbles: true }});
        select.dispatchEvent(event);
        '''
        if radius not in ['10', '25', '50', '100']:
            self.driver.execute_script(script)

        dropdown = self.driver.find_element(By.ID, "apricot_select_6")
        select = Select(dropdown)
        select.select_by_value(radius)

        button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Find a Test Center')]")
        button.click()

        try:
            element = self.driver.find_element(By.XPATH, "//*[contains(text(),'Test centers with available seats')]")
            text = element.text
            number = int(re.findall(r'\d+', text)[0])
        except (NoSuchElementException, IndexError):
            number = 0

        return number

    @tasks.loop(minutes=10)
    async def check_sat_availability(self):
        number = self.check_availability()
        if number > 0:
            try:
                webhook = discord.SyncWebhook.from_url(WEBHOOK_URL)
                embed = discord.Embed(title="SAT Test Center Available", description="A test center is available close to you!!!", color=0x00ff00)
                webhook.send("@everyone", embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True))
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("No available test centers found.")
    
    @check_sat_availability.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}')

bot = commands.Bot(command_prefix="!")
bot.add_cog(SATChecker(bot))

bot.run(TOKEN)
