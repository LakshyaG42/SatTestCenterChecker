import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import discord
from discord import SyncWebhook
from dotenv import load_dotenv



load_dotenv()
url = "https://discord.com/api/webhooks/1269454952980414474/CHZd2JwcKqPphSuJ4NaKt1bpAsppC6kqSh9vvpsa1pzoJ1_gX2xgHmV84M1bXWeajtwm"
zip_code = "08844" 
radius = "16"
class TestSiteChecker():
    def setup_method(self):
        service = Service('chromedriver.exe') 
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(30) 
        self.vars = {}
        self.actions = ActionChains(self.driver)
        

    def teardown_method(self):
        self.driver.quit()
    
    def test_satchecker(self):
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
        if radius not in [10, 25, 50, 100]:
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
            self.test_satchecker()
        print(number)


        
        if number > 0:
            try: 
                message.delete()
                webhook = SyncWebhook.from_url(url)
                embed = discord.Embed(title="SAT Test Center Available", description="A test center is available close to you!!!", color=0x00ff00)
                webhook.send("@everyone",embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True))
            except Exception as e:
                print(f"Error: {e}")

            finally:
                program.teardown_method()




if __name__ == "__main__":
    program = TestSiteChecker()
    program.setup_method()
    print("Setting up...")
    
    try:
        webhook = SyncWebhook.from_url(url)
        embed = discord.Embed(title="SAT Test Center Checker is Running", description="The program will run until there is a test center found.", color=0x00ff00)
        message = webhook.send(embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True), wait=True)
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
    while True:
        program.test_satchecker()
        time.sleep(10)

