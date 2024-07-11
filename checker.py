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
import os
from discord import SyncWebhook
from dotenv import load_dotenv



load_dotenv()
url = os.getenv("WEBHOOK_URL")
email = "siyagour105@gmail.com" 
zip_code = "08817" 
radius = "22.5"
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

        subject = "BOT FOUND SAT TEST CENTER AVAILABLE"
        body = "A TEST CENTER IS AVAILABLE GO SIGN UP!!!! "
        sender = "diamondjetzrule@gmail.com"
        password = "rzaoypgdnrdumtvi"

        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Convert message to string
        text = message.as_string()
        if number > 0:
            try: 
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, email, text)

                server.sendmail(sender, email, text)
                emailSent = True
                webhook = SyncWebhook.from_url(url)
                webhook.send("A TEST CENTER IS AVAILABLE GO SIGN UP!!!")
            except Exception as e:
                print(f"Error: {e}")

            finally:
                server.quit()
                program.teardown_method()




program = TestSiteChecker()
program.setup_method()
while True:
    program.test_satchecker()
    time.sleep(30)

